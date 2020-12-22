# Group members
Kelly Ruan, Curtin Mason, Justin Ching (team leader)

# Project description
The rising cost of public transportation has impacted the budgets of people of low income who heavily rely on public transportation. Representative Elugardo is interested in exploring the feasibility of expanding free bus lines in Massachusetts for both the MBTA and Regional Transit Authorities (RTA).

The objective of this project is to identify bus routes that most serve low income areas. We will accomplish this by first identifying all bus stops in Massachusetts serviced by the MBTA and regional bus authorities and then evaluating which stops and routes serve different income levels. The second part of the project will focus on the potential cost and benefit of establishing free bus lines based on ridership and fares.  

# Strategic questions to be answered:
## Question 1
What bus routes and stops, if made free, would most benefit low income riders in Massachusetts?
## Question 2 
Which towns (and districts)  would most benefit by a policy change to the fare change to these routes?

## Question 3
What would the cost be to the MBTA and regional transit authorities for each proposed bus route/ stop/ zones (based on ridership and fare costs)?

## Question 4
What would the cost be to make an entire regional transit area free and how would this compare? (note: the purpose of this would be to enable policymakers to calculate the cost from maintenance, fare management, etc. of a differentiated approach vs. a holistic approach)

# Datasets
## Transportation data
[RTA Bus Stops](https://geo-massdot.opendata.arcgis.com/datasets/rta-bus-stops/data)

[MBTA Bus Stops](https://docs.digital.mass.gov/dataset/massgis-data-mbta-rapid-transit)

[MBTA Fare Calculator](https://www.mbta.com/fares)

[RTA Fares](https://www.mass.gov/info-details/public-transportation-in-massachusetts#map-of-transit-authorities-in-massachusetts-)

## Income level data
[Income level](https://api.census.gov/data/2018/acs/acs5?get=B19013_001E&for=tract:*&in=state:25)

## Ridershop data
[Ridership](https://mbta-massdot.opendata.arcgis.com/datasets/mbta-bus-ridership-by-trip-season-route-line-and-stop)

# Approach
## Step One:
Create a spreadsheet of all the different bus stops/routes in Massachusetts including MBTA, RTA, and City/Town buses.

## Step Two:
Assign an income level to each stop based on the census tract data. In addition to the census data, we may use insurance API's to find income levels. 

## Step Three:
Determine average fare for each transit stop based on fares for the MTBA and RTA.

## Step Four:
Calculate bus ridership for each transit authority to better prioritize certain bus lines.

## Step Five:
Identify which bus routes, stops, or zones would have the most positive effect on low income riders if free. Identify the impact of free bus lines on certain towns by ranking stops based on income level weighed by traffic.

## Step Six:
Generate visualizations: TBD with client using software such as ArcGIS or tableau as a final deliverable along with the list data.

# Final Results
All code, data, and visualizations can be found [here](https://github.com/cumason123/transit-equity).

Please make sure to read the README.md in the linked github repo.
 
