# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 00:05:04 2018

@author: Administrator
"""

from numpy import *

# 计算欧几里得距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) # 求两个向量之间的距离

# 构建聚簇中心，取k个(此例中为4)随机质心
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))   # 每个质心有n个坐标值，总共要k个质心
    for j in range(n):
        minJ = min(dataSet[:,j])
        maxJ = max(dataSet[:,j])
        rangeJ = float(maxJ - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
    return centroids

# k-means 聚类算法
def kMeans(dataSet, k):
    m = shape(dataSet)[0]   #电影个数
    n = shape(dataSet)[1]   #评价元素个数
    division = mat(zeros((m,2)))    # 用于存放该样本属于哪类及质心距离
    # clusterAssment第一列存放该数据所属的中心点，第二列是该数据到中心点的距离
    centroids = randCent(dataSet, k)
    flag = True   # 用来判断聚类是否已经收敛
    while flag:
        flag = False;
        for i in range(m):  # 把每一个数据点划分到离它最近的中心点
            minDist = 1000000000; 
            minIndex = -1;
            for j in range(k):
                distJI = distEclud(centroids[j,:], dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI 
                    minIndex = j  # 如果第i个数据点到第j个中心点更近，则将i归属为j
            if division[i,0] != minIndex: 
                flag = True  # 如果分配发生变化，则需要继续迭代
            division[i,0] = minIndex
            division[i,1] = minDist   # 并将第i个数据点的分配情况存入字典
        #print (centroids)
        for i in range(k):   # 重新计算中心点
            ptsInClust = dataSet[nonzero(division[:,0].A == i)[0]]   # 去第一列等于cent的所有列
            centroids[i,:] = mean(ptsInClust, axis = 0)  # 算出这些数据的中心点"""
    return division

def KTH(choosename,docs,docs2):   #选中电影名称 选中及筛选后电影各项元素评分 选中及筛选后各项电影名称
    dataMat = []
    for i in range(len(docs)):
        dataMat1 = []
        for j in range(len(docs[i])):
            if docs[i][j]==' ':
                continue
            docs[i][j] = float(float(docs[i][j])*100)
    dataMat = mat(docs)
    m = shape(dataMat)[0]
    choosenum=[]   #选择电影的编号
    ansnum=[]
    vis=[]
    for i in range(m):
        vis.append(0)
    for i in range(m):
        for j in range(len(choosename)):
            if choosename[j]==docs2[i]:
                choosenum.append(i)
                vis[i]=1
                break
    for i in range(m):
        ansnum.append([i,0])
    for p in range(9):
        Division = kMeans(dataMat,9)
        for t in range(len(choosename)):
            tmp = Division[choosenum[t],0]
            ans=[]   #编号 距离
            for i in range(m):
                if Division[i,0]==tmp:
                    ans.append([i,distEclud(dataMat[i,:],dataMat[choosenum[t],:])])
                ans.sort(key=lambda x:x[1])
            for i in range(len(ans)):
                ansnum[ans[i][0]][1]+=1
    ansnum.sort(key=lambda x:x[1],reverse=True)
    templist = []
    flag=0
    for i in range(len(docs)):
        if vis[ansnum[i][0]]==0:
            templist.append(docs2[ansnum[i][0]])
            flag+=1
        if flag==4:
            break
    return templist