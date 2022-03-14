"""Module to create a project-level table for DBCP to use in spreadsheet tools."""
from typing import Sequence, Optional
from re import IGNORECASE

import sqlalchemy as sa
import pandas as pd
import numpy as np
from dbcp.helpers import get_sql_engine


def _subset_db_columns(columns: Sequence[str], table: str, engine: sa.engine.Engine)-> pd.DataFrame:
    query = f"SELECT {', '.join(columns)} FROM {table}"
    df = pd.read_sql(query, engine)
    return df

def _get_iso_location_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = [
        'project_id',
        #'county',  # drop raw name in favor of canonical FIPS name
        #'state',  # drop raw name in favor of canonical FIPS name
        'state_id_fips',
        'county_id_fips',
        #'locality_name',  # drop detailed location info for simplicity
        #'locality_type',  # drop detailed location info for simplicity
        #'containing_county',  # drop geocoded name in favor of canonical FIPS name
    ]
    db = 'dbcp.iso_locations'
    
    simple_location_df = _subset_db_columns(cols, db, engine)
    # If multiple counties, just pick the first one. This is simplistic but there are only 26/13259 (0.2%)
    simple_location_df = simple_location_df.groupby('project_id', as_index=False).nth(0)
    return simple_location_df

def _get_iso_resource_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = [
        'capacity_mw',
        #'project_class',  # will model this according to client wants
        'project_id',
        #'resource',  # drop raw name in favor of resource_clean
        #'resource_class',  # will model this according to client wants
        'resource_clean',
    ]
    db = 'dbcp.iso_resource_capacity'
    df = _subset_db_columns(cols, db, engine)
    return df

def _get_iso_project_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = [
        'date_operational',
        'date_proposed',
        #'date_proposed_raw',  # drop raw date in favor of parsed date_proposed
        'date_withdrawn',
        #'date_withdrawn_raw',  # drop raw date in favor of parsed date_withdrawn
        'days_in_queue',
        'developer',
        'entity',
        'interconnection_status_lbnl',
        #'interconnection_status_raw',  # drop raw status in favor of interconnection_status_lbnl
        'point_of_interconnection',
        'project_id',
        'project_name',
        'queue_date',
        #'queue_date_raw',  # drop raw date in favor of parsed queue_date
        #'queue_id',  # not a candidate key due to hundreds of missing NYISO withdrawn IDs
        'queue_status',
        #'queue_year',   # year info is contained in queue_date
        'region',
        #'resource_type_lbnl',  # just use clean types for simplicity
        'utility',
        'withdrawl_reason',
        #'year_operational',  # year info is contained in date_operational
        #'year_proposed',  # year info is contained in date_proposed
        #'year_withdrawn',  # year info is contained in date_withdrawn
    ]
    db = 'dbcp.iso_projects'
    df = _subset_db_columns(cols, db, engine)
    return df

def _get_ncsl_wind_permitting_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = [
        'description',
        #'link',  # too detailed?
        'permitting_type',
        #'state',  # only need FIPS, state name comes from elsewhere
        'state_id_fips',
    ]
    db = 'dbcp.ncsl_state_permitting'
    df = _subset_db_columns(cols, db, engine)
    return df

def _get_local_opposition_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = [
        #'containing_county',  # only need FIPS, names come from elsewhere
        'county_id_fips',
        'earliest_year_mentioned',
        #'latest_year_mentioned',  # for simplicity, only include one year metric (earliest_year_mentioned)
        'locality_name',
        'locality_type',
        #'n_years_mentioned',  # for simplicity, only include one year metric (earliest_year_mentioned)
        'ordinance',
        #'raw_locality_name',  # drop raw name in favor of geocoded one
        #'state',  # only need FIPS, names come from elsewhere
        #'state_id_fips',  # will join on 5-digit county FIPS, which includes state
    ]
    db = 'dbcp.local_ordinance'
    df = _subset_db_columns(cols, db, engine)
    return df

def _get_state_opposition_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = [
        'earliest_year_mentioned',
        #'latest_year_mentioned',  # for simplicity, only include one year metric (earliest_year_mentioned)
        #'n_years_mentioned',  # for simplicity, only include one year metric (earliest_year_mentioned)
        'policy',
        #'state',  # only need FIPS, names come from elsewhere
        'state_id_fips',
    ]
    db = 'dbcp.state_policy'
    df = _subset_db_columns(cols, db, engine)
    return df

def _get_county_fips_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = ['*']
    db = 'dbcp.county_fips'
    df = _subset_db_columns(cols, db, engine)
    return df


def _get_state_fips_df(engine: sa.engine.Engine) -> pd.DataFrame:
    cols = ['*']
    db = 'dbcp.state_fips'
    df = _subset_db_columns(cols, db, engine)
    return df

def _combine_state_and_local_opposition_as_counties(state_df: pd.DataFrame, local_df: pd.DataFrame, county_fips_df: pd.DataFrame, state_fips_df: pd.DataFrame) -> pd.DataFrame:
    # drop states that repealed their policies or whose policy was pro-RE not anti-RE
    fips_codes_to_drop = {'23', '36'} # Maine, New York
    filtered_state_df = state_df.loc[~state_df.loc[:, 'state_id_fips'].isin(fips_codes_to_drop),:]
    filtered_state_df = filtered_state_df.merge(state_fips_df[['state_abbrev', 'state_id_fips']], on='state_id_fips', how='left')
    states_as_counties = filtered_state_df.merge(county_fips_df, on='state_id_fips', how='left')
    combined = states_as_counties.merge(local_df, on='county_id_fips', how='outer')

    assert local_df['locality_type'].isna().sum() == 0
    combined['locality_type'] = combined['locality_type'].fillna('state')
    combined['locality_name'] = combined['locality_name'].fillna(combined['state_abbrev'])
    
    # resolve overlapping columns
    # fillna county earliest year with state earliest year
    combined['earliest_year_mentioned'] = combined['earliest_year_mentioned_y'].fillna(combined['earliest_year_mentioned_x'])

    # concatenate the intersection (only 4 counties)
    has_both = combined[['ordinance', 'policy']].notna().all(axis=1)
    combined.loc[has_both, 'ordinance'] = combined.loc[has_both, 'ordinance'] + (' State Policy: ' + combined.loc[has_both, 'policy'])
    combined.loc[:, 'ordinance'] = combined['ordinance'].fillna('State Policy: ' + combined['policy'])

    combined = combined[['county_id_fips', 'locality_name', 'locality_type', 'ordinance', 'earliest_year_mentioned']]
    return combined


def _agg_local_ordinances_to_counties(ordinances: pd.DataFrame) -> pd.DataFrame:

    dupe_counties = ordinances.duplicated(subset='county_id_fips', keep=False)
    dupes = ordinances.loc[dupe_counties,:].copy()
    not_dupes = ordinances.loc[~dupe_counties,:].copy()
    
    dupes['ordinance'] = dupes['locality_name'] + ': ' + dupes['ordinance'] + '\n'
    grp = dupes.groupby('county_id_fips')

    years = grp['earliest_year_mentioned'].min()

    n_unique = grp[['locality_name', 'locality_type']].nunique()
    localities = grp[['locality_name', 'locality_type']].nth(0).mask(n_unique > 1, other='multiple')

    descriptions = grp['ordinance'].sum().str.strip()

    agg_dupes = pd.concat([years, localities, descriptions], axis=1).reset_index()
    recombined = pd.concat([not_dupes, agg_dupes], axis=0, ignore_index=True).sort_values('county_id_fips')
    assert not recombined.duplicated(subset='county_id_fips').any()

    return recombined

def _convert_resource_df_long_to_wide(resource_df: pd.DataFrame) -> pd.DataFrame:
    res_df = resource_df.copy()
    # separate generation from storage
    is_storage = res_df.loc[:,'resource_clean'].str.contains('storage', flags=IGNORECASE)
    res_df['storage_type'] = res_df.loc[:,'resource_clean'].where(is_storage)
    res_df['generation_type'] = res_df.loc[:,'resource_clean'].where(~is_storage)
    gen = res_df.loc[~is_storage,:]
    storage = res_df.loc[is_storage,:]

    group = gen.groupby('project_id')[['generation_type', 'capacity_mw']]
    # first generation source
    rename_dict = {'generation_type': 'generation_type_1', 'capacity_mw': 'generation_capacity_mw_1'}
    gen_1 = group.nth(0).rename(columns=rename_dict)
    # second generation source (very few rows)
    rename_dict = {'generation_type': 'generation_type_2', 'capacity_mw': 'generation_capacity_mw_2'}
    gen_2 = group.nth(1).rename(columns=rename_dict)
    # shouldn't be any with 3 generation types
    assert group.nth(2).shape[0] == 0

    # storage
    assert storage.duplicated('project_id').sum() == 0 # no multi-storage projects
    storage = storage.set_index('project_id')[['storage_type', 'capacity_mw']].rename(columns={'capacity_mw': 'storage_capacity_mw'})

    # combine
    output = gen_1.join([gen_2, storage], how='outer', sort=True)
    assert len(output) == res_df.loc[:,'project_id'].nunique() # all projects accounted for and 1:1
    return output


def _get_and_join_iso_tables(engine: Optional[sa.engine.Engine]=None) -> pd.DataFrame:
    if engine is None:
        engine = get_sql_engine()
    project_df = _get_iso_project_df(engine)
    location_df = _get_iso_location_df(engine)
    resource_df = _get_iso_resource_df(engine)
    resource_df = _convert_resource_df_long_to_wide(resource_df)

    n_total_projects = project_df.loc[:, 'project_id'].nunique()
    combined = resource_df.join([project_df.set_index('project_id'), location_df.set_index('project_id')], how='outer')
    assert len(combined) == n_total_projects
    return combined.reset_index()

def _add_derived_columns(mart: pd.DataFrame) -> pd.DataFrame:
    out = mart.copy()
    out['has_ordinance'] = out['ordinance'].notna()
    out['is_hybrid'] = out[['generation_type_1', 'storage_type']].notna().all(axis=1)

    resource_map = {
        'Onshore Wind': 'renewable',
        'Solar': 'renewable',
        'Natural Gas': 'fossil',
        'Other': 'fossil',
        'Hydro': 'renewable',
        'Geothermal': 'renewable',
        'Offshore Wind': 'renewable',
        'Nuclear': 'other',
        'Coal': 'fossil',
        'Waste Heat': 'fossil',
        'Biofuel': 'renewable',
        'Biomass': 'renewable',
        'Landfill Gas': 'fossil',
        'Oil': 'fossil',
        'Unknown': np.nan,
        'Combustion Turbine': 'fossil',
        'Oil; Biomass': 'fossil',
        'Municipal Solid Waste': 'fossil',
        'Fuel Cell': 'renewable',
        'Steam': np.nan,
        'Solar; Biomass': 'renewable',
        'Methane; Solar': 'other',
        np.nan: np.nan,
    }
    # note that this classifies pure storage facilities as np.nan
    assert set(out['generation_type_1'].unique()) == set(resource_map.keys())
    out['resource_class'] = out['generation_type_1'].map(resource_map)
    
    return out

def make_project_data_mart_table(engine: Optional[sa.engine.Engine]=None) -> pd.DataFrame:
    if engine is None:
        engine = get_sql_engine()
    iso = _get_and_join_iso_tables(engine)
    ncsl = _get_ncsl_wind_permitting_df(engine)
    local_opp = _get_local_opposition_df(engine)
    state_opp = _get_state_opposition_df(engine)
    all_counties = _get_county_fips_df(engine)
    all_states = _get_state_fips_df(engine)

    combined_opp = _combine_state_and_local_opposition_as_counties(state_df=state_opp, local_df=local_opp, county_fips_df=all_counties, state_fips_df=all_states)
    
    # use canonical state and county names
    iso = iso.merge(all_states[['state_abbrev', 'state_id_fips']], on='state_id_fips', how='left', validate='m:1')
    iso = iso.merge(all_counties[['county_name', 'county_id_fips']], on='county_id_fips', how='left', validate='m:1')

    combined = iso.merge(ncsl, on='state_id_fips', how='left', validate='m:1')
    combined = combined.merge(combined_opp, on='county_id_fips', how='left', validate='m:1')

    combined = _add_derived_columns(combined)

    rename_dict = {
        'date_proposed': 'date_proposed_online',
        'interconnection_status_lbnl': 'interconnection_status',
        'queue_date': 'date_entered_queue',
        'region': 'iso_region',
        'locality_name': 'ordinance_jurisdiction_name',
        'locality_type': 'ordinance_jurisdiction_type',
        'description': 'state_permitting_text',
        'permitting_type': 'state_permitting_type',
        'state_abbrev': 'state',
        'county_name': 'county',
    }
    combined = combined.rename(columns=rename_dict)

    col_order = [
        'project_name',
        'project_id',
        'iso_region',
        'entity',
        'utility',
        'developer',
        'state',
        'county',
        'state_id_fips',
        'county_id_fips',
        'resource_class',
        'is_hybrid',
        'generation_type_1',
        'generation_capacity_mw_1',
        'generation_type_2',
        'generation_capacity_mw_2',
        'storage_type',
        'storage_capacity_mw',
        'date_entered_queue',
        'date_operational',
        'date_proposed_online',
        'date_withdrawn',
        'days_in_queue',
        'interconnection_status',
        'point_of_interconnection',
        'queue_status',
        'withdrawl_reason',
        'has_ordinance',
        'ordinance_jurisdiction_name',
        'ordinance_jurisdiction_type',
        'ordinance_earliest_year_mentioned',
        'ordinance',
        'state_permitting_type',
        'state_permitting_text',
    ]
    return combined[col_order]
