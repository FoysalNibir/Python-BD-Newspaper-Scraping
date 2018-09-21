import os
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
    THEDB = "bhorerkagoj"
    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=16""")
    date = cursor.fetchone()
    cursor.close()
    date = str(date[0])
    db_connection.close()

    date_1 = datetime.strptime(date, "%Y-%m-%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y-%m-%d")

    return date


def makeDir(date):
    year = str(parse(date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/bhorerkagoj"
    if not os.path.exists(path_2):
        os.makedirs(path_2)

    path_3 = path_2 + "/" + year
    if not os.path.exists(path_3):
        os.makedirs(path_3)

    path_4 = path_3 + "/" + date
    if not os.path.exists(path_4):
        os.makedirs(path_4)

    return path_4


def getLinks(soup, date):
    global news_count
    global getNewsArgs
    path = makeDir(date)

    for script in soup(["script"]):
        script.extract()

    # getNewsArgs = []

    for data in soup.find_all('div', class_='col-sm-6 col-xs-12'):
        for a in data.find_all('a'):
            news_link = (a.get('href'))

        print(news_link)
        # getNewsArgs.append([news_link, date, news_count, path])
        # news_data = getNews(news_link,date,news_count,path_4)
        # result_items.append(news_data)
        getNewsArgs.append([news_link, date, news_count, path])
        news_count += 1

    print news_count


def getNews(getNewsArgs):
    url = getNewsArgs[0]
    date = getNewsArgs[1]
    news_count = getNewsArgs[2]
    newPath = getNewsArgs[3]

    id = 16
    news_paper_id = int(id)
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soupNews = BeautifulSoup(news_page, 'html.parser')

    for script in soupNews(["script"]):
        script.extract()

    # full_news_box = soupNews.find('div', attrs={'class': 'description'})
    # full_news = full_news_box.text.strip()

    full_news_box = soupNews.find("div", {"id": "content-p"}).find_all('p')
    full_news = ''
    for element in full_news_box:
        full_news += '\n' + ''.join(element.findAll(text=True))

    headline_box = soupNews.find('h2', attrs={'class': 'title'})
    headline = headline_box.text.strip()

    year = str(parse(date, fuzzy=True).year)

    description_box = soupNews.findAll('meta', attrs={'property': 'og:description'})

    summary = ''
    for content in description_box:
        summary = (content.get('content'))

    meta_data = headline + ' ' + summary

    entrytime_box = soupNews.find('p', attrs={'class': 'post_bar'})
    entrytime = entrytime_box.text.strip()

    category_box = soupNews.findAll('a', attrs={'rel': 'category tag'})
    category = ''
    for rel in category_box:
        category += '>' + ''.join(rel.findAll(text=True))

    ImgData = soupNews.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''

    for meta in ImgData:
        image_link = (meta['content'])

    # if image_link == "http://bhorerkagoj.com/assets/images/default_news.jpg":
    #     db_img = ""
    # else:
    try:
        # image_link = image_link
        image_name = img_count + '.jpg'
        db_img = "bhorerkagoj/" + year + "/" + date + "/" + image_name
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
        print "problem in img link:", image_link

    return news_paper_id, category, headline, full_news, entrytime, date, db_img, meta_data


def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "bhorerkagoj"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
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
    THEDB = "bhorerkagoj"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=16""", (date))
    db_connection.commit()
    db_connection.close()
    print(" > Data updated")


# def dataDelete(newspaper_id, date):
#     THEHOST = "localhost"
#     THEUSER = "root"
#     THEPASSWD = ""
#     THEDB = "bhorerkagoj"
#
#     db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
#     if db_connection:
#         print ("connected")
#     else:
#         print("connection fucked up")
#
#     cursor = db_connection.cursor()
#     cursor.execute("""DELETE FROM newspapers WHERE newspaper_id=%s AND news_date=%s""", (newspaper_id, date))
#     db_connection.commit()
#     db_connection.close()
#     print(" > Data deleted")

if __name__ == '__main__':
    date = getDate()
    print 'Starting date=', date
    getNewsArgs = []
    now = datetime.now()
    CurrentDate = now.strftime("%Y-%m-%d")
    news_count = 0

    while True:

        if date < CurrentDate:
            # dataDelete(16, date)
            inc = 1
            while True:

                url_date = datetime.strptime(date, "%Y-%m-%d")
                url_date = datetime.strftime(url_date, "%Y/%m/%d")

                if inc < 2:
                    url = "http://www.bhorerkagoj.net/" + url_date + "/"

                else:
                    url = "http://www.bhorerkagoj.net/" + url_date + "/page/" + str(inc) + "/"

                print(url)
                existance = urllib2.urlopen(url)
                soup = BeautifulSoup(existance, 'html.parser')

                check = soup.find('i', class_='fa fa-chevron-right')

                if not check:
                    getLinks(soup, date)
                    inc = 1
                    break
                else:
                    getLinks(soup, date)

                inc += 1

            print news_count
            # print getNewsArgs
            # print len(getNewsArgs)
            process_gateNews = dummyPool(40)
            result_items = process_gateNews.map(getNews, getNewsArgs)
            process_gateNews.close()
            process_gateNews.join()

            dataInsert(result_items)
            dataUpdate(date)
            process_gateNews.terminate()
            getNewsArgs = []

            date_1 = datetime.strptime(date, "%Y-%m-%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y-%m-%d")
            news_count = 0
        else:
            break
