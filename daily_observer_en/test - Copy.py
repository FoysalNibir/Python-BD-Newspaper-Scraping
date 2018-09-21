import os
import time
import urllib
import urllib2
import pymysql
import winsound
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta


#date= datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")



url = "http://www.observerbd.com/archive.php?d=04&m=01&y=2018"

date = "2017-01-01"



def getPage(url):
    count = 1
    result = []
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    # result_items = []

    for data in soup.find_all('div', class_='archive'):
        for a in data.find_all('a'):
            news_url = (a.get('href'))
            news_url = "http://www.observerbd.com/" + news_url
            # print(news_url)
            # news_data = getNewsNew(news_url,modified_date,news_count,path_4)
            result.append(news_url)
            count +=1
    print(count)
    return result

result = getPage(url)
print result
print result[0]