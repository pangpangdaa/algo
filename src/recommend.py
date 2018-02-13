from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
from surprise import KNNBaseline
from surprise import SVD
from surprise import Reader
from surprise import SVDpp
from surprise import Dataset
from surprise import evaluate, print_perf
from numpy import *
import pymysql
from datetime import datetime


'''

推荐系统服务器
SVD++模型训练算法
实时预测推荐函数
'''
from flask import Flask
app = Flask(__name__)

#data = Dataset.load_builtin('ml-100k')
db=pymysql.connect("localhost","root","root","bookRec")
cursor=db.cursor()
    
file_path = os.path.expanduser('C:/Users/xuwei/workspace/Surprise/src/data.txt')
reader = Reader(line_format='user item rating', sep='\t')

data = Dataset.load_from_file(file_path, reader=reader)
trainset = data.build_full_trainset()
print('start training')
starttime=datetime.now()
algo = SVDpp()
algo.train(trainset)
endtime=datetime.now()
print('finished total time',endtime-starttime)
def getRec(id,algo):
    list={}
    uid=trainset.to_inner_uid(str(id))
    for i in range(trainset.n_items):
        list[trainset.to_raw_iid(i)]=algo.estimate(uid,i)
    list=sorted(list.items(),key=lambda jj:jj[1],reverse=True)[:6]
    print(list)
    return list

def saveRec(id,array):
    for bookid in array:
        sql="insert into recommend (user_id,book_id,rating) values('%d','%d','%d');" % (int(id),int(bookid[0]),int(bookid[1]))
        cursor.execute(sql)
        db.commit()
    return [r[0] for r in array]

def Recommend(id,algo):
    sql="select book_id from recommend where user_id='%d';" % int(id)
    print(sql)
    cursor.execute(sql)
    records=cursor.fetchall()
    if len(records)==0:
        list=getRec(id, algo)
        return saveRec(id,list)
    else:
        print(records)
        return [r[0] for r in records]



@app.route("/recommend/<id>")
def show_hello(id):
    rec=Recommend(id, algo)
    back=""
    for r in rec:
        back+=str(r)+'\t'
    print(back)
    return back

if __name__ == '__main__':
    app.run(debug=True)
        