import rocketreach
from linkedin_scraper import Person, actions
from selenium import webdriver

# Teri Williams - OneUnited Bank (No Teri Williams, but Teri Cohee) - id=3609442
# Farrah Belizaire - LiteWork Events (Doesn't show up when company included) - id=1259121
# Terryl Calloway - Calloway Graphix (2 Results with name and current employer, who?)
# Herby Duverne - Windwalker Group (Wrong Corp name - Windwalker Corporation, also accent on e)

# Finds the person through search
# Search and Lookup result documentation:
# https://github.com/rocketreach/rocketreach_python/blob/master/rocketreach/person.py
rr = rocketreach.Gateway(rocketreach.GatewayConfig('apikey'))

# # Code for Searches (does not return linkedin link)
s = rr.person.search().filter(name="")
result = s.execute()
for person in result.people:
    print(person)

# Code for lookups
f = open("info.txt","w")
result = rr.person.lookup(person_id=id)
if result.is_success:
	person = result.person
    f.write("ID: "+ person.id)
    f.write("Name: "+ person.name)
    f.write("Employer: "+ person.current_employer)
    f.write("LinkedIn: "+ person.linkedin_url)
    # linkedin_urls.append(person.linkedin_url)


# LinkedIn Scraper
driver = webdriver.Chrome()
linkedin_urls = ["https://www.linkedin.com/in/teri-williams-cohee-99811029"]
actions.login(driver, "username", "password")
linkedin_person = Person(linkedin_urls[0], driver=driver,scrape=False)
linkedin_person.scrape(close_on_complete=False)
print(linkedin_person)