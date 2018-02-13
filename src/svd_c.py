from __future__ import division  
import numpy as np  
import scipy as sp  
from numpy.random import random  
class  SVD_C:                               #建立SVD算法
    def __init__(self,X,k=20):  
        ''''' 
            k  is the length of vector 
        '''  
        self.X=np.array                   #传入样本
        self.k=k                          #k为特征数
        self.ave=np.mean(self.X[:,2])     #样本评分的平均值
        print ("the input data size is ",self.X.shape  )   
        self.bi={}                        
        self.bu={}  
        self.qi={}  
        self.pu={}  
        self.book_user={}  
        self.user_book={}  
        for i in range(self.X.shape[0]):  
            uid=self.X[i][0]                      
            mid=self.X[i][1]  
            rat=self.X[i][2]  
            #接下来初始化bi,bu,qi,pu.
            self.book_user.setdefault(mid,{})   
            self.user_book.setdefault(uid,{})  
            self.book_user[mid][uid]=rat  
            self.user_book[uid][mid]=rat  
            self.bi.setdefault(mid,0)  
            self.bu.setdefault(uid,0)  
            self.qi.setdefault(mid,random((self.k,1))/10*(np.sqrt(self.k)))  
            self.pu.setdefault(uid,random((self.k,1))/10*(np.sqrt(self.k)))  
    def pred(self,uid,mid):       #预测评分的函数
        #setdefault的作用是当该用户或者物品未出现过时，新建它的bi,bu,qi,pu，并设置初始值为0
        self.bi.setdefault(mid,0)       
        self.bu.setdefault(uid,0)  
        self.qi.setdefault(mid,np.zeros((self.k,1)))  
        self.pu.setdefault(uid,np.zeros((self.k,1)))  
        if (self.qi[mid].any()==None):  
            self.qi[mid]=np.zeros((self.k,1))  
        if (self.pu[uid].any()==None):  
            self.pu[uid]=np.zeros((self.k,1))  
        ans=self.ave+self.bi[mid]+self.bu[uid]+np.sum(self.qi[mid]*self.pu[uid])  #预测评分的公式
        if ans>5:           #由于评分范围在1到5，所以当分数大于5或小于1时，返回5,1.
            return 5  
        elif ans<1:  
            return 1  
        return ans  
    def train(self,steps=30,gamma=0.04,Lambda=0.15):    #训练函数，step为迭代次数。
        for step in range(steps):  
            print ('the ',step+1,'-th  step is running'  )
            rmse_sum=0.0  
            kk=np.random.permutation(self.X.shape[0])    #随机梯度下降算法，kk为对矩阵进行随机洗牌
            for j in range(self.X.shape[0]):  
                i=kk[j]  
                uid=self.X[i][0]  
                mid=self.X[i][1]  
                rat=self.X[i][2]  
                eui=rat-self.pred(uid,mid)  
                rmse_sum+=eui**2  
                self.bu[uid]+=gamma*(eui-Lambda*self.bu[uid])  #优化bu
                self.bi[mid]+=gamma*(eui-Lambda*self.bi[mid])   #优化bi
                temp=self.qi[mid]    
                self.qi[mid]+=gamma*(eui*self.pu[uid]-Lambda*self.qi[mid])   #优化qi
                self.pu[uid]+=gamma*(eui*temp-Lambda*self.pu[uid])   #优化pu
            gamma=gamma*0.93  #gamma以0.93的学习率递减
            print ("the rmse of this step on train data is ",np.sqrt(rmse_sum/self.X.shape[0])  )
            #self.test(test_data)  
    def test(self,test_X):  #对测试集进行测试
        output=[]  
        sums=0  
        test_X=np.array(test_X)  
        #print "the test data size is ",test_X.shape  
        for i in range(test_X.shape[0]):  
            pre=self.pred(test_X[i][0],test_X[i][1])  
            output.append(pre)  
            #print pre,test_X[i][2]  
            sums+=(pre-test_X[i][2])**2  
        rmse=np.sqrt(sums/test_X.shape[0])  
        print ("the rmse on test data is ",rmse)  
        return output  

def getData():   #获取训练集和测试集的函数
    import re
    f=open('C:/Users/xuwei/Desktop/train.txt','r')
    lines=f.readlines()
    f.close()
    train_X=[]
    for line in lines:
        list=re.split('\t|\n',line)
        train_X.append([int(i) for i in list[:3]])
    test_X=[]
    f=open('C:/Users/xuwei/Desktop/test.txt','r')
    lines=f.readlines()
    f.close()
    for line in lines:
        list=re.split('\t|\n',line)
        test_X.append([int(i) for i in list[:3]])
    print('data finished')
    return train_X,test_X
    
train_X,test_X=getData()
a=SVD_C(train_X,30)  
a.train()  
a.test(test_X)  