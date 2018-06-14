#show 01

import sys
import random
import math
from PyQt4.QtGui import *
from PyQt4.QtCore import *

global recommand
recommand = []

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        fontId = QFontDatabase.addApplicationFont("C:\Windows\Fonts\BRITANIC.TTF")
        self.fontName = QFontDatabase.applicationFontFamilies(fontId)[0]

        fontdetail = QFontDatabase.addApplicationFont("C:\Windows\Fonts\Inkfree.ttf")
        self.fontsta = QFontDatabase.applicationFontFamilies(fontdetail)[0]


        self.makeTEXTEDIT()

        #状态栏
        self.statusBar().showMessage('ready')
        self.statusBar().setStyleSheet("color:white")
        self.statusBar().setFont(QFont(self.fontsta,16))

        # 背景图片
        palette1 = QPalette()
        # palette1.setColor(self.backgroundRole(), QColor(255,251,240,100))   # 设置背景颜色
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.png')))  # 设置背景图片
        self.setPalette(palette1)
        self.setAutoFillBackground(True)  # 不设置也可以
        self.setGeometry(300, 100, 1180, 840)
        self.setWindowTitle('recommend')


    def makeTEXTEDIT(self):
        self.wid = QWidget()
        self.text = QLineEdit()
        self.text.setFont(QFont('simHei',20))

        button = QPushButton('pick')
        button.setFlat(True)
        button.setStyleSheet("color:white")
        button.setFont(QFont(self.fontName,20))
        self.connect(button, SIGNAL('clicked()'), self.addList)

        push = QPushButton('finish')
        push.setFlat(True)
        push.setStyleSheet('color:white')
        push.setFont(QFont(self.fontName,20))
        self.connect(push, SIGNAL('clicked()'), self.finishi)

        hboxx = QHBoxLayout()
        hboxx.addWidget(self.text,8)
        hboxx.addWidget(button,2)
        hboxx.addWidget(push,2)

        #横竖布局
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(382)
        self.vbox.addLayout(hboxx)
        #self.vbox.addWidget(self.text)
        self.vbox.addStretch(618)

        hbox =QHBoxLayout()
        hbox.addStretch(2)
        hbox.addLayout(self.vbox,8)
        hbox.addStretch(2)
        self.wid.setLayout(hbox)
        self.setCentralWidget(self.wid)

    def addList(self):
        recommand.append(self.text.text())
        self.statusBar().showMessage(self.text.text())

    def finishi(self):
        self.statusBar().showMessage('Loading,please waiting for our recommendation espacially for you~')
def showw():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
def get_choose():
    showw()
    return recommand