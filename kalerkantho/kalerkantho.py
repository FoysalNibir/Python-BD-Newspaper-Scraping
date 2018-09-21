import urllib2
import pymysql
from bs4 import BeautifulSoup
from datetime import datetime


def getPage(url):
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
    for tag in soup.find_all('td', attrs={'class': 'first-td'}):
        tag.replaceWith('')
    for tag2 in soup.find_all('td', attrs={'class': 'last-td'}):
        tag2.replaceWith('')

    inc = 0
    for data in soup.find_all('tbody'):
        for table in data.find_all('tr'):
            link = table.find('td', attrs={'class': 'col-md-4'})
            for a in link.find_all('a', href=True):
                link = a['href']
            for td in table.find_all('td'):
                if inc == 0:
                    sro_no = td.text.strip()
                    inc = inc + 1
                    continue
                if inc == 1:
                    date = td.text.strip()
                    inc = inc + 1
                    if date:
                        datetime_object = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
                    else:
                        datetime_object = "0000-00-00"
                    continue
                if inc == 2:
                    description = td.text.strip()
                    inc = inc + 1
                    continue
                if inc == 3:
                    amended_by = td.text.strip()
                    if not amended_by:
                        amended_by = ""
                    inc = 0
                    break
            dataInsert(sro_no, datetime_object, description, amended_by, link)


def dataInsert(sro_no, date, description, amended_by, link):
    data = [
        (sro_no, date, description, amended_by, link)
    ]
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "tariff"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB, charset='utf8')
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.executemany("INSERT INTO sros (sro_no,date,description,amended_by,link) VALUES (%s, %s, %s, %s, %s)",data)
    db_connection.commit()
    db_connection.close()
    print(" > Data Inserted")


if __name__ == '__main__':
    count = 0
    while True:
        # try:
            if count < 281:
                page_url = "http://nbr.gov.bd/regulations/sros/customs-sros/" + str(count) + "/eng"
                print 'Now Scraping =', page_url
                getPage(page_url)
                count = count + 40
            else:
                break
        # except:
        #     print('Error at: ', count)
        #     pass
