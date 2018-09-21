import pymysql
import string

THEHOST = "localhost"
THEUSER = "root"
THEPASSWD = ""
THEDB = "osint"

# date = "2017-01-01"
# date_1 = datetime.strptime(date, "%Y-%m-%d")
# print(date_1)

db_connection=pymysql.connect(host=THEHOST,user=THEUSER,passwd=THEPASSWD,db=THEDB)
# if db_connection:
#     print ("connected")
# else:
#     print("connection fucked up")
#data = ['kalerkontho','2015-01-01','2016-01-01']

cursor = db_connection.cursor()
#cursor.execute("INSERT INTO papers (name,start,end) VALUES (%s, %s, %s)",data)

cursor.execute("""select end from papers where id=4""")

#print("{:%Y %m %d}".format(date))

#It is going to fetch the executed mysql query into rows.
#Hence assigning it to row
row = cursor.fetchall()
row2 = str(row[0])
data1 = (row2[15:-3])
data2 = string.replace(data1, ', ', '-')

print data2
#printing the result
#print row
#date_2 = datetime.strptime(row2, "%Y,%m,%d")
print (row2)

# if (datetime.date_1 < row[0]):
#     print("great")
# else:
#     print("bal")


#print(row[0])

#closing the function
cursor.close()
#var = cursor.execute(sqlstmt, {'id': 4})
db_connection.commit()
db_connection.close()
#print(" > Data Inserted")

