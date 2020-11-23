### Output description

1. `./output/stops.csv`

| Column Name    | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| STOP_ID        | ID for this stop                                             |
| STOP_NAME      | Name for this stop                                           |
| TOWN           | Name of the town this stop is located in                     |
| TRACT_ID       | ID for the tract this stop is located in                     |
| income         | Median income for this tract                                 |
| income_level   | income level for this tract, from 0-4, and -1 means missing value |
| route_ids      | IDs for the routes that go through this stop                 |
| ridership      | Average ridership for this stop for routes, in the order of `route_ids` |
| revenues       | Annual revenues for this stop for routes, in the order of `route_ids` |
| revenue_annual | Total annual revenue for this stop (sum of values in `revenues`) |

2. `./output/stops_weighed.csv` (`./output/shapefile/stops.shp` is the shapefile version of it)

| Column Name      | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| STOP_ID          | ID for this stop                                             |
| location         | geometry Point of this stop                                  |
| geometry         | geometry Polygon of the 0.5 mile radius circle               |
| impacted_tractid | ID for tracts that intercept the circle                      |
| proportion       | proportion of area/population of the impacted tracts         |
| income           | weighed income based on proportion                           |
| income_level     | income level for this tract, from 0-4, and -1 means missing value |
| impacted_pop     | weighted population impacted based on proportion             |

