from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from typing import List
import pandas as pd
import re

def remove_html_tags(text: str) -> str:
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text))


def scrape_article_links(year: int) -> List[str]:
    """
    Scrape links of WBUR articles for a specified year
    param year: year for which WBUR articles will be scraped
    return: list of URLs
    """
    base_url = "https://www.wbur.org/news/archive"
    
    month_and_days = {"01": 31, "02":28, "03":31, "04":30, "05":31, "06":30,
                      "07": 31, "08":31, "09":30, "10":31, "11":30, "12":31}
    if year % 4 == 0:
        month_and_days["02"] = 29
    
    article_links = []
    
    for month in month_and_days:
        for day in range(1, month_and_days[month] + 1):
            
            if day < 10:
                day = f"0{day}"
                
            date = f"{year}/{month}/{day}"
            req = Request(f"{base_url}/{date}")
            html_page = urlopen(req)
            
            soup = BeautifulSoup(html_page, "lxml")
            
            links = []
            for link in soup.findAll('a'):
                links.append(link.get('href'))
                
            for link in links:
                if link != None and date in link:
                    article_links.append(link)
            
    article_links_set = set(article_links)
    article_links = list(article_links_set)
                    
    return article_links                    


def scrape_articles(urls: List[str]) -> List[str]:
    """
    Scrape contents of articles given the URLs
    param urls: list of urls
    param year: the year of the articles that will be scraped
    return: a list of articles
    """
    base_url = "https://www.wbur.org"
    articles = []
    
    for url in urls:
        url = f"{base_url}{url}"
        req = Request(url)
        html_page = urlopen(req)
        
        soup = BeautifulSoup(html_page, 'lxml')
        paragraphs = soup.find_all('p', class_="")
        
        if len(paragraphs) > 1:
            
            # Removing HTML tags from text
            clean_text = []
            for paragraph in paragraphs:
                clean_text.append(remove_html_tags(paragraph))
            
            if len(clean_text[0]) > 1:
                if "&" in clean_text[0][0]:
                    del clean_text[0]
            
            clean_str = ''.join(clean_text)
        
            articles.append(clean_str)
        
    return articles


def create_csv(articles: List[str], year: int) -> None:
    """
    Creates and saves a csv file containing a 
    single column for the scraped articles
    param articles: a list of articles
    return: None, saves the csv to disk
    """
    df = pd.DataFrame({
        'text': articles
    })
    
    df.to_csv(f"wbur{year}.csv")


article_links_2015 = scrape_article_links(2015)
print("Done")
articles_2015 = scrape_articles(article_links_2015)
create_csv(articles_2015, 2015)

#test_scrape = scrape_articles(["/news/2014/01/01/family-homelessness", "/news/2014/01/01/james-avery", "/news/2014/01/01/woman-killed-in-boston-drawbridge-accident"])
#test_csv = create_csv(test_scrape, 2014)

'''
# Opening the page of an article
req = Request("https://www.wbur.org/news/2014/07/14/casino-cash-communities")
html_page = urlopen(req)

# Parsing HTML
soup = BeautifulSoup(html_page, "lxml")

# Viewing the html
#print(soup.prettify())

# Saving all the paragraphs in a list
paragraphs = soup.find_all('p', class_="")

#print(paragraphs)

clean = []

for i in paragraphs:
    clean.append(remove_html_tags(i))

print(clean)

if "&" in clean[0][0]:
    del clean[0]

print(clean)
'''

'''
# Opening the archive page that contains links to the articles that were published on 01/01/2014
req = Request("https://www.wbur.org/news/archive/2014/01/01")
html_page = urlopen(req)

# Parsing the HTML
soup = BeautifulSoup(html_page, "lxml")

#print(soup.prettify())

# Getting all the links on the page
links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))



# Only getting the links that contain "2014/01/01" since these would be the article links 
for link in links:
    if link != None:
        if "2014/01/01" in link:
            print(link)

# Opening the page of an article
req = Request("https://www.wbur.org/news/2014/01/01/james-avery")
html_page = urlopen(req)

# Parsing HTML
soup = BeautifulSoup(html_page, "lxml")

# Viewing the html
#print(soup.prettify())

# Saving all the paragraphs in a list
paragraphs = soup.find_all('p', class_="")

# Deleting the last paragraph since it is not a part of the article
del paragraphs[-1]

# Removing HTML tags from each paragraph
clean = []

for i in paragraphs:
    clean.append(remove_html_tags(i))

print(clean)

# Turning the list with all the paragraphs into a string
clean_paragraph = ''.join(clean)
print(clean_paragraph)

# Creating a txt file and saving all the paragraphs to it
f = open("avery.txt", 'w')
for i in clean:
    f.write(i)
f.close()
'''