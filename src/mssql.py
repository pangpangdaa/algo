import pymysql

db=pymysql.connect("localhost","root","root","bi")
cursor=db.cursor()
def createSQL(empid,salary,month_key):
    sql="insert into salary2 (emp_no,month_key,salary) values ";
    for i in range(11):
        app="({},{},{}),".format(empid,month_key+i,salary)
        sql+=app
    app="({},{},{});".format(empid,month_key+11,salary)
    sql+=app
    return sql

def ins(empid,salary,year,month):
    salary=salary/12
    cursor.execute("select month_key from month_dim where month={} and year={}".format(month,year))
    month_key=int(cursor.fetchone()[0])
    sql=createSQL(empid, salary, month_key)
    print(sql)
    cursor.execute(sql)
    db.commit()

sql="select * from salaries;"
cursor.execute(sql)
records=cursor.fetchall()
for record in records:
    empid=record[0]
    salary=record[1]
    year=record[2].year
    month=record[2].month
    print(year,month)
    ins(empid,salary,year,month)