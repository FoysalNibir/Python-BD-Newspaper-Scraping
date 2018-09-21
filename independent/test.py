import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta

def getNews(url):
    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')

    full_news_box = soup.find("div", {"id": "newsDtl"}).findAll('p')
    full_news = ''
    for element in full_news_box:
        full_news += '\n' + ''.join(element.findAll(text=True))


    headline_box1 = soup.find("div", {"id": "hl1"})
    if (headline_box1):
        headline1 = headline_box1.text.strip()
    else:
        headline1 = ''

    headline_box2 = soup.find("div", {"id": "hl2"}).find('h2')
    if (headline_box2):
        headline2 = headline_box2.text.strip()
    else:
        headline2 = ''

    headline_box3 = soup.find("div", {"id": "hl3"})
    if(headline_box3):
        headline3 = headline_box3.text.strip()
    else:
        headline3 = ''

    headline = headline1 + " " + headline2 + " " + headline3

    category_box = soup.find("div", {"class": "menu_name_details"})
    category = category_box.text.strip()

    author_box = soup.find("div", {"id": "rpt"})
    author = author_box.text.strip()

    update_time_box = soup.find("span", {"id": "news_update_time"})
    update_time = update_time_box.text.strip()

    entrytime = author + " " + update_time

    summary_box = soup.find('meta', attrs={'itemprop': 'description'})
    summary = summary_box.get('content')

    meta = headline + " " + summary

    print(headline)
    print(full_news)
    print(meta)
    print(category)
    print(entrytime)
    # ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    # image_link = ''
    # meta_data = headline + " " + summary
    # entrytime_box = soup.find('div', attrs={'class': 'col-xs-12 col-md-6 row'})
    # entrytime = entrytime_box.text.strip()
    #
    # for meta in ImgData:
    #     image_link = (meta['content'])

getNews("http://www.theindependentbd.com/arcprint/details/123812/2017-11-16")