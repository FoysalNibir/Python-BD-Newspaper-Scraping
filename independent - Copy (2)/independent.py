import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as dummyPool

def makeDir(date):
    year = str(parse(date, fuzzy=True).year)

    path_1 = "D:/test_images"
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

    return path_4

def getDate():
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "test"
    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
        print 'Database Name: ', THEDB
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=7""")
    date = cursor.fetchone()
    cursor.close()
    date = str(date[0])
    db_connection.close()

    date_1 = datetime.strptime(date, "%Y-%m-%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y-%m-%d")

    return date


def getMoreLinks(url, date):
    global news_count
    path = makeDir(date)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    # getPageArgs = []
    getNewsArgs = []
    result_items = []
    process_getMoreLinks = dummyPool(40)

    for data in soup.find_all('div', class_='more_news'):
        for a in data.find_all('a'):
            moreNews_url = (a.get('href'))  # for getting link
            moreNews_url = "http://www.theindependentbd.com" + moreNews_url[1:]
            # print(moreNews_url)
            # getPage(news_url,date)
            more_page = urllib2.urlopen(moreNews_url)
            more_soup = BeautifulSoup(more_page, 'html.parser')
            for more_data in more_soup.find_all('div', class_='span9'):
                for ahref in more_data.find_all('a'):
                    news_url = (ahref.get('href'))  # for getting link
                    news_url = "http://www.theindependentbd.com" + news_url[1:]
                    print(news_url)
                    getNewsArgs.append([news_url, date, news_count, path])
                    # news_data = getNews(news_url, date, news_count, path_4)
                    # result_items.append(news_data)
                    news_count = news_count + 1
            # getPageArgs.append([moreNews_url, date, path])

    print news_count
    result_items.append(process_getMoreLinks.map(getNews, getNewsArgs))
    process_getMoreLinks.close()
    process_getMoreLinks.join()
    process_getMoreLinks.terminate()

    # for i in xrange(len(getPageArgs)):
    #     getPage(getPageArgs[i])
    dataInsert(result_items)
    dataUpdate(date)



# def getPage(getPageArgs):
#     global news_count
#     url = getPageArgs[0]
#     date = getPageArgs[1]
#     path = getPageArgs[2]
#
#     page = urllib2.urlopen(url)
#     soup = BeautifulSoup(page, 'html.parser')
#     getNewsArgs = []
#     process_gatePage = dummyPool(20)
#
#     for data in soup.find_all('div', class_='span9'):
#         for a in data.find_all('a'):
#             news_url = (a.get('href'))  # for getting link
#             news_url = "http://www.theindependentbd.com" + news_url[1:]
#             print(news_url)
#             getNewsArgs.append([news_url, date, news_count, path])
#             # news_data = getNews(news_url, date, news_count, path_4)
#             # result_items.append(news_data)
#             news_count = news_count + 1
#
#     print(news_count)
#     result_items = process_gatePage.map(getNews, getNewsArgs)
#     process_gatePage.close()
#     process_gatePage.join()
#
#     dataInsert(result_items)
#     process_gatePage.terminate()


def getNews(getNewsArgs):
    url = getNewsArgs[0]
    # print '\n Now Scraping: ', url, '\n'
    news_date = getNewsArgs[1]
    getNews_count = getNewsArgs[2]
    newPath = getNewsArgs[3]

    intId = 7
    news_paper_id = int(intId)
    img_count = str(getNews_count)
    year = str(parse(news_date, fuzzy=True).year)

    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')

    full_news_box = soup.find("div", {"id": "newsDtl"}).findAll('p')
    full_news = ''
    for element in full_news_box:
        full_news += '\n' + ''.join(element.findAll(text=True))

    headline_box1 = soup.find("div", {"id": "hl1"})
    if headline_box1:
        headline1 = headline_box1.text.strip()
    else:
        headline1 = ''

    headline_box2 = soup.find("div", {"id": "hl2"}).find('h2')
    if headline_box2:
        headline2 = headline_box2.text.strip()
    else:
        headline2 = ''

    headline_box3 = soup.find("div", {"id": "hl3"})
    if headline_box3:
        headline3 = headline_box3.text.strip()
    else:
        headline3 = ''

    headline = headline1 + " " + headline2 + " " + headline3

    category_box = soup.find("div", {"class": "menu_name_details"})
    category = category_box.text.strip()

    author_box = soup.find("div", {"id": "rpt"})
    if author_box:
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

    if image_link == "http://www.theindependentbd.com/assets/importent_images/icon.png":
        db_img = ""
    else:
        try:
            image_link = image_link
            image_name = img_count + '.jpg'
            db_img = "independent/" + year + "/" + news_date + "/" + image_name
            destination_dir_image = newPath + "/" + img_count + ".jpg"
            try:
                os.remove(destination_dir_image)
            except:
                pass

            print destination_dir_image
            urllib.urlretrieve(image_link, destination_dir_image)

        except:
            destination_dir_image = newPath + "/" + img_count + ".jpg"
            db_img = ''
            try:
                os.remove(destination_dir_image)
            except:
                pass
            print("problem in img link:", image_link)

    return (news_paper_id, category, headline, full_news, entrytime, news_date, db_img, meta_data)


def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "test"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
        print 'Database Name: ', THEDB
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.executemany(
        "INSERT INTO newspapers (newspaper_id,category,headline,details,entrytime,news_date,img,meta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        data)
    db_connection.commit()
    db_connection.close()
    print(" > Data Inserted")


def dataUpdate(date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "test"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
        print 'Database Name: ', THEDB
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=7""", (date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")


def dataDelete(newspaper_id, date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "test"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
        print 'Database Name: ', THEDB
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""DELETE FROM newspapers WHERE newspaper_id=%s AND news_date=%s""", (newspaper_id, date))
    db_connection.commit()
    db_connection.close()
    print 'Data deleted of: ', date, ', id: ', newspaper_id


if __name__ == '__main__':
    date = getDate()
    print 'Starting Date: ', date
    now = datetime.now()
    CurrentDate = now.strftime("%Y-%m-%d")
    news_count = 0
    newspaper_id = 7

    while True:
        if date < CurrentDate:
            print 'Now Scraping: ', date
            dataDelete(newspaper_id, date)
            page_url = "http://www.theindependentbd.com/arcprint/home/" + date + '\n'
            print 'Archive url: ', page_url
            getMoreLinks(page_url, date)
            date_1 = datetime.strptime(date, "%Y-%m-%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y-%m-%d")
            news_count = 0
        else:
            break
