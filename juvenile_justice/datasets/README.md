## Dataset Descriptions

NHGIS_pop_by_bg.csv: Population of each Census Block Group in Massachusetts; the AJWME001 column at the far right is what actually contains the population numbers

New Bedford Housing Locations.xlsx: listing of the New Bedford Housing Authority's public housing properties, including latitude and longitude

block_groups_nb.json: shapefiles at the Census Block Group level for New Bedford

blocks_nb.json: shapefiles at the Census Block level for New Bedford

census_tracts_nb.json: shapefiles at the Census Tract level for New Bedford

field_incident_reports: pickled (.pkl) version of the New Bedford dataset which includes geocoding data for each incident's location

field_incident_reports.csv: the main dataset for New Bedford


haverhill_school_incident_reports.csv: the main dataset for Haverhill

haverhill_school_incident_reports_uncleaned.csv: an early version of the Haverhill dataset, from before Dan cleaned up some inconsistencies in how we each recorded missing values

incident_points_nb.json: this is the last column of field_incident_reports, just chopped off for convenient future use -- it contains latitude and longitude information (stored in shapely.geometry.Point format) for each incident in New Bedford

nb_public_schools_final.csv: a listing of all public schools in New Bedford, including latitude and longitude

nibrs_2017.xlsx: listing of all arrests in Massachusetts in 2017 that comes from the FBI's National Incident-Based Reporting System

nibrs_2018.xlsx: similar information as in nibrs_2017.xlsx, but for 2018

springfield_arrest_logs.csv: the main dataset for Springfield

springfield_logs_with_geocoding: a pickled (.pkl) version of the Springfield dataset which includes geocoding data for each arrest with a street address that we could turn into a latitude and longitude

springfield_nibrs_merged.csv: the result of merging the Springfield arrest logs and the 2017 and 2018 NIBRS arrest records, only including exact matches; the merging logic is described in the springfield_merge_w_nibrs.py file in the ./analysis/datasets subfolder
