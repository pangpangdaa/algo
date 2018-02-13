from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
from surprise import KNNBaseline
from surprise import Reader
from surprise import Dataset
from numpy import *
import pymysql
from pandas import Series,DataFrame


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
mat=algo.compute_similarities()
algo.
index=[]
len=shape(mat)[0]
for i in range(len):
        iid=trainset.to_raw_iid(i)
        index.append(iid)
columns=index
data=DataFrame(mat.tolist(),index=index,columns=columns)
data.to_csv('C:/Users/xuwei/workspace/Surprise/src/overlap.csv')
print('finished')
