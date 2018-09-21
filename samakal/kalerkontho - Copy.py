import json
import urllib
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import os

date = "2016/12/13"
page_url = "https://www.jugantor.com/today-print-edition/2016/12/13"
page = urllib.urlopen(page_url)
result_item=[]
soup = BeautifulSoup(page,'html.parser')
print(soup)
#news_links = [div.a for div in soup.findAll('div', attrs={'class' : 'col-xs-12'})]
#links='' [div.a for div in soup.findAll('div', attrs={'class' : 'col-xs-12'})]
count =0

# for script in soup(["h2"]):
#     script.extract()

for data in soup.find_all('div', class_='dailymn_inner'):
    for a in data.find_all('a'):
        print(a.get('href')) #for getting link
        print(a.text) #for getting text between the link
        count = count + 1
# for data in soup.find_all('a', style_='color:#d42028'):
#     print(data.get('href')) #for getting link
#     print(data.text) #for getting text between the link
#     count = count + 1

print(count)