# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat_gui_2.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CchatWindow(object):

    def setupUi(self, CchatWindow):
        CchatWindow.setObjectName("CchatWindow")
        CchatWindow.resize(640, 480)
        CchatWindow.move(QtCore.QPoint(15, 40))
        self.centralwidget = QtWidgets.QWidget(CchatWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBox.setObjectName("textBox")
        self.verticalLayout.addWidget(self.textBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputLine = QtWidgets.QLineEdit(self.centralwidget)
        self.inputLine.setObjectName("inputLine")
        self.horizontalLayout.addWidget(self.inputLine)
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        CchatWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CchatWindow)
        QtCore.QMetaObject.connectSlotsByName(CchatWindow)

    def retranslateUi(self, CchatWindow):
        _translate = QtCore.QCoreApplication.translate
        CchatWindow.setWindowTitle(_translate("CchatWindow", "Cchat"))
        self.sendButton.setText(_translate("CchatWindow", "Send"))
