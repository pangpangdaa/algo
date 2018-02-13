from numpy import *
import numpy
from pandas import Series,DataFrame
import pymysql
import pandas as pd
import numpy as np

def generateMatrix():
    db=pymysql.connect("localhost","root","root","bookRec")
    cursor=db.cursor()
    sql="select user_id,book_id,score from comment limit 1000;"   #取出所有的用户id，书籍id，评分
    cursor.execute(sql)
    data=cursor.fetchall()
    db.close()
    frame=DataFrame()               #建立矩阵
    n=0
    for item in data:
        n+=1
        print(n)               #向矩阵中增加值，矩阵会自动扩大
        frame.loc[item[1],item[0]]=item[2]
    return mat(frame.as_matrix())
    


def svd(mat, feature, steps=500, gama=0.02, lamda=0.3):  
    slowRate = 0.99  
    preRmse = 1000000000.0  
    nowRmse = 0.0  
  
    p = numpy.matrix(numpy.random.rand(mat.shape[0], feature))  
    q = numpy.matrix(numpy.random.rand(mat.shape[1], feature))  
    bu = numpy.matrix(zeros((mat.shape[0],1)))
    bi = numpy.matrix(zeros((mat.shape[1],1)))
    print(shape(bu))
    print(shape(bi))
    u=numpy.average(mat)
    
  
    for step in range(steps):  
        rmse = 0.0    
        n = 0    
        for u in range(mat.shape[0]):  
            for i in range(mat.shape[1]):  
                if not numpy.isnan(mat[u,i]):  
                    pui = float(numpy.dot(p[u,:], q[i,:].T))  
                    eui = mat[u,i]-(u+bu[u]+bi[i]+pui)  
                    #eui=mat[u,i]-(u+pui)
                    rmse += pow(eui, 2)  
                    n += 1   
                    for k in range(feature):  
                        p[u,k] += gama*(eui*q[i,k] - lamda*p[u,k])  
                        q[i,k] += gama*(eui*p[u,k] - lamda*q[i,k]) 
                    
                    bi[i] +=  gama*(eui - lamda*bi[i])
            bu[u] +=  gama*(eui - lamda*bu[u])            
        nowRmse = sqrt(rmse * 1.0 / n)  
        print ('step: %d      Rmse: %s' % ((step+1), nowRmse))  
        if (nowRmse < preRmse):    
            preRmse = nowRmse  
        else:  
            break # 这个退出条件其实还有点问题  
        gama *= slowRate  
        step += 1  
  
    return p,q,bu,bi,u

def svdT(mat, feature, steps=500, gama=0.02, lamda=0.3):  
    slowRate = 0.99  
    preRmse = 1000000000.0  
    nowRmse = 0.0  
  
    user_feature = numpy.matrix(numpy.random.rand(mat.shape[0], feature))  
    item_feature = numpy.matrix(numpy.random.rand(mat.shape[1], feature))  
  
    for step in range(steps):  
        rmse = 0.0    
        n = 0    
        for u in range(mat.shape[0]):  
            for i in range(mat.shape[1]):  
                if not numpy.isnan(mat[u,i]):  
                    pui = float(numpy.dot(user_feature[u,:], item_feature[i,:].T))  
                    eui = mat[u,i] - pui  
                    rmse += pow(eui, 2)  
                    n += 1   
                    for k in range(feature):  
                        user_feature[u,k] += gama*(eui*item_feature[i,k] - lamda*user_feature[u,k])  
                        item_feature[i,k] += gama*(eui*user_feature[u,k] - lamda*item_feature[i,k]) # 原blog这里有错误   
  
        nowRmse = sqrt(rmse * 1.0 / n)  
        print ('step: %d      Rmse: %s' % ((step+1), nowRmse))  
        if (nowRmse < preRmse):    
            preRmse = nowRmse  
        else:  
            break # 这个退出条件其实还有点问题  
        gama *= slowRate  
        step += 1  
  
    return user_feature, item_feature  

mat=generateMatrix()
print('mat generated')
svdT(mat,10)
#print(p,q,bu,bi,u)


class SVD_C:
    def __init__(self,X,k=20):
        self.X=np.array(X)
        self.k=k 
        self.ave=np.mean(self.X[:,2])
        print("the input data size is ",self.X.shape)
        self.bi={}
        self.bu={}
        self.qi={}
        self.pu={}
        self.