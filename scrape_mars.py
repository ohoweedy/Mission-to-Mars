# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time


# def initBrowser():
#     executable_path = {'executable_path': '/anaconda3/envs/PythonData/bin/chromedriver'}
#     return Browser("chrome", **executable_path, headless=False)

# def crawl(url, browser):
#     browser.visit(url)
#     print(browser.html)
#     return browser.html

def init_browser():
    executable_path = {'executable_path': '/anaconda3/envs/PythonData/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    ##### NASA Mars News #####
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
#     print(news_title)

    news_p = soup.find('div', class_='article_teaser_body').text
#     print(news_p)

    date = soup.find('div', class_='list_date').text
#     print(date)

    ##### JPL Mars Space Images - Featured Image #####
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'    

    browser.visit(url_2)

    time.sleep(1)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    featured_image = soup2.find_all('a', class_='fancybox')[0].get('data-fancybox-href')
#     print(featured_image)

    base_jpl_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_jpl_url + featured_image
#     print(featured_image_url)

    ##### Mars Weather #####
    url_3 = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url_3)

    time.sleep(1)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    mars_weather = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_weather = mars_weather.replace('\n', ' ')
#     print(mars_weather)

    ##### Mars Facts #####
    url_4 = 'https://space-facts.com/mars/'

    browser.visit(url_4)

    time.sleep(1)

    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')

    mars_table = pd.read_html(url_4)
#     print(mars_table)

    mars_table_df = mars_table[0]
    mars_table_df.columns = ['Metric', 'Measurement']
    mars_table_df.set_index('Metric')
#     print(mars_table_df)

    mars_html_table = mars_table_df.to_html()

    mars_html_table = mars_html_table.replace('\n', '')
#     print(mars_html_table)

    ##### Mars Hemispheres #####
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_5)

    time.sleep(1)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')

    base_hemis_url = 'https://astrogeology.usgs.gov'

    hemis_links = []
    unique_hemis_links = []
    img_urls = []
    titles = []

    for x in range(8):
        link = soup5.find_all('a', class_='itemLink product-item')[x].get('href')
        hemis_links.append(base_hemis_url + link)

    for i in hemis_links:
        if i not in unique_hemis_links:
            unique_hemis_links.append(i)
#     print(unique_hemis_links)

    for c in range(4):
        title = soup5.find_all('h3')[c].text
        title = title.replace(' Enhanced', '')
        titles.append(title)
#     print(titles)

    for unique_hemis_link in unique_hemis_links:
        browser.visit(unique_hemis_link)
        hemi_html = browser.html
        hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
        hemi_url = hemi_soup.find('img', class_="wide-image").get('src')
        img_urls.append(base_hemis_url + hemi_url)
#     print(img_urls)

    hemisphere_image_urls = []

    for y in range(4):
        hemisphere_image_urls.append({"title": titles[y], "img_url": img_urls[y]})
        
    # Store all scraped Mars data into a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "date": date,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_html_table": mars_html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data
        
    




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


