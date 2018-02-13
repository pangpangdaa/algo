from numpy import *
import pymysql


f=open('data.txt','w')

db=pymysql.connect("localhost","root","root","bookrec")
cursor=db.cursor()
    
sql="select user_id,book_id,score from comment;"
cursor.execute(sql)
data=cursor.fetchall()
n=0
for record in data:
    f.write(str(record[0])+'\t'+str(record[1])+'\t'+str(record[2])+'\n')
    n+=1
    if n%10000==0:
        print(n,'done')
f.close()
    



