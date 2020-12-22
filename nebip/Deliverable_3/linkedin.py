from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
from linkedin_scraper import Person


browser = webdriver.Chrome()

#Open login page
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
# the searches
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

name_comp = "Teri Williams OneUnited Bank"
url = build_url(name_comp)
browser.get(url)



# Rather than doing the scraping ourselves, let the library do the work
# We just need to get the link to the profile, which should be a href link
# in the html.
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')

# Use BeautifulSoup to get the linkedin profile link (may not work)
# Need some more testing to make sure it works consistently
link = soup.find('a', {'class': 'app-aware-link ember-view search-result__result-link'}).get('href')
print(link)

# Using the linkedin_scraper api to do the scraping
linkedin_person = Person(link, driver=browser,scrape=False)
linkedin_person.scrape(close_on_complete=False)
print(linkedin_person)


# testing keyword search
# keyword search works, need to convery linkedin_person
# into a string, and keyword search is case sensitive
# so must convert entire scraped profile and keywords into lower case
profile = str(linkedin_person).lower()
if ("black" in profile):
    print("keyword search works")
else:
    print("does not work")



# For a list of people use a dictionary with name + company as key and
# profile results as value
# Wrap the code in lines 54 - 74 into a loop when there are multiple results
# Set up to do a more pipelined version

# members_dict = {}
# file = "file of all names and company of board members"
# for person in file:
#     url = build_url(person)
#     browser.get(url)

#     src = browser.page_source
#     soup = BeautifulSoup(src, 'lxml')
#     profile_link = soup.find('a', {'class': 'app-aware-link ember-view search-result__result-link'}).get('href')

#     scraping = Person(link, driver=browser,scrape=False)
#     scraping.scrape(close_on_complete=False)

#     members_dict[person] = str(scraping).lower()