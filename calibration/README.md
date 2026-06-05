Scripts and associated files to create calibration targets and to calibrate a simple mode choice model.

/data - This folder is ignored by git, so you will need to put the files needed to run the scripts here manually.  This includes the following files:

- june06vot_v2.csv - An extract of one day of ride-hailing trips in Chicago.  The file comes from the [Chicago Transportation Network Provider Dataset](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips-2023-2024-/n26f-ihde/about_data) for June 6, 2023.  It has been appended to assign each trip a value of time, which is assigned based on the percentage of low vs high income households in the trip pickups location's Census Tract.  Zhihua Jin can provide additional details on any processing.  (Are these 2020 Census tracts?  Check!)

- trip_linked_2024.csv - Linked trip file from Phase 1 of the [CMAP 2024-2025 household travel survey](https://www.arcgis.com/home/item.html?id=2e0719dce2c34eeea81039eca35def80).  

- tract_2020_district.csv - equivalency between 2020 Census tracts and RH_Zone.  Must include GEOID as the Census tract ID and RH_Zone as the 2020 TNP Pricing Zone -- Downtown, Tourist, Airport, Other or External.  External is outside the City of Chicago. 

- times-0.0.1-car-2020-tract-17-0.parquet - Car travel times between Census tracts in Illinois.  Downloaded from https://opentimes.org/ 

/docs - various documentation that may be useful.  

/out - Scripts will write all outputs here.  Ignored by git.  
