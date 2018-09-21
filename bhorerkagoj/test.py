# coding=utf-8
import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as dummyPool

import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

url = 'http://www.bhorerkagoj.net/wp-content/uploads/2018/01/Dr-‍s-a-malek-1.jpg'
urllib.urlretrieve(url, "local-filename.jpg")
# url = str(url)
# resource = urllib.urlopen(url)
# output = open("file01.jpg", "wb")
# output.write(resource.read())
# output.close()