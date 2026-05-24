
Scripts and associated files to create calibration targets and to calibrate a simple mode choice model.

/data - This folder is ignored by git, so you will need to put the files needed to run the scripts here manually.  This includes the following files:

- june06vot_v2.csv - An extract of one day of ride-hailing trips in Chicago.  The file comes from the [Chicago Transportation Network Provider Dataset](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips-2023-2024-/n26f-ihde/about_data) for June 6, 2023.  It has been appended to assign each trip a value of time, which is assigned based on the percentage of low vs high income households in the trip pickups location's Census Tract.  Zhihua Jin can provide additional details on any processing.  (Are these 2020 Census tracts?  Check!)

- trip_linked.csv - Linked trip file from Phase 1 of the [CMAP 2024-2025 household travel survey](https://www.arcgis.com/home/item.html?id=2e0719dce2c34eeea81039eca35def80).  

- tract_2020_place.csv - equivalency between 2020 Census tracts and place (city).  Must include GEOID as the Census tract ID and Place as the name of the city.  In creating this, I excluded O'Hare airport from Chicago.  Otherwise Chicago is right.  No guarantees on other cities.  


/docs - various documentation that may be useful.  

/out - Scripts will write all outputs here.  Ignored by git.  
