# Trends in T-Visa Applications.
## Team 2: Yizhou Mao, Zixuan Jiang, Heriberto Varela.
### Motivation:
The Boston University School of Law Immigrants’ Rights and Human Trafficking Program helps students learn practical legal skills while providing pro bono representation to vulnerable non-citizens facing deportation and survivors of human trafficking. In addition to pro bono legal representation, students and Program faculty work to increase protections available to vulnerable populations and contribute to the national policy landscape by providing new models that address emerging challenges in the immigrants’ rights and human trafficking contexts.

Members of the Program have noticed that there has been an increase in denials in T-Visa applications (there are 5,000 available per year). Never have more than 1,000 been granted in a year and the past few years have seen both an increase in applications and an increase in denials. Thus, they come up with a hypothesis that the increase in denials is related to procedural barriers that immigration is constructing to make it more difficult for applications to find success.

### Project goal:
The goal of this project is to test the hypothesis and answer questions related:
  1. How many cases were decided?
  2. How many cases were dismissed?
  3. How many cases were granted?
  4. What grounds were cases denied?
  5. How has this changed over time?
  6. Any patterns that can help predict?
  7. The distriubtion of each visa applier based on different category (race, sex, age, original nationality etc.)

### Datasets: 
[AAO Non-Precedent Decisions](https://www.uscis.gov/administrative-appeals/aao-decisions/aao-non-precedent-decisions)

## Methodology:
Package Usage:
  1. Scrapy, Selenium webdriver, and/or Beautiful soup will be used for scraping the pdfs on the websites. Related APIs will also be used if present.
  2. Regular Expression and urllib2 packages will be used to organize the scraped pdfs by year or month.
  3. Python packages like pdfreader will be used to convert the pdfs into text files, which are easier for analysis.
  4. NLP packages will be used to preprocess the text and find the words indicating decision.
  5. Pandas will be used to clean and preprocess the data and organize the dataset into dataframes for faster computation.
  6. Data visualization libraries such as Matplotlib, Seaborn, and Bokeh (interactive web-integratable visualizations) will be used to display the financial information between black and other nonprofits.

Analysis Methods(High Level):
  1. Divide all *non-precedent* decisions, by year, and then by appeals and motions to reopen and reconsider. These will not include derivative applications.
  2. Categorize the decisions into *dismissals* and *granted* requests. 
  3. Analyze prevalence of keywords/phrases specified in the decisions of the applications to find patterns.  
  
## Conclusion:
  A dataset containing all non-precedent and precedent decision cases should be obtained at the end of the project. The pattern or the trend of the T-Visa Applications should be concluded by analyzing the dataset collected to test the validity of the hypothesis that the increase in denials is related to procedural barriers that immigration is constructing to make it more difficult for applications to find success. If time allows, a website demonstrating the information collected and the pattern or the trend concluded can be built to help people understand more about the issue, which achieves the goal of the Boston University School of Law Immigrants’ Rights and Human Trafficking Program.
