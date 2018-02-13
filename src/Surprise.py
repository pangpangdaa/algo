from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
from surprise import KNNBaseline
from surprise import Reader
from surprise import Dataset
from numpy import *
import pymysql
'''
计算相似度的代码
'''
#data = Dataset.load_builtin('ml-100k')
db=pymysql.connect("localhost","root","root","bookRec")
cursor=db.cursor()
    
file_path = os.path.expanduser('C:/Users/xuwei/workspace/Surprise/src/data.txt')
reader = Reader(line_format='user item rating', sep='\t')

data = Dataset.load_from_file(file_path, reader=reader)

trainset = data.build_full_trainset()
    #使用pearson_baseline方式计算相似度  False以item为基准计算相似度 本例为电影之间的相似度
sim_options = {'name': 'pearson_baseline', 'user_based': False}
    ##使用KNNBaseline算法
algo = KNNBaseline(sim_options=sim_options)
#algo=KNNBaseline()
    #训练模型
algo.train(trainset)

n=0
for item in range(trainset.n_items):
    raw_id=trainset.to_raw_iid(item)
    neighbors=algo.get_neighbors(item, 5)
    for neighbor in neighbors:
        neighbor_raw_id=trainset.to_raw_iid(neighbor)
        sql="insert into book_similarity_icf(book_id1,book_id2) values('%d','%d');" % (int(raw_id),int(neighbor_raw_id))
        print(sql)
        cursor.execute(sql)
        db.commit()
        n+=1
        if(n%100==0):
            print('----------------')
            print(n,'is done')
db.close()
    

