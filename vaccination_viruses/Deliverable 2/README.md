This file will cover all the labels/features in our dataset. 

States:

- This label simply represents each state within the USA. We are primarly be using state data. 
There are 50 states plus the District of Columbia (DC), which totals to 51 observations. Since
we're looking at state data, we found data and created this final dataset by merging the 
observations with the state name.

- This label represents the percentage of each state's population that has received the MMR
vaccine (measles, mumps, and rubella). The MMR vaccine is one of the most commonly 
recommended vaccines for individuals and is typically taken at a young age in two doses.
This vaccine is very commonly required by law for children to attend school. 2017 is the 
primarly vaccination rate that we used. We also used, however, others as well to gain 
additional insight into trends over the years.

2007

- Vaccination rates by state for 2007. 

2008

- Vaccination rates by state for 2008. 

2009

- Vaccination rates by state for 2009. 

2010

- Vaccination rates by state for 2010. 

2011

- Vaccination rates by state for 2011. 

2012

- Vaccination rates by state for 2012. 

2013

- Vaccination rates by state for 2013.

2014

- Vaccination rates by state for 2014.

2015

- Vaccination rates by state for 2015.

2016

- Vaccination rates by state for 2016.

2017

- Vaccination rates by state for 2017.

Exemption:

- This variable represents the exemptions that each state allows for all mandatory vaccines.
There are three types of exemptions: religious exemption, medical exemption only, and personal
belief exemptions. Religious and medical exemptions are self-explanatory. Personal belief 
exemptions are very broad and may overlap with other exemptions such as religious exemptions.
From strictest vaccination legislation to the most lax: medical exemptions only, religious
exemptions, personal relief exemptions.

Total Health Spending 

- This feature represents the total health spending that each state spends per year (represented
in millions of dollars). This includes “spending for all privately and publicly funded personal 
health care services and products (hospital care, physician services, nursing home care, 
prescription drugs, etc.) by state of residence. It should be noted, however, that we decided it
would be prudent to find the per capita since states have widely varying populations. Therefore, 
just examining the total health spending per state would fail to take into account that the
population may play a role (states with lower populations likely spend much less and vice versa).

Population

- Represents the population of each state. This feature can be used for a myriad of things. For 
example, it was used in conjunction with the "Total Health Spending" feature to find the total
health spending per capita in each state. 

spending_per_capita

- This feature represents the total health spending per capita for each state. This was a variable
that we created by dividing the "Total Health Spending" observations by the "Population" 
observations. This feature will give us more reliable readings on how much each state spends on
health by removing any skewing of the data that might affect "Total Health Spending" due to 
population size differences.

population_density

- Represents the number of people per square mile for each state. This feature may have multiple
uses. It provides insight into the geograph and demographics of different states.

Median_income

- Represents the median household income in per state. The values are indicated in dollars.

HighSchool_Plus

- Represents the percentage of residents in each state that have completed at least 
high school. This percentage also includes those who have completed studies after high school 
such as undergraduate degree (bachelor's).

Bachelor_Plus

-  Represents the percentage of residents in each state that have completed at least a 
bachelor's (undergraduate degree). This also includes those who have pursued further
education (postgraduate education, etc). 

spending_per_pupil

- Represents the amount of dollars spent per elementary and secondary (K-8) student by
state.