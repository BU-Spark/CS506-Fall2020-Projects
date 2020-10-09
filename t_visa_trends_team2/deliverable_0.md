# Trends in T-Visa Applications.
## Team 2: Yizhou Mao, Zixuan Jiang, Heriberto Varela.
### Motivation:
There has been an increase in denials in T-Visa applications (there are 5,000 available per year). Never have more than 1,000 been granted in a year and the past few years have seen both an increase in applications and an increase in denials. There is a hypothesis that the increase in denials is related to procedural barriers that immigration is constructing to make it more difficult to for applications to find success.

### Project goal:
Categorize and analyze all relevant data to understand trends within the decisions, by analyzing the presence of specific keywords within the texts and to conduct topic modeling.

### Datasets: 
https://www.uscis.gov/administrative-appeals/aao-decisions/aao-non-precedent-decisions, 
https://www.justice.gov/eoir/dhs-aao-ins-decisions

## Methodology:
For scraping -Scrapy, Selenium webdriver, and/or Beautiful soup to download the 990 forms, the APIs should allow for easy information retrieval otherwise. For cleaning and preprocessing use Pandas to organize the dataset into dataframes for faster computation. Need to use NLP to preprocess the text and find the words indicating decision. Data visualization libraries such as Matplotlib, Seaborn, and Bokeh (interactive web-integratable visualizations) to display the financial information between black and other nonprofits.

### Analysis:
- Divide all decisions into *precedent* and *non-precedent*, by year. These will be the two main categories. 
- Further categorize them into *appeals* and *motions to reopen and reconsider*. These will not include derivative applications.
- The last categorization of the decisions will be into *dismissals* and *granted* requests. At these categories, further language analysis will be done to find patterns in the decisions. 
