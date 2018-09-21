import json
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
from datetime import datetime

date = '2017/01/01'
modified_date= datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")
news_count = 0



def getNews(url,modified_date):
    image_path = r'D:\kalerkontho\kalerKonthoImages_' + modified_date
    # if not os.path.exists(image_path):
    os.makedirs(image_path)
    newPath = 'D:/kalerkontho/kalerKonthoImages_' + modified_date
    result_items = []
    news_id = int(''.join(date.split('/')))
    global news_count
    img_count = str(news_count)
    news_page = urllib2.urlopen(url)
    soup = BeautifulSoup(news_page, 'html.parser')
    description_box= soup.find('div', attrs={'class': 'some-class-name2'})
    headline_box = soup.find('h2')
    #print(headline_box.text.strip())
    headline = headline_box.text.strip()
    # for p in description_box:
    #     print(p.text)

    for script in soup(["script"]):
        script.extract()
    #print(description_box.text.strip())

    description = description_box.text.strip()
    uniqueIdStr = str(news_id) + str(news_count)
    uniqueId = int(uniqueIdStr)
    ImgData = soup.findAll('meta', attrs={'property': 'og:image'})
    image_link = ''
    for meta in ImgData:
        image_link = (meta['content'])

    #print(image_link)

    source_dir_image = "D:/kalerkontho/" + modified_date + "_" + img_count + ".jpg"
    destination_dir_image = newPath + "/" + modified_date + "_" + img_count + ".jpg"
    file = open(modified_date + '_' + img_count + '.jpg', 'wb')
    file.write(urllib.urlopen(image_link).read())
    file.close()
    try:
        os.remove(destination_dir_image)
        print "Exception in no.", news_count
    except:
        print "All OK!!!"
    os.rename(source_dir_image, destination_dir_image)

    result_items.append({"Headline": headline, "News Date": modified_date,"News Unique Id":uniqueId,"Image Name": (modified_date + '_' + img_count + '.jpg'), "News Count": news_count, "News ID": news_id, "News Link": url, "News Description": description, "Image Link": image_link})
    news_count = news_count + 1
    json_data = json.dumps(result_items)
    with open("kalerKontho_output_" + modified_date + ".json", "w") as text_file:
        text_file.write(json_data)

getNews("http://kalerkantho.com/print-edition/rangberang/2017/01/01/447545",modified_date)



