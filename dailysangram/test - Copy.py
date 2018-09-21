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



my_string="প্রচ্ছদ›আর্কাইভ›০১/০১/২০১৮›প্রথমপাতা"
print my_string.split(">",1)[1]
