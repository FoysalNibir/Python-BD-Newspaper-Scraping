import os
import time
import urllib
import urllib2
import pymysql
import winsound
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from MultiScrappingV2 import MultiScrapper


def getDate():
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "observer"
    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=6""")
    date = cursor.fetchone()
    cursor.close()
    date=str(date[0])
    db_connection.close()

    date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y/%m/%d")
    date_1 = datetime.strptime(date, "%Y/%m/%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y/%m/%d")

    return date


date = getDate()
print 'Starting date =',date

now = datetime.now()
CurrentDate = now.strftime("%Y/%m/%d")
news_count = 0
check_date = '2016/07/10'

def alarm(haltDuration,alarmNo):
    i = 1
    while (i <= alarmNo):
        duration = 100  # millisecond
        freq = 1500  # Hz
        winsound.Beep(freq, duration)
        i += 1
        time.sleep(0.01)
    print("Oops, Something Happened!!!")
    time.sleep(1)
    print("Attempting to restart")
    time.sleep(haltDuration)

def getPage(url,date):
    global news_count
    modified_date = datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")
    year = str(parse(modified_date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/observer_en"
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

    # result_items = []

    for data in soup.find_all('div', class_='bullet'):
        for a in data.find_all('a'):
            news_url = (a.get('href'))
            news_url = (news_url[8:])
            news_url = "http://www.observerbd.com" + news_url
            print(news_url)
            # news_data = getNews(news_url,modified_date,news_count,path_4)
            # result_items.append(news_data)
            scrapper.Add(news_url,modified_date,news_count,path_4)
            news_count = news_count + 1

    print(news_count)
    result_items = scrapper.ScrapAll()
    dataInsert(result_items)
    dataUpdate(date)
    scrapper.Reset()


def getNews(url,modified_date,news_count,newPath):
    id = 6
    news_paper_id = int(id)
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')

    for script in soup(["script"]):
        script.extract()

    full_news_box= soup.find('div', attrs={'id': 'f'})
    headline_box = soup.find('div', attrs={'class': 'detail_heading'})
    headline = headline_box.text.strip()
    year = str(parse(modified_date, fuzzy=True).year)
    full_news = full_news_box.text.strip()

    entrytime0 = ''
    entrytime1 = ''
    entrytime2 = ''

    entrytime_box0 = soup.find('div', attrs={'style': 'color: #545353; margin: 0 0 10px 0'})

    if entrytime_box0:
        entrytime0 = entrytime_box0.text.strip()

    entrytime_box1 = soup.find('font', attrs={'color': '#666666'})

    if entrytime_box1:
        entrytime1 = entrytime_box1.text.strip()

    entrytime_box2 = soup.find('div', attrs={'style': 'font-size: 20px; color: #545353'})

    if entrytime_box2:
        entrytime2 = entrytime_box2.text.strip()

    entrytime = entrytime2+ '  ' + entrytime0 + entrytime1
    summary_box = soup.findAll('meta', attrs={'name': 'description'})

    summary = ''
    for content in summary_box:
        summary = (content.get('content'))

    meta_data = headline + ' ' + summary

    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])

    if(image_link == '.jpg"/' or image_link[-5:] == '..jpg'):
        db_img = ""

    else:
        image_link = image_link
        image_name = img_count + '.jpg'
        try:
            file = open(image_name, 'wb')
            file.write(urllib.urlopen(image_link).read())
            file.close()
            db_img = "observer_en/" + year + "/" + modified_date + "/" + image_name
            source_dir_image = "D:/daily_observer_en/" + img_count + ".jpg"
            destination_dir_image = newPath + "/" + img_count + ".jpg"
            os.rename(source_dir_image, destination_dir_image)

        except:
            file = open(image_name, 'wb')
            file.close()
            os.remove(image_name)
            db_img = ""

    return (news_paper_id,headline,full_news,entrytime,modified_date,db_img,meta_data)

def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "observer"

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
    THEDB = "observer"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB , charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=6""",(date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")


########################################
########################################
########################################

def getPageNew(url,date,scrapperNew):
    global news_count
    modified_date = datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")
    year = str(parse(modified_date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/observer_en"
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

    # result_items = []

    for data in soup.find_all('div', class_='archive'):
        for a in data.find_all('a'):
            news_url = (a.get('href'))
            news_url = "http://www.observerbd.com/" + news_url
            print(news_url)
            # news_data = getNewsNew(news_url,modified_date,news_count,path_4)
            # result_items.append(news_data)
            scrapperNew.Add(news_url,modified_date,news_count,path_4)
            news_count = news_count + 1

    print(news_count)
    result_items = scrapperNew.ScrapAll()
    if len(result_items)==news_count:
        dataInsertNew(result_items)
        dataUpdate(date)
    else:
        alarm(10,3)
        news_count = 0
        time.sleep(10)
        getPageNew(url, date, scrapperNew)
    scrapperNew.Reset()


def dataInsertNew(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "observer"

    db_connection=pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.executemany("INSERT INTO newspapers (newspaper_id,category,headline,details,entrytime,news_date,img,meta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",data)
    db_connection.commit()
    db_connection.close()
    print(" > Data Inserted")


def getNewsNew(url,modified_date,news_count,newPath):
    id = 6
    news_paper_id = int(id)
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')

    for script in soup(["script"]):
        script.extract()

    full_news_box= soup.find('div', attrs={'id': 'f'})

    headline_box1 = soup.find('h2')
    headline_box2 = soup.find('h1')

    headline1=''
    headline2=''

    if headline_box1:
        headline1 = headline_box1.text.strip()

    if headline_box2:
        headline2 = headline_box2.text.strip()

    headline = headline1 + '  ' + headline2

    year = str(parse(modified_date, fuzzy=True).year)

    full_news=''
    if full_news_box:
        full_news = full_news_box.text.strip()

    else:
        print("Link", url, "has no news")

    entrytime=''
    for data in soup.find_all('div', class_='pub'):
        entrytime=''
        for span in data.find_all('span'):
            entrytime = entrytime+" "+span.text.strip()

    summary_box = soup.findAll('meta', attrs={'property': 'og:description'})

    summary = ''
    for content in summary_box:
        summary = (content.get('content'))

    meta_data = headline + ' ' + summary

    category_box = soup.find('span', attrs={'class': 'location'})
    category = category_box.text.strip()

    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])

    if(image_link == '.jpg"/' or image_link == 'http://www.observerbd.com/files/FB-Share.jpg'):
        db_img = ""

    else:
        image_link = image_link
        image_name = img_count + '.jpg'
        file = open(image_name, 'wb')
        try:
            file.write(urllib.urlopen(image_link).read())
            file.close()
            db_img = "observer_en/" + year + "/" + modified_date + "/" + image_name
            source_dir_image = "D:/daily_observer_en/" + img_count + ".jpg"

            try:
                os.remove(newPath + "/" + img_count + ".jpg")
            except:
                pass

            destination_dir_image = newPath + "/" + img_count + ".jpg"
            os.rename(source_dir_image, destination_dir_image)

        except:
            file.close()
            source_dir_image = "D:/daily_observer_en/" + img_count + ".jpg"
            os.remove(source_dir_image)
            db_img = ""

    return (news_paper_id,category,headline,full_news,entrytime,modified_date,db_img,meta_data)

scrapper = MultiScrapper(getNews,5)
scrapperNew = MultiScrapper(getNewsNew,5)

while True:
    try:
        if (date < check_date):
            page_url = "http://www.observerbd.com/" + date + "/index.php"
            getPage(page_url,date,scrapper)

            date_1 = datetime.strptime(date, "%Y/%m/%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y/%m/%d")
            news_count = 0
        else:
            if (date < CurrentDate):
                year = str(parse(date, fuzzy=True).year)
                month = str(parse(date, fuzzy=True).month)
                day = str(parse(date, fuzzy=True).day)

                if (int(day) < 10):
                    day = '0' + day

                if (int(month) < 10):
                    month = '0' + month

                else:
                    day = day
                    month = month

                page_url = "http://www.observerbd.com/archive.php?" + "d=" + day + "&m=" + month + "&y=" + year
                print(page_url)
                getPageNew(page_url, date,scrapperNew)
                date_1 = datetime.strptime(date, "%Y/%m/%d")
                date = date_1 + timedelta(days=1)
                date = datetime.strftime(date, "%Y/%m/%d")
                news_count = 0
            else:
                break

    except urllib2.HTTPError as err:
        if err.code == 404:
            print("error 404 at: ", page_url)
            date_1 = datetime.strptime(date, "%Y/%m/%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y/%m/%d")
            continue

        elif err.code == 500:
            print("urllib2.HTTPError: HTTP Error 500: Internal Server Error at link: ", page_url)
            time.sleep(2)
            continue

        else:
            i = 0
            while (i < 10):
                duration = 100  # millisecond
                freq = 1500  # Hz
                winsound.Beep(freq, duration)
                i += 1
                time.sleep(0.01)
            raise

    except urllib2.URLError as error:
        alarm(10,10)
        continue

    except:
        alarm(10,5)
        raise
        continue


