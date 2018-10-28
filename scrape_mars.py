
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
import pymongo
import tweepy
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time


# In[2]:


### NASA Mars News


# In[3]:

def scrape():

    #pointing to the directory where chromedriver exists
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visiting the page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html,"html.parser")


    # In[4]:


    # Get title & description
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Paragraph: {news_paragraph}")


    # In[5]:


    ### JPL Mars Space Images - Featured Image


    # In[6]:


    # JPL Mars URL
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Setting up splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    browser.visit(image_url)


    # In[7]:


    # Moving through the pages
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)


    # In[8]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    # Get featured image
    #results = soup.find('article')
    extension = soup.find('figure', class_='lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension


    # In[9]:


    #featured_image_url


    # In[10]:


    ### Mars Weather


    # In[11]:


    #get mars weather's latest tweet from the website
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)


    # In[12]:


    weather = browser.html
    soup = bs(weather, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    print(f" mars_weather : {mars_weather}")


    # In[13]:


    ### Mars Facts


    # In[14]:


    facts_url = "http://space-facts.com/mars/"
    data = pd.read_html(facts_url)
    #data


    # In[15]:


    table= data[0]
    table.columns = ["Parameter", "Value"]
    #table


    # In[16]:


    html_mars_table = table.to_html()
    html_mars_table = html_mars_table.replace("\n", "")
    #html_mars_table


    # In[17]:


    ### Mars Hemispheres


    # In[18]:


    # scrape images of Mars' hemispheres from the USGS site
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
        browser.visit(mars_hemisphere_url)

        time.sleep(2)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')

        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()

        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()

        print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)


    # In[19]:

    h = {"hemi_dicts": hemi_dicts,"featured_image_url":featured_image_url, "new_title": news_title, "news_paragraph": news_paragraph, "mars_weather": mars_weather, "fact_table": html_mars_table }
    return h




