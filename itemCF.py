# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 21:43:44 2018

@author: Administrator
"""
from numpy import *
import json
def pearson(data,i,j,m):   #皮尔逊相关系数计算
    tmpxy=0
    tmpx=0
    tmpy=0
    tmpxx=0
    tmpyy=0
    tmpp=0
    for k in range(m):
        if (data[i][k]==0)|(data[j][k]==0):
            continue
        tmpxy=float(tmpxy+data[i][k]*data[j][k])
        tmpx=float(tmpx+data[i][k])
        tmpy=float(tmpy+data[j][k])
        tmpxx=float(tmpxx+data[i][k]*data[i][k])
        tmpyy=float(tmpyy+data[j][k]*data[j][k])
        tmp1=float(tmpxy-tmpx*tmpy/m)
        tmp2=sqrt((tmpxx-tmpx*tmpx/m)*(tmpyy-tmpy*tmpy/m))
        tmpp=tmp1/tmp2
    
    return tmpp

def item_CF(data,docs,docs1,docs2):#评分矩阵 全体电影名称 已选电影名称 已选电影评分
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]==' ':
                continue
            data[i][j] = float(data[i][j])

    n = len(data)
    m = len(data[1])
    #n行 m列
    #元素 评分1 评分2 评分3 评分4...
    pearsonnum=[]
    '''for i in range(n):
        pearsonnum1=[]
        for j in range(i):
            tmp=pearson(data,i,j,m)
            pearsonnum1.append(tmp)
        pearsonnum.append(pearsonnum1)
    f = open("pearson.txt","w")
    JSON_STR = json.dumps(pearsonnum)
    f.write(JSON_STR)
    f.close()
    print('保存成功')'''
    f = open("pearson.txt","r")
    JSON_STR = f.read()
    f.close()
    pearsonnum = json.loads(JSON_STR)
    for i in range(len(docs2)):
            docs2[i] = float(docs2[i])
            
    choosenum=[]   #选择电影的编号
    vis=[]
    for i in range(n):
        vis.append(0)
    for i in range(n):
        for j in range(len(docs1)):
            if docs1[j]==docs[i]:
                choosenum.append(i)
                vis[i]=1
                break
    rec=[]
    for i in range(n):   #未选电影的编号 预测评分
        rec.append([i,0])
    for i in range(n):
        if vis[i]==1:
            continue
        for j in range(len(choosenum)):
            tmp=float((docs2[j])*(pearsonnum[max(i,choosenum[j])][min(i,choosenum[j])]))
            rec[i][1]+=tmp
    rec.sort(key=lambda x:x[1],reverse=True)
    templist = []
    for i in range(72):
        if rec[i][1]<0:
            break
        if vis[rec[i][0]]==0:
            templist.append(docs[rec[i][0]])
    for i in range(len(docs1)):
        templist.append(docs1[i])
    return templist
