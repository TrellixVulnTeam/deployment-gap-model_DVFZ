# iso\_projects\_long\_format

This table gives insight into proposed ISO projects by type. Each row represents a combination of project\_id/resource\_clean with other information joined on for convenience (county, ordinance, and project information). The data source is primarily the LBNL compiled ISO queues, plus local ordinances (via Columbia), state wind permitting types (via NCSL), and standard state/county IDs (from the Census). The last sheet of the raw ISO data contains a list of columns and their definitions for comparison to this table.

## Column Descriptions

**Unique Key Column(s):** (`project_id`, `resource_clean`)

|Subject|Column|Description|Source|Notes|
|----|----|----|----|----|
|Identifiers|`project_id`|A unique ID assigned to each project.|derived||
||`resource_clean`|Fuel type|LBNL||
|Location|`state`|US State name|Census||
||`county`|County name|Census||
||`state_id_fips`|State FIPS ID|Census||
||`county_id_fips`|County FIPS ID|Census||
|Properties|`project_name`|Name of the project|LBNL||
||`is_hybrid`|True/False indicator of whether the project has both generation and storage|derived from LBNL||
||`resource_class`|Renewable, fossil, or storage|derived from LBNL||
||`iso_region`|Name of the ISO region containing the project. Non-ISO projects are categorized as either Northwest or Southeast by LBNL|LBNL||
||`entity`|Similar to iso_region, but non-ISO projects are identified by utility|LBNL||
||`utility`|The utility within which the project will operate.|LBNL||
||`interconnection_status`|LBNL's status category for the interconnection agreement ("not started", "in progress", "IA executed")|LBNL||
||`point_of_interconnection`|The name of the substation where the plant connects to the grid|LBNL||
||`developer`|The name of the project developer.|LBNL|mostly missing|
||`queue_status`|These project have already been filtered to proposed projects, so this column is all "active".|LBNL||
|Dates|`date_proposed_online`|The date the developer expects the project to be completed.|LBNL||
||`date_entered_queue`|The date the project entered the ISO queue.|LBNL||
|Technical|`capacity_mw`|Export capacity of the generator or storage facility, in megawatts|LBNL||
||`co2e_tonnes_per_year`|Estimate of annual equivalent CO2 emissions of proposed gas plants, in metric tonnes.|derived from LBNL||
|Regulatory|`ordinance`|Summary text of the local ordinances in the given county, if any.|RELDI||
||`has_ordinance`|True/false indicator of the presence of any local ordinances in the county.|derived from RELDI||
||`ordinance_earliest_year_mentioned`|Approximate year the local ordinance was enacted. This was automatically extracted from the ordinance text so is not perfectly accurate.|derived from RELDI||
||`ordinance_jurisdiction_name`|Name of the jurisdiction with a local ordinance. This is usually a county or town within that county. "multiple" if more than one jurisdiction within the county has an ordinance.|RELDI||
||`ordinance_jurisdiction_type`|Category of jurisdiction: county, town, or city. "multiple" if more than one jurisdiction type within the county has an ordinance.|derived from RELDI||
||`state_permitting_text`|Summary text of the wind permitting rules of the given state.|NCSL||
||`state_permitting_type`|Category of the state's wind permitting jurisdiction: state, local, or hybrid.|NCSL||

## Modeling Decisions

### Definition of “Hybrid”

Currently any project with more than one resource\_clean is classified as “hybrid”, even if the second resource is a second source of generation rather than storage. So a combined wind/solar plant, or solar/gas plant, as well as solar/battery plant, will all have values of True in the is\_hybrid column.

### Omitted Columns

The following raw ISO columns were not included in this table:

* queue\_id – it is not quite unique and all NYISO withdrawn projects (several hundred) are missing this value
* queue\_year – it already exists in queue\_date, which is included
* proposed\_on\_year – it already exists in date\_proposed, which is included
* ia\_status\_raw – interconnection\_status\_lbnl (called ia\_status\_clean in the raw data) is standardized and easier to interpret
* withdrawn\_year – it already exists in withdrawn\_date, which is included
* on\_year – it already exists in date\_operational, which is included

NCSL columns:

* link – A link to state legislation. Too detailed.

Columbia Local Opposition:

* latest\_year\_mentioned – an additional metric to help estimate the year an ordinance was enacted. I thought one metric plus the actual description was enough
* n\_years\_mentioned – an additional metric to help estimate the year an ordinance was enacted. I thought one metric plus the actual description was enough

### Multiple Project Counties

A few (26 out of 5283, 0.5% as of the 2020 data) active ISO projects are associated with multiple counties. I don’t know if this is because they cross county lines or because the developer attempts to account for spatial contingency or something else. But due to the small number, I have so far simply ignored all but the first listed county.

### Hybrid Projects with a Single Capacity Value

Half (442 out of 868, 51% as of the 2020 data) of hybrid projects in the active ISO queue report only a single capacity value. So far we have not made any attempt to model the missing values, so the empty value remains empty and does not contribute to any aggregates for its resource type. I don’t know if the single capacity value is supposed to be a combined capacity, the larger of the two capacities, only generation capacity, or something else. The dominant hybrid configuration (91%) is solar + battery.

### Local Ordinance Resolution Mismatch

ISO projects are only geolocated by state/county. Local ordinances can be either at the county level (60 out of 103, 58% as of the 2020 data) or some smaller jurisdiction like a town (43/103, 42%). Without more precise ISO project locations, we don’t know if the ordinance directly effects the project. So far we have taken the conservative approach and assumed that if a project and ordinance share the same county, they are related.

The maps in Tableau also reflect this conservative assumption. A more accurate map would require shapefiles of city/town jurisdictions, which is entirely doable but was deemed low priority.

Furthermore, there are 6 state-level laws affecting RE siting in some capacity, but these laws are not included in the scope of local ordinances. The law in NY is pro-RE and the law in ME was repealed. The law in OH simply adds a level of veto power to county jurisdictions. Laws in KS, OR, and CT restrict development on certain types of land; their severity can only be assessed by an expert.

### CO2e Estimates

We estimated annual CO2e production for proposed gas and coal plants. See the page on CO2 estimation for details:

{% content-ref url="../co2-estimation.md" %}
[co2-estimation.md](../co2-estimation.md)
{% endcontent-ref %}
