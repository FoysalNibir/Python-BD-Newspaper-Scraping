import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta

date = '2015/01/01'
now = datetime.now()
CurrentDate = now.strftime("%Y/%m/%d")
news_count = 0

def getPage(url,date):
    global news_count
    modified_date = datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")
    year = str(parse(modified_date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/kalerkontho"
    if not os.path.exists(path_2):
        os.makedirs(path_2)

    path_3 = path_2 + "/" + year
    if not os.path.exists(path_3):
        os.makedirs(path_3)

    path_4 = path_3 + "/" + modified_date
    if not os.path.exists(path_4):
        os.makedirs(path_4)

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    for script in soup(["h2"]):
        script.extract()

    result_items = []

    for data in soup.find_all('div', class_='col-xs-6 left print'):
        for a in data.find_all('a'):
            news_url = (a.get('href')) # for getting link
            print(news_url)
            news_data = getNews(news_url,modified_date,news_count,path_4)
            result_items.append(news_data)
            news_count = news_count + 1

    dataInsert(result_items)
    dataUpdate(modified_date)

def getNews(url,modified_date,news_count,newPath):
    id = 4
    news_paper_id = int(id)
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')
    full_news_box= soup.find('div', attrs={'class': 'some-class-name2'})
    headline_box = soup.find('h2')
    headline = headline_box.text.strip()
    year = str(parse(modified_date, fuzzy=True).year)

    for script in soup(["script"]):
        script.extract()

    full_news = full_news_box.text.strip()
    destination_box = soup.findAll('meta', attrs={'name': 'description'})

    for content in destination_box:
        summary = (content.get('content'))

    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''
    meta_data = headline + " " + summary
    entrytime_box = soup.find('div', attrs={'class': 'col-xs-12 col-md-6 row'})
    entrytime = entrytime_box.text.strip()

    for meta in ImgData:
        image_link = (meta['content'])

    if(image_link == "http://www.kalerkantho.com/assets/site/img/kkoo.png"):
        db_img = ""
    else:
        image_link = image_link
        db_img = "kalerkontho/" + year + "/" + modified_date
        image_name = img_count + '.jpg'
        file = open(image_name, 'wb')
        file.write(urllib.urlopen(image_link).read())
        file.close()
        source_dir_image = "D:/kalerkontho/" + img_count + ".jpg"
        destination_dir_image = newPath + "/" + img_count + ".jpg"
        os.rename(source_dir_image, destination_dir_image)

    return (news_paper_id,headline.encode("utf-8"),full_news.encode("utf-8"),entrytime.encode("utf-8"),modified_date.encode("utf-8"),db_img.encode("utf-8"),meta_data.encode("utf-8"))

def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "osint"

    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB)
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.executemany("INSERT INTO newspapers (newspaper_id,headline,details,entrytime,news_date,img,meta) VALUES (%s, %s, %s, %s, %s, %s, %s)",data)
    db_connection.commit()
    db_connection.close()
    print(" > Data Inserted")

def dataUpdate(date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "osint"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB)
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=4""",(date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")

# while True:
#     try:
#         if (date < CurrentDate):
#             page_url = "http://kalerkantho.com/print-edition/" + date
#             getPage(page_url,date)
#             date_1 = datetime.strptime(date, "%Y/%m/%d")
#             date = date_1 + timedelta(days=1)
#             date = datetime.strftime(date, "%Y/%m/%d")
#             news_count = 0
#         else:
#             break
#     except:
#         print("No news at:", date)
#         pass

while True:
    if (date < CurrentDate):
        page_url = "http://kalerkantho.com/print-edition/" + date
        getPage(page_url,date)
        date_1 = datetime.strptime(date, "%Y/%m/%d")
        date = date_1 + timedelta(days=1)
        date = datetime.strftime(date, "%Y/%m/%d")
        news_count = 0
    else:
        break
