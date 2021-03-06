import json
import urllib
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from datetime import datetime, timedelta

path_to_chrome = "chromedriver"
driver = webdriver.Chrome(executable_path=path_to_chrome)
start_date = '2013-11-09'
news_count = 0
now = datetime.now()
CurrentDate = now.strftime("%Y-%m-%d")

def load(date):
    #date = '2017-11-10'
    news_id = int(''.join(date.split('-')))
    g_url = "http://www.prothom-alo.com/archive/" + date

    driver.get(g_url)

    result_items = []

    image_path = r'D:\work\osint\newspaper\prothomAloImages_'+date
    #if not os.path.exists(image_path):
    os.makedirs(image_path)
    newPath = 'D:/work/osint/newspaper/prothomAloImages_'+date


    def extractData():
        count = 0
        global news_count
        all_headings = driver.find_elements_by_xpath("//h2[@class='title_holder']")
        h2_links = driver.find_elements_by_xpath("//a[@class='link_overlay']")

        for h2 in all_headings:
            img_count = str(news_count)
            url = h2_links[count].get_attribute("href")
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            description_box = soup.find('div', attrs={'itemprop': 'articleBody'})
            description = description_box.text.strip()
            image_link=''
            ImgData = soup.findAll('meta', attrs={'property': 'og:image'})

            for meta in ImgData:
                image_link = (meta['content'])

            source_dir_image = "D:/work/osint/newspaper/" + date + "_" + img_count + ".jpg"
            destination_dir_image = newPath +"/"+ date + "_" + img_count + ".jpg"
            file = open(date + '_' + img_count + '.jpg', 'wb')
            file.write(urllib.urlopen(image_link).read())
            file.close()

            try:
                os.remove(destination_dir_image)
                print "Exception in no.", news_count
            except:
                print "All OK!!!"

            os.rename(source_dir_image, destination_dir_image)
            uniqueIdStr=str(news_id)+str(news_count)
            uniqueId = int(uniqueIdStr)
            result_items.append({"Headline":h2.text,"News Date": date,"News Count":news_count,"News ID":news_id,"News Unique Id":uniqueId,"News Link":h2_links[count].get_attribute("href"),"News Description":description,"Image Link":image_link})
            count = count+1
            news_count = news_count + 1

    extractData()

    while True:
        try:
            elem = driver.find_element_by_xpath('//a[@class="next_page"]')
            elem = driver.find_element_by_xpath('//a[@class="next_page"]').click()
            extractData()
        except:
            break

    json_data = json.dumps(result_items)

    with open("prothomAlo_output_"+date+".json", "w") as text_file:
        text_file.write(json_data)



while True:
    try:
        if (start_date < CurrentDate):
            date_1 = datetime.strptime(start_date, "%Y-%m-%d")
            start_date = date_1 + timedelta(days=1)
            start_date = datetime.strftime(start_date, "%Y-%m-%d")
            load(start_date)
            news_count = 0
        else:
            break
    except:
        print("error at:", start_date)
        pass
