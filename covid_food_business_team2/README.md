# CS506 Fall 2020 Final Projects--- Boston-Restaurants-During-Covid
Creat a database of resturants from various sources to understand how these businesses have been impacted by covid.

## Membership :
  - Li jingyi
  - Li Junwei
  - Pei Qingxuan (leader)
  - Hu Shiyang

## Project Deliverable 0 (Due on 2020/9/30)
  - Teams met with project client
  - Submitted project scope and  final project description
    1. Data souces
    2. Strategic question to be answered
    3. Step by step approach for cleaning data and answering strategic questions

    ### Project Scope
      This project is to create a consolidated database of restaurants by data source Google Place API, Yelp, GrubHub, Uber Eats, Safegraph, city of Boston. To understand how thses restaurants have been impacted by Covid-19. To understand the impact of various goverment policies and assistance program on the boston food business.There are four delivarables and the last deadline is 2020/12/09. 

    ### Data souces
      - [Yelp API ](https://www.yelp.com/developers/documentation/v3/event)
      - [Bing](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/)
      - [GrubHub](https://stevesie.com/apps/grubhub-api) 
      - [Uber Eats](https://www.ubereats.com/)
      -   [Google Place API](https://developers.google.com/places/web-service/details)
      - [Licenses (Alcohol)](https://data.boston.gov/dataset/liquor-licenses)
      - [City of Boston Certified Businesses](https://data.boston.gov/dataset/certified-business-directory/resource/3fc08ca2-9baf-4d77-b03a-aaed1cc936ed)
      - [FOOD ESTABLISHMENT INSPECTIONS](https://data.boston.gov/dataset/food-establishment-inspections)
      - [Licensing Board Licenses - Datasets](https://data.boston.gov/dataset/licensing-board-licenses)
      - [Active Food Establishment Licenses](https://data.boston.gov/dataset/active-food-establishment-licenses)
      
      
    ### Strategic Question
      1. How many restaurants have permanently closed during Covid-19 ?
      2. how many restaurants open ?
      3. How many are temporarily closed ? 
      4. How much activity is happening at different types of business by restaurant type?
      5.  what has been the relative impact on goverment policies?

## Project Deliverable 1  (Due on 2020/10/28)
  - All data should be collected.
  - Perform Preliminary analysis of the data.
  - Attempt to answer one relevant question in Strategic quenstion. 

    ### Data Collection   
    - [ ] Bing
    - [X] Boston Certified Business 
    - [X] Food Establishment Inspections
    - [X] Active Food Establishmen Licenses
    - [X] Licenses Alcohol 
    - [X] Licensing Board Licenses

    ### Data Analysis 
    seen in the data_Visualization folder
    ### Answer Question
    Based on the current datasets and analysis we can do, the above question can not be answered.<br>
    For the next sprint of the project,we will merge the data we collected and combined with the safegraph data using aws<br>
    At that time, we can do the further and deeper analysis, at least 3 questions will be answered.

## Project Deliverable 2
- All project questions should have been reviewed, answered, and submitted in a written document outlining findings as a PR. 
- You will also be asked to submit the associated data and a README explaining what each label/feature in your dataset represents.
- Your team should meet with the client before this deliverable.
  ### Question
  For the restaurants part like the number of closed restaurants or open resturants, we'd like to answer them after a fully analysis considering our analysis are inaccuarte enough at this moment. We have met the name problem because different datasets use different name for the same restruant which cause lots of repeated calculation.

  By analysing the data of popularity during last 7 months, we found that the populartiy Bosotn area is related to the reopening policies of the MA and Boston government.

  ### Data
  For the popularity of the resturants we still have trouble because of the differences between datasets. For the same restruant, the same resturant may have different name in diffferent datasets, so in our primary process, lots of resturants are recalculated, so we anlysis the polpularity based on post code which may partly reflects the impact on restruants in a specific neighborhood.

  The data was saved as json file, and the formant is postcode:{popularity}, the data was collected from Feb 2020 to Nov 2020.