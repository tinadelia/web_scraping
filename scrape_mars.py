#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd


#site navigation
def init_browser():
    executable_path = {"executable_path": "C:/Users/tinad/Desktop/web_scrapping/web_scrapping/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def title_scrape():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news = soup.find('div', class_='list_text')
    mars_title = news.find('div', class_='content_title').text
    title = mars_title
    mars_data["title"] = title
    browser.quit()
    return mars_data

def paragraph_scrape():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news = soup.find('div', class_='list_text')
    mars_paragraph = news.find('div', class_='article_teaser_body').text
    paragraph = mars_paragraph
    mars_data["paragraph"] = paragraph
    browser.quit()
    return mars_data

def image_scrape():
    browser = init_browser()
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    image = image_soup.find('img', class_='thumb')['src']
    mars_jpl_image = "https://www.jpl.nasa.gov" + image
    image = mars_jpl_image
    mars_data["image"] = image
    browser.quit()
    return mars_data


def twitter_scrape():
    browser = init_browser()
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter_url)
    weather_soup = BeautifulSoup(response.text, 'html.parser')
    mars_weather_tweet = weather_soup.find_all('div', class_ = "js-tweet-text-container")
    for tweet in mars_weather_tweet:
        if tweet.text.strip().startswith('InSight'):
            mars_weather = tweet.text.strip()
    weather = mars_weather
    mars_data["weather"] = weather
    browser.quit()
    return mars_data


def facts_scrape():
    browser = init_browser()
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    table = pd.read_html(facts_url)
    mars_facts = table[0]
    mars_facts = mars_facts.loc[:, ["Mars - Earth Comparison", "Mars"]]
    mars_facts = mars_facts.rename(columns={"Mars - Earth Comparison": "description", "Mars": "value"})
    mars_facts.set_index('description', inplace=True)
    mars_facts = mars_facts.to_html()
    facts = mars_facts
    mars_data["facts"] = facts
    browser.quit()
    return mars_data


def hems_scrape():
    browser = init_browser()
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    usgs_html = browser.html
    soup = BeautifulSoup(usgs_html, 'html.parser')

    mars_hemispheres = []

    list = soup.find("div", class_ = "result-list" )
    hemispheres = list.find_all("div", class_="item")


    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(img_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        img_url = downloads.find("a")["href"]
        mars_hemispheres.append({"title": title, "img_url": img_url})
    hems = mars_hemispheres
    mars_data["hems"] = hems
    browser.quit()
    return mars_data

