# coding=utf-8
import os
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as dummyPool

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

image_link = 'http://print.thesangbad.net/images/2017/August/12Aug17/fb_images/sangbad_today_1502539573.jpg'

myopener = MyOpener()
myopener.retrieve(image_link, 'hi.jpg')