# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'abc.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogServer(object):
    def setupUi(self, DialogServer):
        DialogServer.setObjectName("DialogServer")
        DialogServer.setFixedSize(382, 276)
        self.textEdit = QtWidgets.QTextEdit(DialogServer)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 361, 231))
        self.textEdit.setObjectName("textEdit")
        self.editServerButton = QtWidgets.QPushButton(DialogServer)
        self.editServerButton.setGeometry(QtCore.QRect(300, 250, 75, 23))
        self.editServerButton.setObjectName("editABCButton")

        self.retranslateUi(DialogServer)
        QtCore.QMetaObject.connectSlotsByName(DialogServer)

    def retranslateUi(self, DialogServer):
        _translate = QtCore.QCoreApplication.translate
        DialogServer.setWindowTitle(_translate("DialogServer", "Настройки подключения к серверу"))
        self.editServerButton.setText(_translate("DialogServer", "Обновить"))
