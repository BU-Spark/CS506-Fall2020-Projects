# Spark Project: Restaurants During Covid
Team Members: Ganghao Li, Zhou Shen, Zhenfei Yu, Kefan Zhang

## Background & Targets

As the Covid-19 attacked the world in 2020, the restaurants in Boston were struggling to survive this difficult time. The Mayor’s Office of Economic Development was looking for some conclusions about the restaurants during Covid, supported by solid data.

Main questions we are expected to answer are:

- How many businesses have permanently closed during Covid? How many are open? How many are temporarily closed? 
- How much activity is happening at different types of businesses by restaurant type (e.g. Italian vs. Thai vs. pizza, etc.), by neighborhood or zip code?? Do hours of operation seem to impact overall activity/ success?
- What has been the relative impact on government policies or assistance programs?

Mainly we are focusing on answering them with the data we fetched and tools we use on those data, but we may also analyze the data in many other different ways to come up with other useful conclusions.

## Resources (APIs & Datasets)

- Google Maps Places API
Google Maps Places API provides static data at the time when we started collecting information. It provides answers to below questions: location of restaurants, current business status of restaurants, whether restaurants are permanently closed, number of total ratings and ratings from users. To access it, we need to get a Google Maps Places API key.

- Safegraph
Safegraph provides data of Place foot-traffic and demographic aggregations that answer: how often people visit, where they came from, where else they go, and more. Available for ~3.6MM POI in the USA. To access it, we need to set up an AWS client and get an access key. 

- Active Food Establishment license dataset
The Health Division of the Department of Inspectional Services (ISD) creates and enforces food safety codes to protect public health. This dataset contains a list of restaurants that met the City’s standards to become licensed food service establishments.

## Code instruction

- Data preparation and clearing
Safegraph provides us data of monthly visits to all of the visiting places in the United States, so we first extracted data about Boston from it based on the city name column. Then we join what we get from safegraph with the active food license table, which generates the visiting information to Boston restaurants from January 2020 to September 2020.  
The nine datasets are the main sources that our observation and analysis is based on. Here is an example of January data, which includes columns like restaurant name, address, city, postal_code, raw_visit_counts and etc.




# Past Stage: [Deliverable 3](https://github.com/ec506-Spark-Team/CS506-Fall2020-Projects/blob/master/covid_food_business_team1/Documents/deliverable_3.pdf)

# Past Stage: [Deliverable 2](https://github.com/ec506-Spark-Team/CS506-Fall2020-Projects/blob/master/covid_food_business_team1/Documents/deliverable_2.pdf)

# Past Stage: [Deliverable 1](https://github.com/ec506-Spark-Team/CS506-Fall2020-Projects/blob/master/covid_food_business_team1/Documents/deliverable_1.pdf)
