import os
import time
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as dummyPool

def getDate():
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "kalerkantho"
    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=4""")
    date = cursor.fetchone()
    cursor.close()
    date=str(date[0])
    db_connection.close()

    date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y/%m/%d")
    date_1 = datetime.strptime(date, "%Y/%m/%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y/%m/%d")

    return date

def getPage(url, date):
    global news_count
    modified_date = datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")
    year = str(parse(modified_date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)
        print path_1

    path_2 = path_1 + "/kalerkantho"
    if not os.path.exists(path_2):
        os.makedirs(path_2)

    path_3 = path_2 + "/" + year
    if not os.path.exists(path_3):
        os.makedirs(path_3)

    path_4 = path_3 + "/" + modified_date
    if not os.path.exists(path_4):
        os.makedirs(path_4)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    for script in soup(["h2"]):
        script.extract()

    p = dummyPool(50)
    arguments = []

    for data in soup.find_all('div', class_='col-xs-6 left print'):
        for a in data.find_all('a'):
            news_url = (a.get('href'))  # for getting link
            print(news_url)
            arguments.append([news_url, modified_date, news_count, path_4])
            news_count = news_count + 1
            # try:
            #     urllib2.urlopen(news_url)
            #     arguments.append([news_url, modified_date, news_count, path_4])
            #     news_count = news_count + 1
            # except:
            #     print('Problem in',news_url)

    result_items = p.map(getNews, arguments)
    p.close()
    p.join()
    print(news_count)

    dataInsert(result_items)

    dataUpdate(modified_date)
    p.terminate()


def getNews(arguments):
    id = 4
    news_url = arguments[0]
    modified_date = arguments[1]
    news_count = arguments[2]
    path = arguments[3]

    news_paper_id = int(id)
    img_count = str(news_count)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(news_url, headers=hdr)
    news_page = urllib2.urlopen(req)

    soup = BeautifulSoup(news_page, 'html.parser')

    for script in soup(["script"]):
        script.extract()

    full_news_box = soup.find('div', attrs={'class': 'some-class-name2'})
    full_news = ''

    if full_news_box:
        full_news = full_news_box.text.strip()

    headline_box = soup.find('h2')
    headline = ''

    if headline_box:
        headline = headline_box.text.strip()

    year = str(parse(modified_date, fuzzy=True).year)

    description_box = soup.findAll('meta', attrs={'name': 'description'})

    summary = ''

    for content in description_box:
        summary = (content.get('content'))

    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''
    meta_data = headline + " " + summary
    entrytime_box = soup.find('div', attrs={'class': 'col-xs-12 col-md-6 row'})
    entrytime = ''

    if entrytime_box:
        entrytime = entrytime_box.text.strip()

    for meta in ImgData:
        image_link = (meta['content'])

    if (image_link == "http://www.kalerkantho.com/assets/site/img/kkoo.png"):
        db_img = ""
    else:
        try:
            image_link = image_link
            image_name = img_count + '.jpg'
            db_img = "kalerkantho/" + year + "/" + modified_date + "/" + image_name
            destination_dir_image = path + "/" + img_count + ".jpg"
            try:
                os.remove(path + "/" + img_count + ".jpg")
            except:
                pass

            print destination_dir_image
            urllib.urlretrieve(image_link, destination_dir_image)

        except:
            db_img = ""
            try:
                os.remove("/" + img_count + ".jpg")
            except:
                pass

    return (news_paper_id, headline, full_news, entrytime, modified_date, db_img, meta_data)

def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "kalerkantho"

    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
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
    THEDB = "kalerkantho"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
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

if __name__ == '__main__':
    date = getDate()
    print 'Starting date =', date

    now = datetime.now()
    CurrentDate = now.strftime("%Y/%m/%d")
    news_count = 0
    while True:
        try:
            if (date < CurrentDate):
                print 'Now Scraping =', date
                page_url = "http://kalerkantho.com/print-edition/" + date
                print(page_url)
                getPage(page_url,date)
                date_1 = datetime.strptime(date, "%Y/%m/%d")
                date = date_1 + timedelta(days=1)
                date = datetime.strftime(date, "%Y/%m/%d")
                news_count = 0
            else:
                break

        except:
            print('No news at: ', date)
            pass

