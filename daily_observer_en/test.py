import pymysql
import string
from datetime import datetime, timedelta



# date = "2017-01-01"
# date_1 = datetime.strptime(date, "%Y-%m-%d")
# print(date_1)
def getDate():
    THEHOST = "localhost"
    THEUSER = "root"
    THEPASSWD = ""
    THEDB = "osint_demo"
    db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB,charset='utf8')
    db_connection.commit()

    if db_connection:
        print ("connected")
    else:
        print("connection fucked up")

    cursor = db_connection.cursor()
    cursor.execute("""select end from papers where id=6""")
    date = cursor.fetchone()
    cursor.close()
    date=str(date[0])
    db_connection.close()

    date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y/%m/%d")
    date_1 = datetime.strptime(date, "%Y/%m/%d")
    date = date_1 + timedelta(days=1)
    date = datetime.strftime(date, "%Y/%m/%d")

    return date


date = getDate()
print('Starting date=',date)

