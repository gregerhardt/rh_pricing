Scripts and associated files to process Chicago TNP data for use in Ride-Hailing Pricing Model.

/data - This folder is ignored by git, so you will need to put the files needed to run the scripts here manually.  This includes the following files:

- june06vot_v2.csv - An extract of one day of ride-hailing trips in Chicago.  The file comes from the [Chicago Transportation Network Provider Dataset](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips-2023-2024-/n26f-ihde/about_data) for June 6, 2023.  It has been appended to assign each trip a value of time, which is assigned based on the percentage of low vs high income households in the trip pickups location's Census Tract.  Zhihua Jin can provide additional details on any processing.  (Are these 2020 Census tracts?  Check!)

- Transportation_Network_Providers_Trips_(<Vintage>)_<date>.csv - The Chicago TNP data downloaded directly from their servers for a specific date.  

/out - Scripts will write all outputs here.  Ignored by git.  
