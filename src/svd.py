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

#data = Dataset.load_builtin('ml-100k')
db=pymysql.connect("localhost","root","root","bookRec")
cursor=db.cursor()
    
file_path = os.path.expanduser('C:/Users/xuwei/workspace/Surprise/src/data.txt')
reader = Reader(line_format='user item rating', sep='\t')

data = Dataset.load_from_file(file_path, reader=reader)
trainset = data.build_full_trainset()

algo = SVDpp()



# Evaluate performances of our algorithm on the dataset.
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])

print_perf(perf)

