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
    THEDB = "dailysangram"
    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=20""")
    date = cursor.fetchone()
    cursor.close()
    date = str(date[0])
    db_connection.close()

    date_1 = datetime.strptime(date, "%Y-%m-%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y-%m-%d")

    return date


class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


def makeDir(date):
    year = str(parse(date, fuzzy=True).year)

    path_1 = "D:/newspaper_images"
    if not os.path.exists(path_1):
        os.makedirs(path_1)

    path_2 = path_1 + "/dailysangram"
    if not os.path.exists(path_2):
        os.makedirs(path_2)

    path_3 = path_2 + "/" + year
    if not os.path.exists(path_3):
        os.makedirs(path_3)

    path_4 = path_3 + "/" + date
    if not os.path.exists(path_4):
        os.makedirs(path_4)

    return path_4


def getLinks(dateurl, date):
    global news_count
    global getNewsArgs
    site = dateurl
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(site, headers=hdr)

    datepage = urllib2.urlopen(req)
    soup = BeautifulSoup(datepage, 'html.parser')
    path = makeDir(date)

    for script in soup(["script"]):
        script.extract()

    for div in soup.find_all('p', class_='news-short-description'):
        for ahref in div.find_all('a'):
            news_link = (ahref.get('href'))
            length = len(news_link)
            end = 0

            for i in range(length):
                if news_link[i] == '-':
                    end = i
                    break

            news_link = news_link[:end]
            print news_link
            getNewsArgs.append([news_link, date, news_count, path])
            news_count += 1

    print news_count


def getNews(getNewsArgs):
    url = getNewsArgs[0]
    date = getNewsArgs[1]
    news_count = getNewsArgs[2]
    newPath = getNewsArgs[3]
    try:
        id = 20
        news_paper_id = int(id)
        img_count = str(news_count)
        site = url
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        req = urllib2.Request(site, headers=hdr)

        news_page = urllib2.urlopen(req)
        soupNews = BeautifulSoup(news_page.read().decode('utf-8', 'ignore'), 'html.parser')

        for script in soupNews(["script"]):
            script.extract()

        full_news_box = soupNews.find("div", {"class": "postBody"})
        full_news = full_news_box.text.strip()

        headline_box = soupNews.find('div', attrs={'class': 'postDetails'}).find('h1')
        headline = ''
        if headline_box:
            headline = headline_box.text.strip()
        # print headline, url

        year = str(parse(date, fuzzy=True).year)

        description_box = soupNews.findAll('meta', attrs={'property': 'og:description'})

        summary = ''
        for content in description_box:
            summary = (content.get('content'))

        meta_data = headline + ' ' + summary

        entrytime_box = soupNews.find('div', attrs={'class': 'postInfo'})
        entrytime = entrytime_box.text.strip()

        category_box = soupNews.find('ul', attrs={'class': 'breadcrumb'})
        category = category_box.text.strip()

        ImgData = soupNews.findAll('meta', attrs={'property': 'og:image'})
        image_link = ''

        for meta in ImgData:
            image_link = (meta['content'])

        if image_link == "http://www.dailysangram.com/images/the-daily-sangram.png":
            db_img = ""
            print 'Image Skipped'
        else:
            try:
                image_name = img_count + '.jpg'
                db_img = "dailysangram/" + year + "/" + date + "/" + image_name
                destination_dir_image = newPath + "/" + img_count + ".jpg"
                try:
                    os.remove(destination_dir_image)
                except:
                    pass

                print destination_dir_image
                myopener = MyOpener()
                myopener.retrieve(image_link, destination_dir_image)

            except:
                destination_dir_image = newPath + "/" + img_count + ".jpg"
                db_img = ''
                try:
                    os.remove(destination_dir_image)
                except:
                    pass
                print "problem in img link:", image_link

        return news_paper_id, category, headline, full_news, entrytime, date, db_img, meta_data
    except:
        print 'Problem in: ', url
        news_paper_id = 20
        category = ''
        headline = ''
        full_news = ''
        entrytime = ''
        db_img = ''
        meta_data = ''
        return news_paper_id, category, headline, full_news, entrytime, date, db_img, meta_data


def dataInsert(data):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "dailysangram"

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
    THEDB = "dailysangram"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""UPDATE papers SET end=%s WHERE id=20""", (date))
    db_connection.commit()
    db_connection.close()
    print(" > Date updated")


if __name__ == '__main__':
    date = getDate()
    print 'Starting date: ', date
    getNewsArgs = []
    now = datetime.now()
    CurrentDate = now.strftime("%Y-%m-%d")
    news_count = 0

    while True:

        if date < CurrentDate:
            print 'Now Scraping: ', date
            url = "http://www.dailysangram.com/page/first-page/" + date
            print(url)
            site = url
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}

            req = urllib2.Request(site, headers=hdr)

            datepage = urllib2.urlopen(req)
            soup = BeautifulSoup(datepage, 'html.parser')
            subnewslinks = []
            subnewslinks.append(url)
            for data in soup.find_all('ul', class_='subMenu'):
                for a in data.find_all('a'):
                    sub_news_url = (a.get('href'))
                    sub_news_url = 'http://www.dailysangram.com' + sub_news_url
                    sub_news_url = sub_news_url.replace(' ', '%20')
                    # if not sub_news_url == "http://www.dailysangram.com/page/eid-ul-fitor-2015":
                    #     print sub_news_url
                    #     subnewslinks.append(sub_news_url)
                    if not sub_news_url.find('eid-ul-fitor') != -1:
                        print sub_news_url
                        subnewslinks.append(sub_news_url)

            for val in subnewslinks:
                getLinks(val, date)

            print 'len', len(getNewsArgs)
            process_gateNews = dummyPool(40)
            result_items = process_gateNews.map(getNews, getNewsArgs)
            process_gateNews.close()
            process_gateNews.join()

            dataInsert(result_items)
            dataUpdate(date)
            process_gateNews.terminate()
            getNewsArgs = []
            print 'End of: ', date
            date_1 = datetime.strptime(date, "%Y-%m-%d")
            date = date_1 + timedelta(days=1)
            date = datetime.strftime(date, "%Y-%m-%d")
            news_count = 0
        else:
            break
