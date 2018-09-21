import json
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import winsound
import datetime
from datetime import datetime, timedelta
import pymysql
import time
from itertools import groupby
from dateutil.parser import parse
from MultiScrappingV2 import MultiScrapper

def getDate():
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "samakal"
    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=9""")
    date = cursor.fetchone()
    cursor.close()
    date=str(date[0])
    db_connection.close()

    date_1 = datetime.strptime(date, "%Y-%m-%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y-%m-%d")

    return date


date = getDate()
print 'Starting date=',date

now = datetime.now()
CurrentDate = now.strftime("%Y-%m-%d")
news_count = 0

def getLinks(soup,date,scrapper):
    global news_count
    year = str(parse(date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/samakal"
    if not os.path.exists(path_2):
        os.makedirs(path_2)

    path_3 = path_2 + "/" + year
    if not os.path.exists(path_3):
        os.makedirs(path_3)

    path_4 = path_3 + "/" + date
    if not os.path.exists(path_4):
        os.makedirs(path_4)

    for script in soup(["script"]):
        script.extract()

    # result_items = []

    for content in soup.find_all('a', class_='link-overlay'):
        news_link = (content.get('href'))

        length = len(news_link)
        end = ''
        count = 0

        for i in range(length):
            if news_link[i] == '/':
                count += 1
                end = i

        news_link = news_link[:end + 1]

        print(news_link)
        scrapper.Add(news_link,date,news_count,path_4)
        # news_data = getNews(news_link,date,news_count,path_4)
        # result_items.append(news_data)
        news_count += 1

def getNews(url,date,news_count,newPath):
    id = 9
    news_paper_id = int(id)
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soupNews = BeautifulSoup(news_page, 'html.parser')

    for script in soupNews(["script"]):
        script.extract()

    full_news_box = soupNews.find('div', attrs={'class': 'description'})
    full_news = full_news_box.text.strip()

    # full_news_box = soup.find("div", {"class": "description"}).find_all('p')
    # full_news = ''
    # for element in full_news_box:
    #     full_news += '\n' + ''.join(element.findAll(text=True))

    headline_box = soupNews.find('h1', attrs={'class': 'font-xs-h detail-headline '})
    headline=''

    if headline_box:
        headline = headline_box.text.strip()

    else:
        for text in soupNews.find_all('div', attrs={'class': 'openion-news-head'}):
            headline = text.select('h1')[0].text.strip()

        print(headline)

    year = str(parse(date, fuzzy=True).year)

    description_box = soupNews.findAll('meta', attrs={'property': 'og:description'})

    summary = ''
    for content in description_box:
        summary = (content.get('content'))

    meta_data = headline + ' ' + summary

    entrytime_box = soupNews.find('span', attrs={'class': 'detail-time'})
    if entrytime_box:
        entrytime = entrytime_box.text.strip()

    else:
        entrytime_box=soupNews.find('span', attrs={'class': 'writer'})
        entrytime = entrytime_box.text.strip()
        print(entrytime)

    category_box = soupNews.find('p', attrs={'class': 'detail-reporter'})
    category = ''
    
    if category_box:
        category = category_box.text.strip()

    ImgData = soupNews.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])

    if(image_link == "http://samakal.com/assets/images/default_news.jpg"):
        db_img = ""
    else:
        image_link = image_link
        image_name = img_count + '.jpg'
        db_img = "samakal/" + year + "/" + date + "/" + image_name
        file = open(image_name, 'wb')
        file.write(urllib.urlopen(image_link).read())
        file.close()
        source_dir_image = "D:/samakal/" + img_count + ".jpg"

        try:
            os.remove(newPath + "/" + img_count + ".jpg")
        except:
            pass

        destination_dir_image = newPath + "/" + img_count + ".jpg"
        os.rename(source_dir_image, destination_dir_image)

    return (news_paper_id,category,headline,full_news,entrytime,date,db_img,meta_data)


def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "samakal"

    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.executemany("INSERT INTO newspapers (newspaper_id,category,headline,details,entrytime,news_date,img,meta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",data)
    db_connection.commit()
    db_connection.close()
    print(" > Data Inserted")

def dataUpdate(date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "samakal"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=9""",(date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")

def dataDelete(newspaper_id,date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "samakal"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""DELETE FROM newspapers WHERE newspaper_id=%s AND news_date=%s""",(newspaper_id,date))
    db_connection.commit()
    db_connection.close()
    print(" > Data deleted")

i=0

scrapper = MultiScrapper(getNews,20)

while True:

    try:
        if (date < CurrentDate):
            dataDelete(9,date)

            while True:
                url = "http://samakal.com/archive/" + date + "?&page=" + str(i)
                print(url)
                existance = urllib2.urlopen(url)
                soup = BeautifulSoup(existance, 'html.parser')

                check = soup.find('div', class_='media-left')

                if not check:
                    i = 0
                    break
                else:
                    getLinks(soup,date,scrapper)

                i += 1

            print(news_count)
            result_items = scrapper.ScrapAll()
            dataInsert(result_items)
            dataUpdate(date)
            scrapper.Reset()

            date_1 = datetime.strptime(date, "%Y-%m-%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y-%m-%d")
            news_count = 0
        else:
            break

    except:
        i = 0
        while (i < 2):
            duration = 100  # millisecond
            freq = 1500  # Hz
            winsound.Beep(freq, duration)
            i += 1
            time.sleep(0.01)
        print("Oops, Something Happened!!!")
        time.sleep(1)
        print("Attempting to restart")
        time.sleep(10)
        raise
        #continue