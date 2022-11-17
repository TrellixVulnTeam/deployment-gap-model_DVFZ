"""SQL Alchemy metadata for the data mart tables."""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()
schema = "data_mart"

counties_wide_format = Table(
    "counties_wide_format",
    metadata,
    Column("state_id_fips", String, nullable=False),
    Column("county_id_fips", String, primary_key=True),
    Column("state", String),
    Column("county", String, nullable=False),
    Column("has_ordinance", Boolean, nullable=False),
    Column("state_permitting_type", String),
    Column("county_total_co2e_tonnes_per_year", Float),
    Column("fossil_existing_capacity_mw", Float),
    Column("fossil_existing_co2e_tonnes_per_year", Float),
    Column("fossil_existing_facility_count", Integer),
    Column("fossil_proposed_capacity_mw", Float),
    Column("fossil_proposed_co2e_tonnes_per_year", Float),
    Column("fossil_proposed_facility_count", Integer),
    Column("renewable_and_battery_existing_capacity_mw", Float),
    Column("renewable_and_battery_existing_co2e_tonnes_per_year", Float),
    Column("renewable_and_battery_existing_facility_count", Integer),
    Column("renewable_and_battery_proposed_capacity_mw", Float),
    Column("renewable_and_battery_proposed_facility_count", Integer),
    Column("infra_total_proposed_co2e_tonnes_per_year", Float),
    Column("infra_total_proposed_facility_count", Integer),
    Column("infra_total_proposed_nox_tonnes_per_year", Float),
    Column("infra_total_proposed_pm2_5_tonnes_per_year", Float),
    Column("battery_storage_existing_capacity_mw", Float),
    Column("battery_storage_existing_facility_count", Integer),
    Column("battery_storage_proposed_capacity_mw", Float),
    Column("battery_storage_proposed_facility_count", Integer),
    Column("coal_existing_capacity_mw", Float),
    Column("coal_existing_co2e_tonnes_per_year", Float),
    Column("coal_existing_facility_count", Integer),
    Column("coal_proposed_capacity_mw", Float),
    Column("coal_proposed_co2e_tonnes_per_year", Float),
    Column("coal_proposed_facility_count", Integer),
    Column("gas_existing_capacity_mw", Float),
    Column("gas_existing_co2e_tonnes_per_year", Float),
    Column("gas_existing_facility_count", Integer),
    Column("gas_proposed_capacity_mw", Float),
    Column("gas_proposed_co2e_tonnes_per_year", Float),
    Column("gas_proposed_facility_count", Integer),
    Column("offshore_wind_existing_capacity_mw", Float),
    Column("offshore_wind_existing_facility_count", Integer),
    Column("offshore_wind_proposed_capacity_mw", Float),
    Column("offshore_wind_proposed_facility_count", Integer),
    Column("oil_existing_capacity_mw", Float),
    Column("oil_existing_co2e_tonnes_per_year", Float),
    Column("oil_existing_facility_count", Integer),
    Column("onshore_wind_existing_capacity_mw", Float),
    Column("onshore_wind_existing_facility_count", Integer),
    Column("onshore_wind_proposed_capacity_mw", Float),
    Column("onshore_wind_proposed_facility_count", Integer),
    Column("solar_existing_capacity_mw", Float),
    Column("solar_existing_co2e_tonnes_per_year", Float),
    Column("solar_existing_facility_count", Integer),
    Column("solar_proposed_capacity_mw", Float),
    Column("solar_proposed_facility_count", Integer),
    Column("infra_gas_proposed_co2e_tonnes_per_year", Float),
    Column("infra_gas_proposed_facility_count", Integer),
    Column("infra_gas_proposed_nox_tonnes_per_year", Float),
    Column("infra_gas_proposed_pm2_5_tonnes_per_year", Float),
    Column("infra_lng_proposed_co2e_tonnes_per_year", Float),
    Column("infra_lng_proposed_facility_count", Integer),
    Column("infra_lng_proposed_nox_tonnes_per_year", Float),
    Column("infra_lng_proposed_pm2_5_tonnes_per_year", Float),
    Column("infra_oil_proposed_co2e_tonnes_per_year", Float),
    Column("infra_oil_proposed_facility_count", Integer),
    Column("infra_oil_proposed_nox_tonnes_per_year", Float),
    Column("infra_oil_proposed_pm2_5_tonnes_per_year", Float),
    Column(
        "infra_petrochemicals_and_plastics_proposed_co2e_tonnes_per_year",
        Float,
        nullable=True,
    ),
    Column(
        "infra_petrochemicals_and_plastics_proposed_facility_count",
        Integer,
        nullable=True,
    ),
    Column(
        "infra_petrochemicals_and_plastics_proposed_nox_tonnes_per_year",
        Float,
        nullable=True,
    ),
    Column(
        "infra_petrochemicals_and_plastics_proposed_pm2_5_tonnes_per_yea",
        Float,
        nullable=True,
    ),
    Column(
        "infra_synthetic_fertilizers_proposed_co2e_tonnes_per_year",
        Float,
        nullable=True,
    ),
    Column("infra_synthetic_fertilizers_proposed_facility_count", Integer),
    Column("infra_synthetic_fertilizers_proposed_nox_tonnes_per_year", Float),
    Column(
        "infra_synthetic_fertilizers_proposed_pm2_5_tonnes_per_year",
        Float,
        nullable=True,
    ),
    Column("ordinance", String),
    Column("ordinance_earliest_year_mentioned", Float),
    Column("ordinance_jurisdiction_name", String),
    Column("ordinance_jurisdiction_type", String),
    Column("state_permitting_text", String),
    Column("total_tracts", Integer),
    Column("justice40_dbcp_index", Float),
    Column("n_distinct_qualifying_tracts", Integer),
    Column("n_tracts_agriculture_loss_low_income_not_students", Integer),
    Column("n_tracts_asthma_low_income_not_students", Integer),
    Column("n_tracts_below_poverty_and_low_high_school", Integer),
    Column("n_tracts_below_poverty_line_less_than_high_school_islands", Integer),
    Column("n_tracts_building_loss_low_income_not_students", Integer),
    Column("n_tracts_diabetes_low_income_not_students", Integer),
    Column("n_tracts_diesel_particulates_low_income_not_students", Integer),
    Column("n_tracts_energy_burden_low_income_not_students", Integer),
    Column("n_tracts_hazardous_waste_proximity_low_income_not_students", Integer),
    Column("n_tracts_heart_disease_low_income_not_students", Integer),
    Column("n_tracts_housing_burden_low_income_not_students", Integer),
    Column("n_tracts_lead_paint_and_median_home_price_low_income_not_studen", Integer),
    Column("n_tracts_life_expectancy_low_income_not_students", Integer),
    Column("n_tracts_linguistic_isolation_and_low_high_school", Integer),
    Column("n_tracts_local_to_area_income_ratio_and_low_high_school", Integer),
    Column("n_tracts_local_to_area_income_ratio_less_than_high_school_islan", Integer),
    Column("n_tracts_pm2_5_low_income_not_students", Integer),
    Column("n_tracts_population_loss_low_income_not_students", Integer),
    Column("n_tracts_risk_management_plan_proximity_low_income_not_students", Integer),
    Column("n_tracts_superfund_proximity_low_income_not_students", Integer),
    Column("n_tracts_traffic_low_income_not_students", Integer),
    Column("n_tracts_unemployment_and_low_high_school", Integer),
    Column("n_tracts_unemployment_less_than_high_school_islands", Integer),
    Column("n_tracts_wastewater_low_income_not_students", Integer),
    schema=schema,
)

existing_plants = Table(
    "existing_plants",
    metadata,
    Column("plant_id_eia", Integer, primary_key=True),
    Column("resource", String, nullable=False),
    Column("max_operating_date", DateTime),
    Column("capacity_mw", Float, nullable=False),
    Column("co2e_tonnes_per_year", Float),
    Column("state_id_fips", String),
    Column("county_id_fips", String),
    Column("state", String),
    Column("county", String),
    schema=schema,
)

fossil_infrastructure_projects = Table(
    "fossil_infrastructure_projects",
    metadata,
    Column("project_id", Integer, primary_key=True),
    Column("project_name", String, nullable=False),
    Column("state", String),
    Column("county", String),
    Column("county_id_fips", String),
    Column("state_id_fips", String),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("raw_street_address", String),
    Column("air_construction_id", Float),
    Column("facility_id", Integer),
    Column("facility_name", String),
    Column("project_classification", String),
    Column("industry_sector", String, nullable=False),
    Column("raw_project_type", String, nullable=False),
    Column("project_description", String),
    Column("facility_description", String),
    Column("permit_description", String),
    Column("cost_millions", Integer),
    Column("raw_number_of_jobs_promised", String),
    Column("date_modified", DateTime),
    Column("co2e_tonnes_per_year", Float),
    Column("voc_tonnes_per_year", Float),
    Column("so2_tonnes_per_year", Float),
    Column("nox_tonnes_per_year", Float),
    Column("co_tonnes_per_year", Float),
    Column("pm2_5_tonnes_per_year", Float),
    Column("total_wetlands_affected_permanently_acres", Float),
    Column("total_wetlands_affected_temporarily_acres", String),
    Column("raw_estimated_population_within_3_miles", Integer),
    Column("raw_percent_low_income_within_3_miles", Float),
    Column("raw_percent_people_of_color_within_3_miles", Float),
    Column("raw_respiratory_hazard_index_within_3_miles", Float),
    Column("raw_relative_cancer_risk_per_million_within_3_miles", Float),
    Column("raw_wastewater_discharge_indicator", Float),
    Column("is_ally_target", String, nullable=False),
    schema=schema,
)

iso_projects_wide_format = Table(
    "iso_projects_wide_format",
    metadata,
    Column("project_id", Integer, primary_key=True),
    Column("project_name", String),
    Column("iso_region", String, nullable=False),
    Column("entity", String, nullable=False),
    Column("utility", String),
    Column("developer", String),
    Column("state", String),
    Column("county", String),
    Column("state_id_fips", String),
    Column("county_id_fips", String),
    Column("resource_class", String),
    Column("is_hybrid", Boolean, nullable=False),
    Column("generation_type_1", String),
    Column("generation_capacity_mw_1", Float),
    Column("generation_type_2", String),
    Column("generation_capacity_mw_2", Float),
    Column("storage_type", String),
    Column("storage_capacity_mw", Float),
    Column("co2e_tonnes_per_year", Float, nullable=False),
    Column("date_entered_queue", DateTime),
    Column("date_proposed_online", DateTime),
    Column("interconnection_status", String, nullable=False),
    Column("point_of_interconnection", String),
    Column("queue_status", String, nullable=False),
    Column("has_ordinance", Boolean, nullable=False),
    Column("ordinance_jurisdiction_name", String),
    Column("ordinance_jurisdiction_type", String),
    Column("ordinance_earliest_year_mentioned", Integer),
    Column("ordinance", String),
    Column("state_permitting_type", String),
    schema=schema,
)
iso_projects_long_format = Table(
    "iso_projects_long_format",
    metadata,
    Column("state", String),
    Column("county", String),
    Column("project_id", Integer, primary_key=True),
    Column("date_proposed_online", DateTime),
    Column("developer", String),
    Column("entity", String, nullable=False),
    Column("interconnection_status", String, nullable=False),
    Column("point_of_interconnection", String),
    Column("project_name", String),
    Column("date_entered_queue", DateTime),
    Column("queue_status", String, nullable=False),
    Column("iso_region", String, nullable=False),
    Column("utility", String),
    Column("capacity_mw", Float),
    Column("resource_clean", String, primary_key=True),
    Column("state_id_fips", String),
    Column("county_id_fips", String),
    Column("state_permitting_type", String),
    Column("co2e_tonnes_per_year", Float),
    Column("ordinance_earliest_year_mentioned", Float),
    Column("ordinance_jurisdiction_name", String),
    Column("ordinance_jurisdiction_type", String),
    Column("ordinance", String),
    Column("has_ordinance", Boolean, nullable=False),
    Column("is_hybrid", Boolean, nullable=False),
    Column("resource_class", String),
    schema=schema,
)

proposed_power_dash_existing_plants = Table(
    "proposed_power_dash_existing_plants",
    metadata,
    Column("state", String),
    Column("county", String),
    Column("state_id_fips", String),
    Column(
        "county_id_fips", String
    ),  # Should be a part of the primary key, 9 records with missing count info
    Column("resource", String, nullable=False),  # Should be a part of the primary key
    Column("capacity_mw", Float, nullable=False),
    Column("permitting_type", String),
    Column("has_ordinance", Boolean, nullable=False),
    schema=schema,
)

proposed_power_dash_proposed_plants = Table(
    "proposed_power_dash_proposed_plants",
    metadata,
    Column("state", String),
    Column("county", String),
    Column("state_id_fips", String),
    Column(
        "county_id_fips", String
    ),  # Should be a part of the primary key, 9 records with missing count info
    Column(
        "resource", String
    ),  # Should be a part of the primary key, 9 records missing resource info
    Column("capacity_mw", Float),
    Column("project_count", Integer, nullable=False),
    Column("permitting_type", String),
    Column("has_ordinance", Boolean, nullable=False),
    schema=schema,
)

proposed_power_dash_local_opp = Table(
    "proposed_power_dash_local_opp",
    metadata,
    Column("county_id_fips", String, primary_key=True),
    Column("ordinance_earliest_year_mentioned", Integer),
    Column("ordinance_jurisdiction_name", String, nullable=False),
    Column("ordinance_jurisdiction_type", String, nullable=False),
    Column("ordinance", String, nullable=False),
    Column("has_ordinance", Boolean, nullable=False),
    Column("state_id_fips", String, nullable=False),
    Column("county", String, nullable=False),
    Column("state", String, nullable=False),
    Column("state_abbrev", String, nullable=False),
    Column("permitting_type", String),
    schema=schema,
)

co2_dashboard = Table(
    "co2_dashboard",
    metadata,
    Column("state", String),
    Column("county", String),
    Column("state_id_fips", String),
    Column("id", Integer),  # Should be a part of the pk but is missing one value :(
    Column("county_id_fips", String),
    Column("co2e_tonnes_per_year", Float),
    Column("facility_type", String, nullable=False),  # Should be a part of the pk
    schema=schema,
)

counties_long_format = Table(
    "counties_long_format",
    metadata,
    Column("state_id_fips", String, nullable=False),
    Column("county_id_fips", String, primary_key=True),
    Column("state", String, nullable=False),
    Column("county", String, nullable=False),
    Column("facility_type", String, primary_key=True),
    Column("resource_or_sector", String, primary_key=True),
    Column("status", String, primary_key=True),
    Column("facility_count", Integer, nullable=False),
    Column("capacity_mw", Float),
    Column("co2e_tonnes_per_year", Float),
    Column("pm2_5_tonnes_per_year", Float),
    Column("nox_tonnes_per_year", Float),
    Column("has_ordinance", Boolean, nullable=False),
    Column("ordinance_jurisdiction_name", String),
    Column("ordinance_jurisdiction_type", String),
    Column("ordinance", String),
    Column("ordinance_earliest_year_mentioned", Integer),
    Column("state_permitting_type", String),
    Column("state_permitting_text", String, nullable=False),
    Column("total_tracts", Integer),
    Column("justice40_dbcp_index", Float),
    Column("n_distinct_qualifying_tracts", Integer),
    Column("n_tracts_agriculture_loss_low_income_not_students", Integer),
    Column("n_tracts_asthma_low_income_not_students", Integer),
    Column("n_tracts_below_poverty_and_low_high_school", Integer),
    Column("n_tracts_below_poverty_line_less_than_high_school_islands", Integer),
    Column("n_tracts_building_loss_low_income_not_students", Integer),
    Column("n_tracts_diabetes_low_income_not_students", Integer),
    Column("n_tracts_diesel_particulates_low_income_not_students", Integer),
    Column("n_tracts_energy_burden_low_income_not_students", Integer),
    Column("n_tracts_hazardous_waste_proximity_low_income_not_students", Integer),
    Column("n_tracts_heart_disease_low_income_not_students", Integer),
    Column("n_tracts_housing_burden_low_income_not_students", Integer),
    Column("n_tracts_lead_paint_and_median_home_price_low_income_not_studen", Integer),
    Column("n_tracts_life_expectancy_low_income_not_students", Integer),
    Column("n_tracts_linguistic_isolation_and_low_high_school", Integer),
    Column("n_tracts_local_to_area_income_ratio_and_low_high_school", Integer),
    Column("n_tracts_local_to_area_income_ratio_less_than_high_school_islan", Integer),
    Column("n_tracts_pm2_5_low_income_not_students", Integer),
    Column("n_tracts_population_loss_low_income_not_students", Integer),
    Column("n_tracts_risk_management_plan_proximity_low_income_not_students", Integer),
    Column("n_tracts_superfund_proximity_low_income_not_students", Integer),
    Column("n_tracts_traffic_low_income_not_students", Integer),
    Column("n_tracts_unemployment_and_low_high_school", Integer),
    Column("n_tracts_unemployment_less_than_high_school_islands", Integer),
    Column("n_tracts_wastewater_low_income_not_students", Integer),
    schema=schema,
)