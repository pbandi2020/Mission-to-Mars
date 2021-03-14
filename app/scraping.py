# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Setup splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

# Module 10.5.3 - connecting to MongoDB
def scrape_all():
    # iniitate headdless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run the scraping function and store the data into a dictionary
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "hemispheres": hemisphere_scrape(browser),
            "last_modified": dt.datetime.now()
    }
    # Stop the webdriver and return the data
    browser.quit()
    return data

# function - 10.5.2 module
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p
        
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

# Function to get the Mars Facts
def mars_facts():
    try:
        # use pandas "read_html" function to scrape the fact table into a data frame
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        # df.head()
    except BaseException:
        None
    
    # Assign the columns and set the index of the data frame
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert the dataframe into HTML format and add bootstrap

    return df.to_html()
# scrape the hemispheres of Mars
def hemisphere_scrape(browser):
    #visit url
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    hemisphere_image_urls = []   # empty dictionary to hold titles and urls
    #get the links of hemispheres
    img_link = browser.find_by_css("a.product-item h3")
    
    #loop through the number of urls.
    for i in range(4):
        # empty dictionary
        hemisphere_dict = {}   
        #click on each url using the click()
        browser.find_by_css('a.product-item h3')[i].click() 
        #get the title of the hemisphere and add into the dictionary
        hemisphere_dict['title']=  browser.find_by_css('h2.title').text
        #just validating the title in the dictionary
        print(hemisphere_dict)
        #check links on the Sample text  within the same url 
        img_url_text = browser.links.find_by_text('Sample').first
        #add to the hemisphere dict 
        hemisphere_dict['img_url'] = img_url_text['href']
        print(hemisphere_dict)
        #append the to empty list
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()
    
    return hemisphere_image_urls

    # Finally, we navigate backwards
    browser.back()

# browser.quit()
if __name__ == "__main__":
    # print the scraped data when run as script
    print(scrape_all())