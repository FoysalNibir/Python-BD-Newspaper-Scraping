import json
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import datetime
from datetime import datetime
import pymysql
from itertools import groupby
from dateutil.parser import parse


#date= datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")






def dataDelete(newspaper_id,date):
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "test"

    db_connection = pymysql.connect(host=THEHOST, user=THEUSER, passwd=THEPASSWD, db=THEDB)
    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""SELECT meta FROM newspapers WHERE newspaper_id=%s AND news_date=%s""",(newspaper_id,date))
    row = cursor.fetchone()
    print row
    db_connection.commit()
    db_connection.close()
    print(" > Data deleted")

dataDelete(6,'2017-11-30')