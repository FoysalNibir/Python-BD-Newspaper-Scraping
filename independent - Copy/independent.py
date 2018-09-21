import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse

from datetime import datetime, timedelta



def getDate():
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "independent"
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

    date_1 = datetime.strptime(date, "%Y-%m-%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y-%m-%d")

    return date

def getMoreLinks(url,date):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    for data in soup.find_all('div', class_='more_news'):
        for a in data.find_all('a'):
            news_url = (a.get('href')) # for getting link
            news_url = "http://www.theindependentbd.com" + news_url[1:]
            getPage(news_url,date)

    dataUpdate(date)

def getPage(url,date):
    global news_count
    year = str(parse(date, fuzzy=True).year)
    result_items = []
    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/independent"
    if not os.path.exists(path_2):
        os.makedirs(path_2)

    path_3 = path_2 + "/" + year
    if not os.path.exists(path_3):
        os.makedirs(path_3)

    path_4 = path_3 + "/" + date
    if not os.path.exists(path_4):
        os.makedirs(path_4)

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    for data in soup.find_all('div', class_='span9'):
        for a in data.find_all('a'):
            news_url = (a.get('href')) # for getting link
            news_url = "http://www.theindependentbd.com" + news_url[1:]
            print(news_url)
            news_data = getNews(news_url, date, news_count, path_4)
            result_items.append(news_data)
            news_count = news_count +1

    dataInsert(result_items)

def getNews(url,date,news_count,newPath):
    id = 7
    news_paper_id = int(id)
    img_count = str(news_count)
    year = str(parse(date, fuzzy=True).year)
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
    if (headline_box3):
        headline3 = headline_box3.text.strip()
    else:
        headline3 = ''

    headline = headline1 + " " + headline2 + " " + headline3

    category_box = soup.find("div", {"class": "menu_name_details"})
    category = category_box.text.strip()

    author_box = soup.find("div", {"id": "rpt"})
    if (author_box):
        author = author_box.text.strip()
    else:
        author = ''

    update_time_box = soup.find("span", {"id": "news_update_time"})
    update_time = update_time_box.text.strip()

    entrytime = author + " " + update_time

    summary_box = soup.find('meta', attrs={'itemprop': 'description'})
    summary = summary_box.get('content')

    meta_data = headline + " " + summary
    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])

    if(image_link == "http://www.theindependentbd.com/assets/importent_images/icon.png"):
        db_img = ""
    else:
        image_link = image_link
        image_name = img_count + '.jpg'
        db_img = "independent/" + year + "/" + date + "/" + image_name
        try:
            file = open(image_name, 'wb')
            file.write(urllib.urlopen(image_link).read())
            file.close()
            source_dir_image = "D:/independent/" + img_count + ".jpg"

            try:
                os.remove(newPath + "/" + img_count + ".jpg")
            except:
                pass
            destination_dir_image = newPath + "/" + img_count + ".jpg"
            os.rename(source_dir_image, destination_dir_image)

        except:
            db_img=''
            source_dir_image = "D:/independent/" + img_count + ".jpg"
            try:
                os.remove(source_dir_image)
            except:
                pass
            print("problem in img link:",image_link)

    return (news_paper_id,headline,full_news,entrytime,date,db_img,meta_data)

def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "independent"

    db_connection = pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
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
    THEDB = "independent"

    db_connection = pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=7""",(date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")

def dataDelete(newspaper_id,date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "osint_demo"

    db_connection = pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""DELETE FROM newspapers WHERE newspaper_id=%s AND news_date=%s""",(newspaper_id,date))
    db_connection.commit()
    db_connection.close()
    print(" > Data deleted of: ",date, "id: ",newspaper_id)

if __name__ == '__main__':
    date = getDate()
    print('Starting Date: ',date)
    now = datetime.now()
    CurrentDate = now.strftime("%Y-%m-%d")
    news_count = 0
    newspaper_id = 7

    while True:
        if (date < CurrentDate):
            print('Now Scraping: ',date)
            page_url = "http://www.theindependentbd.com/arcprint/home/" + date
            dataDelete(newspaper_id, date)
            getMoreLinks(page_url,date)
            date_1 = datetime.strptime(date, "%Y-%m-%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y-%m-%d")
            news_count = 0
        else:
            break