# -*- coding: utf-8 -*-
import kmeans
import itemCF
import json
import GOM
#import GSM
import ask
import Found
import show
choose_name = ask.get_choose()
print(choose_name)
user_star = [4.0 for x in range(len(choose_name))]
all_film_name = Found.getallfilm()
print('OK1')
f = open("dump.txt",'r')
json_str = f.read()
f.close()
commentscoreMat = json.loads(json_str)
print('OK2')
choose_object_mat = GOM.gom(choose_name)
print('OK3')
#itemCF.item_CF(commentscoreMat,all_film_name,choose_name,user_star)
item_name = itemCF.item_CF(commentscoreMat,all_film_name,choose_name,user_star)
#print(item_name)
print('OK4')
kmeans_object_mat = GOM.gom(item_name)
print('OK5')
show.work(kmeans.KTH(choose_name,kmeans_object_mat,item_name))
