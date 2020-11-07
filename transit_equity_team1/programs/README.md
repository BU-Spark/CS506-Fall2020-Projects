### Output description

1. "./output./stops.csv"

| Column Name    | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| STOP_ID        | ID for this stop                                             |
| STOP_NAME      | Name for this stop                                           |
| TOWN           | Name of the town this stop is located in                     |
| TRACT_ID       | ID for the tract this stop is located in                     |
| income         | Median income for this tract                                 |
| income_level   | income level for this tract, from 0-5, and -1 means missing value |
| route_ids      | IDs for the routes that go through this stop                 |
| ridership      | Average ridership for this stop for routes, in the order of `route_ids` |
| revenues       | Annual revenues for this stop for routes, in the order of `route_ids` |
| revenue_annual | Total annual revenue for this stop (sum of values in `revenues`) |

