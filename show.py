# -*- coding: utf-8 -*-
#电影详细展示
import sys
import random
import math
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from sql import *
def takesecond(elem):
    return elem[1]
def findroles(actortext):
    index = []
    for i in range(len(roles)):
        tempindex = actortext.find(roles[i])
        if(tempindex ==-1):
            continue
        index.append((roles[i],tempindex))
    index.sort(key = takesecond)
    index = [temp[0] for temp in index]
    if(len(index) == 0):
        return ('无')
    return(str(index[0]))
class MainWindow(QtGui.QWidget):
    def __init__(self, rowCount, parent=None):
        fontId2 = QFontDatabase.addApplicationFont("C:\Windows\Fonts\STZHONGS.TTF")
        self.fontName2 = QFontDatabase.applicationFontFamilies(fontId2)[0]
        
        self.slavewindow = [0 for x in range(len(films))]
        self.rowCount = rowCount
        QtGui.QWidget.__init__(self, parent)
        #电影展示
        self.initUI()
        #self.setWindowOpacity(0.5)#半透明


        #背景图片
        palette1 = QtGui.QPalette()
        #palette1.setColor(self.backgroundRole(), QColor(255,251,240,100))   # 设置背景颜色
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('background.png')))   # 设置背景图片
        self.setPalette(palette1)
        self.setAutoFillBackground(True) # 不设置也可以
        self.setGeometry(0,50,1180, 840)
        self.setWindowTitle('影评分析结果')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def initUI(self):
        self.widget = QtGui.QWidget(self)
        self.grid =QtGui.QGridLayout()

        #电影封面
        for i in range(len(films)):
            label = self.getFilmLabel(films[i])
            button=self.getFilmButton(i)
            self.assignFilm(i%self.rowCount,i//self.rowCount,label,button)
            
        self.widget.setLayout(self.grid)

        '''self.widget.setMinimumSize(len(films)*270,len(films)*390)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.widget)
        self.scroll.setAutoFillBackground(True)
        self.scroll.setWidgetResizable(True)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.setLayout(self.vbox)'''

    def assignFilm(self,x,y,label,button):
        self.grid.addWidget(label,y*2,x)
        self.grid.addWidget(button,y*2+1,x)

    def getFilmButton(self,i):
        button= QtGui.QPushButton(films[i])
        button.setFlat(True)
        button.setStyleSheet("color:white")
        button.setFont(QFont(self.fontName2,12))
        self.slavewindow[i] = Slavewindow(i)
        self.connect(button,SIGNAL('clicked()'),self.slavewindow[i].show)
        return button

    def getFilmLabel(self,filmname):
        label = QtGui.QLabel()
        png = QtGui.QPixmap('D:\\pythoncode\Project\Data\poster\\'+filmname+ '.png').scaled(270, 390)#回头改成数据库调
        label.setPixmap(png)
        return label

class Slavewindow(QWidget):
    def __init__(self,index,parent=None):
        super(Slavewindow,self).__init__(parent)
        self.index=index
        fontId1 = QFontDatabase.addApplicationFont("C:\Windows\Fonts\禹卫书法行书简体.ttf")
        self.fontName1 = QFontDatabase.applicationFontFamilies(fontId1)[0]

        fontId2 = QFontDatabase.addApplicationFont("C:\Windows\Fonts\STZHONGS.TTF")
        self.fontName2 = QFontDatabase.applicationFontFamilies(fontId2)[0]
        
        self.initUI()
        

        
        # 背景图片
        palette = QtGui.QPalette()
        # palette1.setColor(self.backgroundRole(), QColor(255,251,240,100))   # 设置背景颜色
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('background.png')))  # 设置背景图片
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 不设置也可以
        self.setGeometry(600, 300, 680, 840)
        self.setWindowTitle('电影介绍')
        #self.setWindowMainWindow(QtGui.QMainWindow('004.png'))
        # mylayout = QVBoxLayout()
        # self.setLayout(mylayout)

    def initUI(self):
        self.widget = QWidget(self)
        self.grid = QGridLayout()
        #题目：电影名称
        self.title = QPushButton(films[self.index])
        self.title.setFlat(True)
        self.title.setStyleSheet("color:white")
        self.title.setFont(QFont(self.fontName1, 24))
        self.grid.addWidget(self.title,0,1,1,2)

        self.label = QtGui.QLabel()
        png = QtGui.QPixmap('D:\\pythoncode\Project\Data\poster\\'+films[self.index] + '.png').scaled(270, 390)#scaled代表控制图片大小，记得按比例调整……
        self.label.setPixmap(png)
        self.grid.addWidget(self.label, 1, 3,8,1)#对象，行数，列数，所占行数，所占列数
        
        data_table=db.select('film',films[self.index].strip())
        f = open('D:\\pythoncode\Project\Data\\'+films[self.index]+'分项评分.txt','r')
        #exit()
        film_score = f.readlines()
        film_score = [x.strip() for x in film_score]
        f.close()
        if(len(data_table)==0):
            return
        #导演：
        dire0 = QPushButton('导演：')#按钮名称
        dire0.setFlat(True)#透明
        dire0.setStyleSheet("color:white")#字体颜色
        dire0.setFont(QFont(self.fontName2, 16))#字体，字号
        self.grid.addWidget(dire0, 1, 1)#对象，行数，列数#把对象塞到网格布局（grid)里
        
        #print(films[self.index])
        dire = QPushButton(data_table[0][2])
        dire.setFlat(True)
        dire.setStyleSheet("color:white")
        dire.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(dire, 1, 2)
        #演员：
        role0 = QPushButton('主演：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 2,1)

        role = QPushButton(findroles(data_table[0][3]))
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 2, 2)

        #类型：
        role0 = QPushButton('类型：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 3, 1)

        role = QPushButton(data_table[0][4])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 3, 2)

        #得分：
        role0 = QPushButton('得分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 4, 1)

        role = QPushButton(str(data_table[0][5]))
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 4, 2)

        #国家：
        role0 = QPushButton('国家：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 5, 1)

        role = QPushButton(data_table[0][6])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 5, 2)

        #时长：
        role0 = QPushButton('时长：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 6, 1)

        role = QPushButton(data_table[0][7])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 6, 2)

        #上映日期：
        role0 = QPushButton('上映日期：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 7, 1)

        role = QPushButton(data_table[0][8])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 7, 2)

        #票房：
        role0 = QPushButton('——————————')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 8, 1)

        role = QPushButton('——————————')
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 8, 2)

        # 评分1
        role0 = QPushButton('主题评分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 9, 1)

        role = QPushButton(film_score[0])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 9, 2)

        # 评分2
        role0 = QPushButton('演员评分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 10, 1)

        role = QPushButton(film_score[1])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 10, 2)

        # 评分3
        role0 = QPushButton('导演评分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 11, 1)

        role = QPushButton(film_score[2])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 11, 2)

        # 评分4
        role0 = QPushButton('剧情评分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 12, 1)

        role = QPushButton(film_score[3])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 12, 2)

        # 评分5
        role0 = QPushButton('视觉评分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 13, 1)

        role = QPushButton(film_score[4])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 13, 2)

        # 评分6
        role0 = QPushButton('配乐评分：')
        role0.setFlat(True)
        role0.setStyleSheet("color:white")
        role0.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role0, 14, 1)

        role = QPushButton(film_score[5])
        role.setFlat(True)
        role.setStyleSheet("color:white")
        role.setFont(QFont(self.fontName2, 16))
        self.grid.addWidget(role, 14, 2)

        self.widget.setLayout(self.grid)

def work(film_list):
    global films
    films = film_list
    print(films)
    f = open('director.txt', 'r', encoding='utf-8')
    global directors
    directors = f.readlines()
    for i in range(len(directors)):
        directors[i] = directors[i].split(' ')[1]
        directors[i] = directors[i].replace('\n', '')
    f.close()
    f = open('role.txt', 'r', encoding='utf-8')
    global roles
    roles = f.readlines()
    for i in range(len(roles)):
        roles[i] = roles[i].split(' ')[1]
        roles[i] = roles[i].replace('\n', '')
    f.close()
    global db
    db = connect()
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(4)
    mainWindow.show()
    app.exec_()
    db.close()
