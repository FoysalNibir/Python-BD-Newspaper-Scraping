# coding=utf-8
import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as dummyPool

def getNews(url):


    site = url
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(site, headers=hdr)

    news_page = urllib2.urlopen(req)
    soupNews = BeautifulSoup(news_page.read().decode('utf-8', 'ignore'), 'html.parser')

    for script in soupNews(["script"]):
        script.extract()

    full_news_box = soupNews.find("div", {"class": "postBody"})
    full_news = full_news_box.text.strip()
    print 'Details: ', full_news

    headline_box = soupNews.find('div', attrs={'class': 'postDetails'}).find('h1')
    headline = headline_box.text.strip()
    print 'Headline: ', headline

    description_box = soupNews.findAll('meta', attrs={'property': 'og:description'})

    summary = ''
    for content in description_box:
        summary = (content.get('content'))

    print 'Summery: ', summary
    meta_data = headline + ' ' + summary
    print 'Meta: ', meta_data

    entrytime_box = soupNews.find('div', attrs={'class': 'postInfo'})
    entrytime = entrytime_box.text.strip()
    print 'Entrytime: ', entrytime

    category_box = soupNews.find('ul', attrs={'class': 'breadcrumb'})
    category = category_box.text.strip()
    print 'Category: ', category

    ImgData = soupNews.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])
    print 'Img: ', image_link


url = 'http://www.dailysangram.com/post/28350'
getNews(url)