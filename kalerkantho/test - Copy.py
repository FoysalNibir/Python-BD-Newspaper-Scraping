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



url = "http://kalerkantho.com/print-edition/first-page/2017/01/01/447459"

date = "2017-01-01"



date_1 = datetime.strptime(date, "%Y-%m-%d")
print(date_1)
# year = datetime(date_1).year
year = str(parse(date, fuzzy=True).year)

path_1 = "D:/newspaper_images"
if not os.path.exists(path_1):
    os.makedirs(path_1)

path_2 = path_1 + "/kalerkontho"
if not os.path.exists(path_2):
    os.makedirs(path_2)

path_3 = path_2 + "/" + year
if not os.path.exists(path_3):
    os.makedirs(path_3)

path_4 = path_3 + "/" + date
if not os.path.exists(path_4):
    os.makedirs(path_4)
print (path_4)
db_path = "kalerkontho/" + year + "/" + date

print(db_path)

newyear = "/"+year
print(newyear)

# for year, group in groupby(date_1.items(), lambda (k, v): k.year):
#     print(year)

#print(year)


def getNews(url):
    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')
    full_news_box= soup.find('div', attrs={'class': 'some-class-name2'})

    for script in soup(["script"]):
        script.extract()

    full_news = full_news_box.text.strip()
    destination_box = soup.findAll('meta', attrs={'name': 'description'})

    for content in destination_box:
        summary = (content.get('content'))

    #print(summary)

    entrytime_box = soup.find('div', attrs={'class': 'col-xs-12 col-md-6 row'})
    entrytime = entrytime_box.text.strip()

    print(entrytime)

    return ([(url,full_news,summary)])

var = getNews(url)

print(var)
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