#-*- coding=utf-8 -*-
import jieba
import re
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV##TF-IDF
from sklearn.naive_bayes import MultinomialNB as MNB#多项式贝叶斯分类器
from sklearn.model_selection import cross_val_score#交叉验证
from sklearn.metrics import roc_auc_score
from sklearn.externals import joblib
from sklearn.metrics import classification_report
def jieba_input():#加入人名帮助分词
    actor_file=open('D:\\pythoncode\Project\Data\\'+'role.txt','r',encoding='utf-8')
    director_file=open('D:\pythoncode\Project\Data\\'+'director.txt','r',encoding='utf-8')
    actor_list = actor_file.readlines()
    director_list=director_file.readlines()
    for x in actor_list:
        x=(re.sub("[^\u4E00-\u9FA5]+"," ",x)).strip()
        jieba.suggest_freq(x,True)
    for x in director_list:
        x=(re.sub("[^\u4E00-\u9FA5]+"," ",x)).strip()
        jieba.suggest_freq(x,True)    
    actor_file.close()
    director_file.close()
def review_to_wordlist(review):#将影评转换为其中包含的词的list
    seg_list = jieba.cut(review)
    words = " ".join(seg_list)
    words = re.sub("[^\u4E00-\u9FA5]+"," ",words)
    return words
def value_to_sentiment(value):
    if int(value[0]) >= 3:
        return 1
    else:
        return 0

jieba_input()
f = open('stopword.txt',"r")
stops = f.readlines()
for x in range(len(stops)):
    stops[x] = re.sub("\n","",stops[x])
f.close()
f = open('D:\\pythoncode\Project\Data\\'+'fullfilmname.txt',"r",encoding='utf-8')
filmname_list = f.readlines()
f.close()
trainv = []
trainw = []
for x in filmname_list:
    x = x.strip()
    f1 = open('D:\\pythoncode\Project\Data\\'+x+'影评打分.txt','r',encoding='utf-8')
    f2 = open('D:\\pythoncode\Project\Data\\'+x+'影评内容.txt','r',encoding='utf-8')
    trainv = trainv + [value_to_sentiment(c.strip()) for c in f1.readlines()]
    trainw = trainw + [c.strip() for c in f2.readlines()]
trainv = [int(c) for c in trainv]
train = [trainv,trainw]
train = pd.DataFrame(train)
train = train.T
train.columns = ['sentiment','review']
train['sentiment'] = train['sentiment'].astype(int)
train['review']= train['review'].astype(str)
now = os.path.abspath(r'testdata.csv')
test = pd.read_csv(now,encoding="gbk")
#读入训练数据和待分类数据
label_train = train['sentiment']
train_data = []
for i in range(len(train['review'])):
    train_data.append("".join(review_to_wordlist(train['review'][i])))
test_data = []
for i in range(len(test['review'])):
    test_data.append("".join(review_to_wordlist(test['review'] [i])))
#将影评转化为以影评中的所有词以空格隔开的字符串为一个元素的list
tfv = TFIV(min_df=2, max_features=None, strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1,2),use_idf=True,smooth_idf=True,sublinear_tf=True,stop_words=stops)
#生成TF-IDF类的实例 最小词频 选择全部关键词使用 去除重音符号 特征类型 正则表达式匹配单词 n元模型 启用IDF算法 平滑IDF 线性缩放TF为1+log(tf) 使用内置英文停止词
X_all = train_data+test_data
len_train = len(train_data)#合并测试数据及训练数据 保存长度便于切片
tfv.fit(X_all)#学习数据
X_all = tfv.transform(X_all)#  返回各文档词频矩阵
X = X_all[:len_train] 
X_test = X_all[len_train:] #切片还原为合适的矩阵
#TF_IDF转化为特征词向量
model_NB = MNB(alpha = 1, class_prior = None, fit_prior = True)
model_NB.fit(X,label_train)
#训练分类器
#print("多项式贝叶斯分类器10折交叉验证得分",np.mean(cross_val_score(model_NB,X,label_train,cv=10,scoring='precision')))#交叉验证      
print("多项式贝叶斯分类器10折交叉验证得分",np.mean(cross_val_score(model_NB,X,label_train,cv=10,scoring='roc_auc')))#交叉验证      
test_predicted = np.array(model_NB.predict(X_test))
test_true = test['sentiment']
#print("模型评估报告")
#print(classification_report(test_true,test_predicted))
#nb_output = pd.DataFrame(data=test_predicted, columns=['sentiment'])
#nb_output.to_csv("my_result.csv",index=False)
#保存结果
joblib.dump(model_NB,"MNB_SA.m")
joblib.dump(tfv,"TFV.m")