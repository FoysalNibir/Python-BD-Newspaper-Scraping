import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta

date = '2017/11/22'
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

    result_items = []

    for data in soup.find_all('div', class_='archive'):
        for a in data.find_all('a'):
            news_url = (a.get('href')) # for getting link
            #news_url = (news_url[8:])
            news_url = "http://www.observerbd.com/" + news_url
            print(news_url)
            news_data = getNews(news_url,modified_date,news_count,path_4)
            result_items.append(news_data)
            news_count = news_count + 1

    dataInsert(result_items)
    dataUpdate(modified_date)

def getNews(url,modified_date,news_count,newPath):
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
    headline1 = headline_box1.text.strip()
    headline2 = headline_box2.text.strip()

    headline = headline1 + '  ' + headline2
    #print(headline)
    year = str(parse(modified_date, fuzzy=True).year)
    full_news = full_news_box.text.strip()
    #print(full_news)

    for data in soup.find_all('div', class_='pub'):
        entrytime='';
        for span in data.find_all('span'):
            entrytime = entrytime+" "+span.text.strip()

    # print(entrytime)
    # entrytime_box0 = soup.find('div', attrs={'style': 'color: #545353; margin: 0 0 10px 0'})
    # entrytime0 = entrytime_box0.text.strip()
    # entrytime_box1 = soup.find('font', attrs={'color': '#666666'})
    # entrytime1 = entrytime_box1.text.strip()
    # entrytime_box2 = soup.find('div', attrs={'style': 'font-size: 20px; color: #545353'})
    # entrytime2 = entrytime_box2.text.strip()
    # entrytime = entrytime2+ '  ' + entrytime0 + entrytime1
    summary_box = soup.findAll('meta', attrs={'property': 'og:description'})

    summary = ''
    for content in summary_box:
        summary = (content.get('content'))

    meta_data = headline + ' ' + summary

    category_box = soup.find('span', attrs={'class': 'location'})
    category = category_box.text.strip()

    #print(category)

    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])

    if(image_link == '.jpg"/' or image_link == 'http://www.observerbd.com/files/FB-Share.jpg'):
        db_img = ""

    # elif(image_link == 'http://www.observerbd.com/files/FB-Share.jpg'):
    #     db_img = ""

    else:
        image_link = image_link
        image_name = img_count + '.jpg'
        try:
            file = open(image_name, 'wb')
            file.write(urllib.urlopen(image_link).read())
            file.close()
            db_img = "observer_en/" + year + "/" + modified_date + "/" + image_name
            source_dir_image = "D:/daily_observer_en_demo/" + img_count + ".jpg"

            try:
                os.remove(newPath + "/" + img_count + ".jpg")
            except:
                pass

            destination_dir_image = newPath + "/" + img_count + ".jpg"
            os.rename(source_dir_image, destination_dir_image)

        except:
            os.remove(image_name)
            db_img = ""

    return (news_paper_id,category.encode("utf-8"),headline.encode("utf-8"),full_news.encode("utf-8"),entrytime.encode("utf-8"),modified_date.encode("utf-8"),db_img.encode("utf-8"),meta_data.encode("utf-8"))

def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "osint_demo"

    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB)
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
    THEDB = "osint_demo"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB)
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=6""",(date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")

while True:
    if (date < CurrentDate):
        year = str(parse(date, fuzzy=True).year)
        month = str(parse(date, fuzzy=True).month)
        day = str(parse(date, fuzzy=True).day)

        page_url = "http://www.observerbd.com/archive.php?" + "d=" + day + "&m=" + month + "&y=" + year
        getPage(page_url,date)
        date_1 = datetime.strptime(date, "%Y/%m/%d")
        date = date_1 + timedelta(days=1)
        date = datetime.strftime(date, "%Y/%m/%d")
        news_count = 0
    else:
        break


