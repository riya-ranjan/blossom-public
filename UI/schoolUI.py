# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'riyaBlossomUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from blossompy import Blossom
from time import sleep
import simpleaudio as sa
# class school UI would have two instance vari schoolUI and blossom
# init -> blossom start up and UI start up
# is there a way to tell when UI

class Ui_MainWindow(object):

    def __init__(self):
        bl = Blossom(sequence_dir='../blossompy/src/sequences')
        bl.connect() # safe init and connects to blossom and puts blossom in reset position

        bl.load_sequences()
        bl.do_sequence("breathing/exhale")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 30, 481, 51))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 100, 481, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 170, 481, 51))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 240, 231, 181))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 240, 231, 181))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(110, 440, 231, 181))
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(360, 440, 231, 181))
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(110, 640, 141, 131))
        self.pushButton_8.setObjectName("pushButton_8")

        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(280, 640, 141, 131))
        self.pushButton_9.setObjectName("pushButton_9")

        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(450, 640, 141, 131))
        self.pushButton_10.setObjectName("pushButton_10")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.pushButton.setText(_translate("MainWindow", "Reset"))
        self.pushButton.clicked.connect(self.reset_clicked)
        self.pushButton_2.setText(_translate("MainWindow", "Play Introduction"))
        self.pushButton_2.clicked.connect(self.playIntro_clicked)
        self.pushButton_3.setText(_translate("MainWindow", "Start Breath"))
        self.pushButton_3.clicked.connect(self.startBreath_clicked)

        self.pushButton_4.setText(_translate("MainWindow", "Exhale"))
        self.pushButton_4.clicked.connect(self.exhale_clicked)
        self.pushButton_5.setText(_translate("MainWindow", "Inhale"))
        self.pushButton_5.clicked.connect(self.inhale_clicked)
        self.pushButton_6.setText(_translate("MainWindow", "Inhale with Counting"))
        self.pushButton_6.clicked.connect(self.inhaleCount_clicked)
        self.pushButton_7.setText(_translate("MainWindow", "Exhale with Counting"))
        self.pushButton_7.clicked.connect(self.exhaleCount_clicked)

        self.pushButton_8.setText(_translate("MainWindow", "Count \"one\""))
        self.pushButton_8.clicked.connect(self.countOne_clicked)
        self.pushButton_9.setText(_translate("MainWindow", "Count \"two\""))
        self.pushButton_9.clicked.connect(self.countTwo_clicked)
        self.pushButton_10.setText(_translate("MainWindow", "Count \"three\""))
        self.pushButton_10.clicked.connect(self.countThree_clicked)

    def reset_clicked(self):
        self.pushButton.setText("clicked")
        # add function calls here!
        # do we want to still show "clicked"?
        # play sequence "reset"

    def playIntro_clicked(self):
        self.pushButton_2.setText("clicked")
        # play "breathing - intro" (in breathing demos)

    def startBreath_clicked(self):
        self.pushButton_3.setText("clicked")
        # play sequence "start breath"

    def exhale_clicked(self):
        self.pushButton_4.setText("clicked")
        # play sequence "exhale"

    def inhale_clicked(self):
        self.pushButton_5.setText("clicked")
        # play sequence "inhale"
        bl.do_sequence("breathing/inhale")
        sleep(3.5)

    def inhaleCount_clicked(self):
        self.pushButton_6.setText("clicked")
        # play sequence "inhale_counting" in breathing demos

    def exhaleCount_clicked(self):
        self.pushButton_7.setText("clicked")
        # play sequence "exhale_counting" in breathing demos

    def countOne_clicked(self):
        # self.pushButton_8.setText("clicked")
        # play wave file riya sent
        playsound("/Users/nataliehumber/Desktop/one.wav")

    def countTwo_clicked(self):
        # self.pushButton_9.setText("clicked")
        # play wave file riya sent
        playsound("/Users/nataliehumber/Desktop/two.wav")

    def countThree_clicked(self):
        # self.pushButton_10.setText("clicked")
        # play wave file riya sent
        playsound("/Users/nataliehumber/Desktop/three.wav")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())