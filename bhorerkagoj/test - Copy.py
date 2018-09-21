import json
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import datetime
from datetime import datetime
import pymysql
from itertools import groupby
from dateutil.parser import parse



#date= datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")



url = "http://samakal.com/archive/2015-01-19?&page=0"

date = "2015-07-01"



news_count = 0

def getLinks(soup):
    global c
    global news_count
    for script in soup(["script"]):
        script.extract()

    for content in soup.find_all('a', class_='link-overlay'):
        news_link = (content.get('href'))

        length = len(news_link)
        end = ''
        count = 0

        for i in range(length):
            if news_link[i] == '/':
                count += 1
                end = i

        news_link = news_link[:end+1]
        print(news_link)
        getNews(news_link)
        print(news_count)
        news_count += 1


def getNews(url):
    id = 9
    news_paper_id = int(id)
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soupNews = BeautifulSoup(news_page, 'html.parser')

    for script in soupNews(["script"]):
        script.extract()

    full_news_box = soupNews.find('div', attrs={'class': 'description'})
    full_news = full_news_box.text.strip()
    print(full_news)

    headline_box = soupNews.find('h1', attrs={'class': 'font-xs-h detail-headline '})
    headline = headline_box.text.strip()
    print(headline)

    year = str(parse(date, fuzzy=True).year)


    description_box = soupNews.findAll('meta', attrs={'property': 'og:description'})

    for content in description_box:
        summary = (content.get('content'))

    print(summary)

    entryTime_box = soupNews.find('span', attrs={'class': 'detail-time'})
    entryTime = entryTime_box.text.strip()
    print(entryTime)

    category_box = soupNews.find('p', attrs={'class': 'detail-reporter'})
    category = category_box.text.strip()
    print(category)


page_count = 0

while True:
    url = "http://samakal.com/archive/"+ date + "?&page=" + str(page_count)
    existance = urllib2.urlopen(url)
    soup = BeautifulSoup(existance, 'html.parser')

    check = soup.find('div', class_='media-left')

    if not check:
        page_count=0
        break
    else:
        getLinks(soup)

    page_count+=1
    news_count = 0

# result_json_data = json.dumps(var)
# print(result_json_data)

# conn = pymysql.connect(host="localhost", user="root", passwd="", db="test")
# myCursor = conn.cursor()

# print var['summary']
# print pymysql.escape_string(var['summary'])
# json_obj = json.loads(result_json_data.decode('unicode_escape').encode('iso8859-1').decode('utf8'))
# print var["summary"].encode("utf-8").decode("ascii")
# var = {}
# for product in json_obj:
# myCursor.executemany("INSERT INTO details (url, full_news, summary) VALUES (%s,%s,%s)", var)
#
# #myCursor.execute("INSERT INTO details VALUES %s", result_json_data)
# conn.commit()
#
# conn.close()

#print(result_json_data)