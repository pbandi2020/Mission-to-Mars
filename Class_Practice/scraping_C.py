# Import the libraries
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
# executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# The website that we are accessing to extract information from.
# Quotes is the site
url = 'http://quotes.toscrape.com/'
browser.visit(url)

# We will be using BeautifulSoup to parse the HTML. The below line of code will extract 
# the entire html code for the webpage.
html = browser.html
html_soup = soup(html, 'html.parser')
# print(html_soup)

# Now we will parse to extract specific tags 
# scarape the title.
# We've also extracted only the text within the HTML tags by adding .text
# to the end of the code.
title = html_soup.find('h2').text
# print(title)

# Scrape the top ten tags
tag_box = html_soup.find('div', class_='tags-box')
# tag_box
tags = tag_box.find_all('a', class_='tag')

for tag in tags:
    word = tag.text
    print(word)

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
# executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'http://quotes.toscrape.com/'
browser.visit(url)


# for x in range(1,6):
#     html=browser.html
#     quote_soup = soup(html, 'html.parser')
#     quotes = quote_soup.find_all('div',class_='quote')
#     for quote in quotes:
#         print('page:', x, '----------')
#         print(quote.text)
#     browser.links.find_by_partial_text('Next')
    
for x in range(1,6):
    url = f'http://quotes.toscrape.com/page/{x}/'
    browser.visit(url)
    html=browser.html
    print(url)
    quote_soup = soup(html, 'html.parser')
    quotes = quote_soup.find_all('div',class_='quote')
    for quote in quotes:
        print('page:', x, '----------')
        print(quote.text)
    browser.links.find_by_partial_text('Next')
    

# Setup splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

# ## JPL Space Impage Featured Image
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Pandas also has a way to easily convert our DataFrame back into
# HTML-ready code using the .to_html() function. 

df.to_html()

browser.quit()

