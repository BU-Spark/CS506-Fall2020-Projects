### Output description

1. `./output/stops/stops.shp`
   `./output/stops.csv` is the same file saved as a csv

| Column Name    | Description                                                                                |
| -------------- | ------------------------------------------------------------------------------------------ |
| STOP_ID        | ID for each stop                                             							  |
| STOP_NAME      | Name for each stop                                           							  |
| TOWN           | Name of the town each stop is located in                     							  |
| impacted_g     | Geo IDs of all tracts that intersect with each stop's radius 							  |
| income         | Weighted average median household income for each stop      							  	  |
| income_level   | Income level assigned to each stop, from 0-4                 							  |
| impacted_p     | Weighted average impacted population for each stop           							  |
| route_ids      | IDs for the routes that each stop corresponds to             							  |
| geometry       | Coordinates for each stop using the EPSG:26986 CRS                                         |
| proportion     | Proportions of tracts that intersect with each stop's "circle", divided by area of tract   |
| proporti_1     | Proportions of tracts that intersect with each stop's "circle", divided by area of circle  |

2. `./output/weighted_route_info_FINAL.csv`

| Column Name      | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| route_id         | ID for each route                                            |
| level_0          | Count of income_level 0 stops along each route               |
| level_1          | Count of income_level 1 stops along each route               |
| total            | Sum of level_0 and level_1                                   |
| impacted_p       | Sum of impacted_p of all stops along each route              |

3. `./output/all_rep_data_FINAL.csv` - table is an outer join on the geometries of `./output/stops/stops.shp` and `./data/house2012/HOUSES2012_POLY.shp`

4. `./output/impacted_districts.csv`

| Column Name      | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| district         | Name for each district                                       |
| level_0          | Count of income_level 0 stops in each district               |
| level_1          | Count of income_level 1 stops in each district               |
| total            | Sum of level_0 and level_1                                   |
| rep              | The MA state representative for each district                |