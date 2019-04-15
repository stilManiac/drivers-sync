# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(326, 226)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(110, 8, 201, 22))
        self.comboBox.setObjectName("comboBox")
        self.devices_label = QtWidgets.QLabel(self.centralwidget)
        self.devices_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.devices_label.setObjectName("devices_label")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(10, 50, 211, 16))
        self.status_label.setObjectName("status_label")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(10, 70, 211, 16))
        self.name_label.setObjectName("name_label")
        self.syncButton = QtWidgets.QPushButton(self.centralwidget)
        self.syncButton.setGeometry(QtCore.QRect(117, 170, 101, 23))
        self.syncButton.setObjectName("syncButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 326, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.devices_label.setText(_translate("MainWindow", "Storage devices:"))
        self.status_label.setText(_translate("MainWindow", "Status: Synced"))
        self.name_label.setText(_translate("MainWindow", "Name: Kingston"))
        self.syncButton.setText(_translate("MainWindow", "Sync / Delete"))


