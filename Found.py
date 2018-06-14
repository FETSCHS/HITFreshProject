import os
import re
def getallfilm():
    f = open('film.txt', 'r', encoding='utf-8')
    films = f.readlines()
    # nn = []
    for i in range(len(films)):
        films[i] = films[i].split(' ')[1]
        films[i] = films[i].replace('\n','')
    f.close()
    return films