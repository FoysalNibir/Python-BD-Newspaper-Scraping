import os
import time
import urllib
import urllib2
import pymysql
from bs4 import BeautifulSoup
from dateutil.parser import parse
from multiprocessing import Process
from datetime import datetime, timedelta
from MultiScrappingV2 import MultiScrapper

class Simple(object):
    def one(self):
        print "http://kalerkantho.com/print-edition/"

    def two(self,two):
        print "two" + two

    def three(self):
        print "three"

class Wrapper(object):
    def __init__(self,wrapped_class):
        self.wrapped_class = wrapped_class()

    def __getattr__(self,attr):
        orig_attr = self.wrapped_class.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                self.pre()
                result = orig_attr(*args, **kwargs)
                # prevent wrapped_class from becoming unwrapped
                if result == self.wrapped_class:
                    return self
                self.post()
                return result
            return hooked
        else:
            return orig_attr

    def pre(self):
        print ">> pre"

    def post(self):
        print "<< post"

number = Wrapper(Simple)

print "\nCalling wrapped 'one':"
number.one()

print "\nCalling wrapped 'two':"
number.two("2")