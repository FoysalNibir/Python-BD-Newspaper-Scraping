import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as dummyPool


#date= datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")






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
    cursor.execute("""select end from papers where id=7""")
    date = cursor.fetchone()
    cursor.close()
    date=str(date[0])
    db_connection.close()

    date_1 = datetime.strptime(date, "%Y-%m-%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y-%m-%d")

    return date


date = getDate()
print date