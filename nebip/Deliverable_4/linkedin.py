""" This is a program that scrapes LinkedIn profiles.
    It uses a combination of Beautiful Soup to access html fields 
    and extract the contents, and a python library linkedin web
    scraper. The documention of the linkedin_scraper is the following:
    https://pypi.org/project/linkedin-scraper/

    The article on how Beautiful Soup is used is below:
    https://levelup.gitconnected.com/linkedin-scrapper-a3e6790099b5

    For more details about how the program worked please go to
    the Setup section and the Web Scaper section labeled below.
    
    The Setup section as the name suggests set ups the web scraper by
    logging in and dealing with certain parts of LinkedIn that may 
    prevent the actual scraping from working. It also includes a helper
    function that helps the search process.
    
    The Testing/Experimenting section is commented out, but it should
    offer good intuition of how each component works individually. 
    
    The Web Scraper section is just combining each part of the Testing/
    Experimenting section into a single cohesive program. 
"""


# Import the required libraries
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
from linkedin_scraper import Person
import pandas as pd


#################################################### Setup ################################################################
""" Declare the webdriver
    Users should deal with this on their own by downloading
    the desired webdriver (in this case Chrome) and
    setting the correct paths. Setting path is crucial
    for this to work, otherwise the webdriver will not be recognized
"""
browser = webdriver.Chrome()

""" Grabs the LinkedIn login page and the corresponding username
    and password fields and filling them in with the user's 
    log-in information
"""
# Open login page
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

#Enter login info:
elementID = browser.find_element_by_id('username')
username = ""
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
password = ""
elementID.send_keys(password)

elementID.submit()


# Gets rid of the pop up chat window in case it does something weird with
# the searches and accessing html classes
try:
    if browser.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
    	pass
except NoSuchElementException:
    try:
        if browser.find_element_by_class_name('msg-overlay-bubble-header') is not None:
        	browser.find_element_by_class_name('msg-overlay-bubble-header').click()
    except NoSuchElementException:
    	pass

# Gives it some time to process
time.sleep(2)


# Manually search person by building the url needed
# Build search
def build_url(search):
    url = "https://www.linkedin.com/search/results/all/?keywords="
    search = search.split()

    for w in range(len(search)):
        if (w != len(search) - 1):
            url = url + search[w] + "%20"
        else:
            url = url + search[w] + "&origin=GLOBAL_SEARCH_HEADER"
    return url


#################################################### Testing/Experimenting ################################################################
""" The following pieces of commented code are used for
    testing/experimenting purposes. They help walk through each
    part of the web scraping process and shows how this program
    works bit by bit. 
"""
# name_comp = "Herby Duverne"
# url = build_url(name_comp)
# browser.get(url)



# # Rather than doing the scraping ourselves, let the library do the work
# # We just need to get the link to the profile, which should be a href link
# # in the html.
# src = browser.page_source
# soup = BeautifulSoup(src, 'lxml')

# # Use BeautifulSoup to get the linkedin profile link (may not work)
# # Need some more testing to make sure it works consistently
# link = soup.find('a', {'class': 'app-aware-link ember-view search-result__result-link'}).get('href')
# print(link)

# # Using the linkedin_scraper api to do the scraping
# linkedin_person = Person(link, driver=browser,scrape=False)
# linkedin_person.scrape(close_on_complete=False)
# print(linkedin_person)


# # testing keyword search
# # keyword search works, need to convery linkedin_person
# # into a string, and keyword search is case sensitive
# # so must convert entire scraped profile and keywords into lower case
# profile = str(linkedin_person).lower()
# if ("black" in profile):
#     print("keyword search works")
# else:
#     print("does not work")


################################################# Web Scraper ###################################################################
""" The following code is the entire actual program that web scrapes LinkedIn after login.
    The program will take a xlsx file and extract the desired fields (name and/or company) and
    uses those as the search field to build a search url using the build_url function. 
    NOTE: If your input is CSV, please alter the code appropriately

    Once the url is built, the web scraper will access that search page and grab the top
    result's href link to the profile. It will then access the profile page and scrape the
    entire page for profile content. This will be done to all the names in the CSV file, and
    after scraping an individual the program will cross-reference the list of keywords with
    the scraped results. If a keyword is in the result, it will keep track of the appearance
    and append it to a list. After cross-referencing all the keywords, the appearance list will
    be hashed into the dictionary with name as key and list as value.
"""
# List of keywords
keywords = ["alpha phi alpha", "alpha kappa alpha", "kappa alpha psi", "omega psi phi", 
            "delta sigma theta", "phi beta sigma", "zeta phi beta", "sigma gamma rho",
            "iota phi theta", "the links", "the links incorporated", "the boulé", "boulé",
            "jack and jill of america", "n.a.a.c.p", "naacp", "the urban league", "urban league",
            "national association of black accountants, inc.", "national association of black accountants",
            "national association of black accountants inc", "national association of black accountants, inc",
            "national association of black accountants inc.", "naba", "national black mba association",
            "nbmbaa", "hbcu", "boston, young black professionals", "boston young black professionals",
            "young black professionals", "ybp", "black networking groups", "black women", "black woman",
            "black men", "black man", "black enterprise", "national association of african americans in human resources",
            "naaahr", "new england blacks in philantropy", "black educators alliance of massachusetts",
            "national association of black social workers", "people of color in independent schools",
            "national society of black engineers", "national black nurses association",
            "student national medical association", "blacks in government", "black lawyers association",
            "national black law students association", "national forum for black public administrators",
            "national association of black journalists", "alabama a&m university", "alabama am university",
            "alabama state university", "bishop state community college", "gadsden state community college",
            "shelton state community college", "concordia college", "miles college", " oakwood university",
            "selma university", "stillman college","talladega college", "tuskegee university", 
            "university of arkansas at pine bluff", "arkansas baptist college", "philander smith college"
            "shorter college", "charles drew university of medicine and science", "delaware state university",
            "university of the district of columbia", "howard university", "florida a&m university", "florida am university",
            "bethune-cookman university", "bethune cookman university", "edward waters college", "florida memorial university",
            "albany state university", "fort valley state university", "savannah state university", 'clark atlanta university', 
            'interdenominational theological center', 'morehouse college', 'morris brown college', 'paine college', 'spelman college', 
            'kentucky state university', 'simmons college of kentucky', 'grambling state university', 'southern university and a&m college', 
            'southern university law center', 'southern university at new orleans', 'southern university at shreveport', 'dillard university', 
            'xavier university', 'bowie state university', 'coppin state university', 'morgan state university', 
            'university of maryland, eastern shore', 'alcorn state university', 'jackson state university', 'mississippi valley state university',
            'coahoma community college', 'hinds community college-utica', 'rust college', 'tougaloo college', 'harris-stowe state university', 
            'lincoln university of missouri', 'elizabeth city state university', 'fayetteville state university', 'north carolina a&t state university', 
            'north carolina central university', 'winston-salem state university', 'barber-scotia college', 'bennett college', 
            'johnson c. smith university', 'livingstone college', 'st. augustine’s college', 'shaw university', 'central state university', 
            'wilberforce university', 'langston university', 'cheyney university of pennsylvania', 'lincoln university', 'south carolina state university', 
            'denmark technical college', 'allen university', 'benedict college', 'claflin university', 'morris college', 'voorhees college', 
            'clinton junior college', 'tennessee state university', 'american baptist college', 'fisk university', 'knoxville college', 
            'lane college', 'lemoyne-owen college', 'meharry medical college', 'prairie view a&m university', 'texas southern university', 
            'st. philip’s college', 'huston-tillotson university', 'jarvis christian college', 'paul quinn college', 'southwestern christian college', 
            'texas college', 'wiley college', 'norfolk state university', 'virginia state university', 'hampton university', 'virginia union university', 
            'virginia university of lynchburg', 'bluefield state college', 'west virginia state university', 'university of the virgin islands']

# For a list of people use a dictionary with name as key and
# the list of appeared keywords as values.
members_dict = {}


""" The following is code to extract the features from an xlsx file.
    If you are using a CSV file, please alter the pandas read program
    appropriately as currently it only reads excel. Also alter the column
    names and file names appropriately when running the code
"""

# Use pandas to read the excel file
df = pd.read_excel("filename.xlsx",sheet_name=0)

# get rid of some empty lines
# There are empty lines separating each organization for our file, so
# this line of code gets rid of those lines based on the director names
# as we are more focused on director names
df = df[df['data__operations__officers_directors_key_employees__name'].notna()]

# isolate the organization name, and director names
# For our file, we had to manually change the organization name column
# as is only had one line with organization name as below:
# org name | director
#  na      | director
#  na      | director ...
# Therefore we had to go into the file itself and make the change
df = df[["data__summary__organization_name", "data__operations__officers_directors_key_employees__name"]]

# turn the columns into a list
# We ended up only using the name, because adding organization name
# narrowed the LinkedIn search too much too often and returned will no results
name_list = df["data__operations__officers_directors_key_employees__name"].tolist()
org_list = df["data__summary__organization_name"].tolist()
name_org = [x + " " + y for x,y in zip(name_list, org_list)]


# Do the LinkedIn web scrape
for person in name_list:
    url = build_url(person)
    browser.get(url)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    # some cases where there is no such class
    # mostly happens when the search didn't find a person with that name
    profile_link = soup.find('a', {'class': 'app-aware-link ember-view search-result__result-link'})
    if (profile_link is None):
        members_dict[person] = "None"
        continue
    
    # get the link
    profile_link = profile_link.get('href')

    # Need an exception block because sometimes when no search
    # results appear it was still able to get a link which gives
    # an error to the web scraper because there are no fields
    # it can extract
    try:
        # Must set the fields as empty list because otherwise each web scraped result
        # will just append to the previous results and by the end, you will just have
        # a really long and overlapping profile of everyone you have scraped
        scraping = Person(profile_link, about=[], experiences=[], educations=[], interests=[], accomplishments=[], driver=browser,scrape=False)
        scraping.scrape(close_on_complete=False)
        results = str(scraping).lower()


        # gives it some time to process
        time.sleep(1)

        # Create a list and for each keyword that is in the
        # scraped results, append it, and at the end add it
        # as the value with the name of the individual as the key
        dict_list = []
        for keyword in keywords:
            if (keyword in results):
                dict_list.append(keyword)
        members_dict[person] = dict_list
    except NoSuchElementException:
        members_dict[person] = "None"
        continue

# Prints the dictionary, but change to writing into a txt file, etc
print(members_dict)