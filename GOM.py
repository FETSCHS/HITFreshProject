#-*- coding=utf-8 -*-
import jieba
import re
import os
import pandas as pd
import numpy as np
from sql import *
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV##TF-IDF
from sklearn.naive_bayes import MultinomialNB as MNB#多项式贝叶斯分类器
from sklearn.externals import joblib
def SA(test_data):
    test_data = tfv.transform(test_data)
    test_predicted = model_NB.predict(test_data)
    if int(test_predicted)==0:
        return -1
    else:
        return int(test_predicted[0])
def review_to_wordlist(review):#将影评转换为其中包含的词的list
    seg_list = jieba.cut(review)
    words = " ".join(seg_list)
    words = re.sub("[^\u4E00-\u9FA5]+"," ",words)
    return words
def cut_sentences(sentence):  #切分短句
    puns = frozenset(u'，, 。！？')  
    tmp = []  
    for ch in sentence:  
        tmp.append(ch)  
        if puns.__contains__(ch):  
            yield ''.join(tmp)  
            tmp = []  
    yield ''.join(tmp)  
def findobject(sentence,object_list):
    for object_num in range(len(object_list)):
        for object_word in object_list[object_num]:
            if(sentence.find(object_word)!=-1):
                return object_num
        if object_num ==1:
            for actor_name in actor_list:
                if sentence.find(actor_name):
                    print(sentence,actor_name)
                    return object_num
        if object_num == 2:
            for director_name in director_list:
                if sentence.find(director_name):
                    return object_num
    return -1
def find_worker():
    actor_file=open('D:\\pythoncode\Project\Data\\'+'role.txt','r',encoding='utf-8')
    director_file=open('D:\pythoncode\Project\Data\\'+'director.txt','r',encoding='utf-8')
    actor_list = []
    director_list = []
    for x in actor_list:
        x=(re.sub("[^\u4E00-\u9FA5]+"," ",x)).strip()
        actor_list.append(x)
    for x in director_list:
        x=(re.sub("[^\u4E00-\u9FA5]+"," ",x)).strip()
        director_list.append(x)
    actor_file.close()
    director_file.close()
    return actor_list,director_list
def gom(filmname_list): 
    global db
    db=connect()    
    db.close()
    global tfv,actor_list,director_list,model_NB
    tfv = joblib.load('D:\\pythoncode\Project\FETS\\'+'TFV.m')
    model_NB = joblib.load('D:\\pythoncode\Project\FETS\\'+'MNB_SA.m')
    actor_list,director_list = find_worker()
    comobject_file = open('D:\\pythoncode\Project\FETS\\'+'commentobject.txt','r',encoding='utf-8')
    comobject_list = comobject_file.readlines()
    comobject_list = [object.split() for object in comobject_list]
    comobject_file.close()
    stops_file = open('D:\\pythoncode\Project\FETS\\'+'stopword.txt',"r")
    stops = stops_file.readlines()
    for x in range(len(stops)):
        stops[x] = re.sub("\n","",stops[x])
    stops_file.close()
    trainv = []
    trainw = []
    score = [[0 for y in range(6)] for x in range(len(filmname_list))]
    for filmname in filmname_list:
        score_sum = [0 for x in range(6)]
        score_val = [0 for x in range(6)]
        #comment_file = open('D:\\pythoncode\Project\Data\\'+filmname+'影评内容.txt','r',encoding ='utf-8')
        #star_file = open('D:\\pythoncode\Project\Data\\'+filmname+'影评打分.txt','r',encoding ='utf-8')
        data_table=db.select('comment',filmname.strip())        
        comment_list = [temp[2] for temp in data_table]
        star_list =  [temp[3] for temp in data_table]
        for text in comment_list:
            for temptext in cut_sentences(text):
                if(len(temptext)<6):
                    continue
                object = findobject(temptext,comobject_list)
                if(object!=-1):
                    temptext_list = []
                    temptext_list.append("".join(review_to_wordlist(temptext)))
                    sentiment=SA(temptext_list)
                    if(star_list[comment_list.index (text)] == 1.0):
                        sentiment = -1
                    score_val[object]+=sentiment  
                    score_sum[object]+=1               
        for x in range(6):
            if(score_sum[x]>5):
                score_val[x]=round(score_val[x]/score_sum[x]*2.5)+2.5
            else:       
                score_val[x]=0
        score[filmname_list.index(filmname)] = score_val
        '''f = open('D:\\pythoncode\Project\Data\\'+filmname+'分项评分.txt','w')
        for val in score_val:
            f.write(str(val)+'\n')
        f.close()'''
    return score