#-*- coding=utf-8 -*
import requests
import chardet
import re
import io
import sys
import time
from bs4 import BeautifulSoup
global flag


def isallcn(s):
    for c in s:
        if not ('\u4e00' <= c <= '\u9fa5'):
            return False
    return True


def acquireuser(url, flim):
    f = open('《'+flim+'》'+"影评者所在地.txt", "a", encoding='utf-8')
    response = requests.get(url)
    htmltext = response.content.decode('utf-8')
    soup = BeautifulSoup(htmltext, 'lxml')
    for k in soup.find_all('div', class_='user-info'):
        if k.find('a') != None:
            f.write(k.find('a').string+'\n')
        else:
            f.write("未知"+'\n')
    f.close()


def acquirepage(url, flim):
    response = requests.get(url)
    htmltext = response.content.decode('utf-8')
    soup = BeautifulSoup(htmltext, 'lxml')
    f = open('《'+flim+'》'+" 影评时间.txt", "a", encoding='utf-8')
    for k in soup.find_all('span', class_="comment-time"):
        text = k.string.strip()+'\n'
        f.write(text)
    f.close()
    f = open('《'+flim+'》'+" 影评评分.txt", "a", encoding='utf-8')
    for k in soup.find_all('span', class_="comment-info"):
        if k.find('span', class_=re.compile(r"allstar")) != None:
            f.write(k.find('span', class_=re.compile(
                r"allstar")).get('class')[0][7])
            f.write('\n')
        else:
            f.write("?\n")
    f.close()
    f = open('《'+flim+'》'+" 影评内容.txt", "a", encoding='utf-8')
    for k in soup..find_all('div',class_ = 'comment')
        f.write(k.find('p').getext().strip())
        f.write('\n')
    f.close()
    for k in soup.find_all('div',class_='avatar'):
        userurl = k.find('a').get('href')
        acquireuser(userurl,"红海行动")

for x in range(11):
    x = x*20
    url = "https://movie.douban.com/subject/26861685/comments?" + \
        "start="+str(x)+"&limit=20&sort=new_score&status=P&percent_type="
    acquirepage(url, "红海行动")
