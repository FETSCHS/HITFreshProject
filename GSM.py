#-*- coding=utf-8 -*-
from sql import *
import Found
import json
def Gsm(filmname_list):
    number = 0
    username_set = set()
    dic = {}
    for film in filmname_list:
        data=db.select('comment',film.strip())
        username_list=[i[4] for i in data]
        star_list=[i[3] for i in data]
        for username in username_list:
            username_set.add(username)
    for name in username_set:
        dic[name]=number
        number += 1
    mat = [[0 for y in range(len(username_set))] for x in range(len(filmname_list))]    
    for film in filmname_list:
        index = filmname_list.index(film)
        data=db.select('comment',film.strip())
        username_list=[i[4] for i in data]
        star_list=[i[3] for i in data]
        comment_list=[i[2] for i in data]
        for x in range(len(username_list)):
            mat[index][dic[username_list[x]]] = float(star_list[x])
    return mat
global db
db = connect()
'''all_film_name = Found.getallfilm()
f = open('dump.txt','w')
MAT = gsm(all_film_name)
JSON_STR = json.dumps(MAT)
f.write(JSON_STR)
f.close()'''

db.close()