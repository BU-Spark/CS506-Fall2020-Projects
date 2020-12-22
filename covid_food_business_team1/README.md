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

![img](https://lh4.googleusercontent.com/w8hCzd1X_i2oSxuje4bm3ZRHQnhga-iZlJ6wz_HLXknhc5ZMfPGPQhFEEKTuFIwnD8KwH_kfp6FV1VKvXwwppkksTxYGGR10TTevAjPT_wfuz_Hws-Erfu5aDyY90Q66yR3mrWGJ)

- HeatMap 
We also use the latitude, longitude and the raw visits from restaurants per month, in above filter safegraph DataFrame to illustrate this heatmap, which can reflect the popularity of the restaurants and variety of different regions.

![img](https://lh6.googleusercontent.com/WbIYBE68VgxA9JbNYhTmEhBFG7Av9aCxaNVugMZb403CADMqix5gOzR6-WAGX0gqmzlRtM77US3YgaiXE-I6E1Kp39yR18_ZPU1YBAUiJ8iadTtSjV3_5a4kClKrw8HvIT_JFYD0)

- Data analysis and visualization
We categorized data by different postcodes and different areas in Boston, and analyzed the relationship between monthly mean visits and different post codes, between monthly mean visits and time period.

## Data visualization
- Number of user reviews from top restaurants from Google Maps Places API

![This Figure shows that the number of user ratings is different among the restaurants, and the span is relatively large, the highest and lowest has 2,000 ratings gaps.
](https://lh4.googleusercontent.com/RWqH01jDWBC_JoJ3LGsb0gD2rofSq23Wb5LJVya8BZLIN3JwkT3erReLypUrcZeSe-T_J1BNuZtLirUePMx0CXMt7USKL30FtqouqFODKGLUTW5axe3-T3us9i6VDCMoQ6TfDTXZ)

This Figure shows that the number of user ratings is different among the restaurants, and the span is relatively large, the highest and lowest has 2,000 ratings gaps.

- Relationship between visits and different areas (by postal code/CITY/brand of restaurant)
By postal code
![img](https://lh5.googleusercontent.com/4TZjKsa7P-IZsIxBGxUnwDXj08KU1ESdPvCIIAVj6u_w5_DwUie7YUG_VCM4MBQr3fmcgiS2pVu6lJV7qtU18FO0_Uw8NEPGvVySwEw5RUkG2J2jDYbwwtWN1GhbwU__0B3CmR4w)

The X axis is the postal code, and the y axis is the raw visits take Logarithm operation (to display the graph as the better visual format).

This proves that restaurants in different postal codes have the different distribution of raw visits. We can see that  restaurants in 02115 have the highest and lowest visits, but most of them in this region are at relatively high visits.

By city

![img](https://lh3.googleusercontent.com/U0QWDVoPuHBoOwW4IMJmNSuuE70gE3kMP8CimuLCzjuqLFCLD5mMpEZj4-dyYqR7ZQRMX3qj1-1lmW6cOf8OpUjNjrNmLcT5b2a7VnqZjMluy5jXrv2exdGyszdhUhGa-9FFApSK)

The X axis means the name of the district and Y axis is the same as above.
This proves that most restaurants are centered in the Boston District, and most of the raw visits are from 16 ~ 256 per day. It strengthens the conclusion that different locations do impact the restaurant's visits.

By brands of restaurants

![img](https://lh5.googleusercontent.com/z9EU_WgkKEl-zzETUE4f3Dx-yM0V_cKx1yHdoQ6AWbjJZS15BuZZ3W-Z5bqGxjZs3lh_eKXAVwnjSz-zYBXRNl7jN4kWHpwDATruv_DIYpTXT7K_GvnpnwG-OCC8Od8r1y3sRxO3)

The X axis represents the brand of restaurants like Subway, Starbuck, Five guys and so on. It shows that different brands have different distributions of customer visits. Besides, it also displays that even restaurants are the same brand, their visits still vary a lot, which we can conclude from Subway, Ben & Jerry’s.

- Number of visits to different CITY/postal code in different months


By postal code

![img](https://lh6.googleusercontent.com/VVgv65UJjGJaBauC6QRZiSKe758l1pjglWWrPswXyCXeWKlDzW6mVh8lYvAk7fVBmE-rTrlyQ0O4dhe0J6U7YrM8ZBJ5m1YrchwLo0FEue2MR1po-vBUjD8rVQ2WRSbENTlZ1NxZ)

![img](https://lh6.googleusercontent.com/nEbDHwugfM3MJIP5nlPKAW_2WBCc8tSicfV7_KowblZ0aaX_4fEMa0nXfg8L7TQ7CKybDTOdpcseXKuTBs9UNGWQ7_f1TPMWDlFJOVsp3nO02X3fFt9ww7OpxHG8GYQyaEx58cLA)

![img](https://lh6.googleusercontent.com/5eiI8Xg8MrvvXoJDYjpvjrRdyDGngJ0XrWkaDb1Cn0PuiAhsfFe5IDj16F4sZh-ohq9mMI4WWuCQrPAPHdInCdce37Qrdmap2i4UFqQG333gkAP4bSVPCeUt1PVOoI-tZj3EAVVk)

These 3 graphs shows each postal code groups’ visits in January, April, and 
September. 



 

By CITY

![img](https://lh6.googleusercontent.com/WLR-huBwCrfOD8wIXqGPQvOsZNdEeee160fYCEmL6P6ThAobf5fa-sD2tGxonKITUTJxTnb_P4OHE-gnDTJTQbAW_340Oncx7rDyHUoZoVr2KXN4dTIlr2HOHipEYd_gzCPbxg9f)   

![img](https://lh6.googleusercontent.com/op3XIRB3k8GlA8dWro1JRBiO4KyrCZm_9B272xZQTs9-GNK25jJbXjery1Olg7ahO63aw1mCObKA79bOXLDqn6j4rm_-JSiowGaCJkK1eoogCTnwltPwlpqSK0xfUjsJx22PPMKG)    

Above 2 graphs show each postal code group's visits in January and April..
- Change of numbers of visits to different postal code/CITY
General Trend of all the restaurants

![img](https://lh4.googleusercontent.com/QOpnFYeWcxwyS7HocB6Wy17Nj0uvSsPr_Ko_apKyPSLdeoBnqROVoJWP5DnB-wyVTVRkbkRjBz1ZWebd9xfwieRsrxEz6s5tCyBbKEC7PDabiP6Rkgeg7y8Rs06bNs9VR9a3_d5o)

By different postal code

![img](https://lh3.googleusercontent.com/eHhHyHa809zoQx7lM6-WgIri25bg-JmjusV2lfUdfWUnG2K5Ys5aHOpgg9kXGgKQt-6bako4zK5PiPPSwB0wdUTPD2mU-I44c6NdnnsqEAocU-f9D91gfj3NQ5tAQDJlkKd994Ih)



![img](https://lh4.googleusercontent.com/lZLxDStzBEKa6Xmtw5LXnjgrWYB2hlK-FsomOEb8X4HIYsShODAJJ6n_CZgHTg6XVUUVxlQ6Vg9KLUUsVUVTZ4DZ2XH4U6scMnUk3r1UTlRqIjQ3zSi1OwIoFWH03jzsZpMBzNW0)


By CITY - Allston

![img](https://lh4.googleusercontent.com/ZmRIWZGBORJ5s_HI4wFiMgsoZzHz38Gw9iPT3iDAYkjRIeiVrRgZUzgXOxfiqKodVuxRGZECRZ1XXaAgTTZQZaxfw7nlWe-qZh5MNDE2F937ISdbLTNkOyqpM88ukYku6F_KLQ2W)

It proves that although the general trend reduced sharply and then increased slowly, but actually different location,different brand, the visits trend is not always the same as the general trend. Some of them will increase relatively more from April to September, and some will decrease in August while others still keep 
rising.
- Restaurants’ visits with Governments Support Policies      

![img](https://lh4.googleusercontent.com/LMk1TwDyqeSgg-jJf8-aHDwX3ORWAgmsm-HGCx7WLnY7t2wTT2qKIKW9G-gui9ta49bpPxq_Tyy7wbMkoP4g_eTThQrkdepB_4cmnBmYWWcVw6CNC9asUM__6jgclEOnV9j56Emk)      
This image shows the restaurants which receive the government support policies. We can see that in April, the visits reduce to the lowest at less than 40 visits / day. After these restaurants receive the support, their visits start to rise at stable speed.


## Conclusion
From the above data visualization, some conclusions are as follows.
- With the time changes, the total visits of all the restaurants reduce sharply from January to April, and then it increases slowly from April to September. That means firstly, each restaurant has suffered a lot from Covid-19, because people  gradually noticed the harm of Covid -19 and the Government also Strongly suggested citizens not go outside if not necessary. But after April, people started to be familiar with covid and were not as terrified as before, so they began to eat in the public areas, but the total visits is still at relatively low number
- Through the graph of relationship of visits and different areas (by postal code/CITY/brand of restaurant), we can see that the total visits amount and distribution is different according to above elements, which means the location, City Region, brand are also the key factors to the restaurants business.



## Limitations 
- We could not obtain the feature which can presents each restaurants’ operation hours, we found that feature of each restaurant is null
- Most Apis is not open-source and free, so there are few resources available from the third party apis
- Because the data format in each datasets is different, so after we merge the same item, there are only few elements left

## Roles and responsibilities of the team
**Ganghao Li:**
Mainly work on obtaining data from safegraph, data cleaning, visualization, heatmap and analysis, writing reports. 

**Zhou Shen:**
Mainly work on obtaining data from Google Maps Places API, visualization (relationship between visits and different components), analysis and completing reports. 

**Zhenfei Yu:**
Mainly work on data cleaning and filtering from safegraph and license dataset, visualization of covid impact on restaurants categorized by postcode, and writing reports.

**Kefan Zhang:**
Mainly work on obtaining data using Yelp API, exploiting government policy datasets (for example Reopen Boston Fund and Small Business Relief Fund), integrating them with datasets fetched from SafeGraph and find useful common tuples, merging useful columns, removing duplicates and so on.



# Past Stage: [Deliverable 3](https://github.com/ec506-Spark-Team/CS506-Fall2020-Projects/blob/master/covid_food_business_team1/Documents/deliverable_3.pdf)

# Past Stage: [Deliverable 2](https://github.com/ec506-Spark-Team/CS506-Fall2020-Projects/blob/master/covid_food_business_team1/Documents/deliverable_2.pdf)

# Past Stage: [Deliverable 1](https://github.com/ec506-Spark-Team/CS506-Fall2020-Projects/blob/master/covid_food_business_team1/Documents/deliverable_1.pdf)
