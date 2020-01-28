# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mailbook.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogEmail(object):
    def setupUi(self, DialogEmail):
        DialogEmail.setObjectName("DialogEmail")
        DialogEmail.setFixedSize(382, 276)
        self.textEdit = QtWidgets.QTextEdit(DialogEmail)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 361, 231))
        self.textEdit.setObjectName("textEdit")
        self.editEmailButton = QtWidgets.QPushButton(DialogEmail)
        self.editEmailButton.setGeometry(QtCore.QRect(300, 250, 75, 23))
        self.editEmailButton.setObjectName("editEmailButton")

        self.retranslateUi(DialogEmail)
        QtCore.QMetaObject.connectSlotsByName(DialogEmail)

    def retranslateUi(self, DialogEmail):
        _translate = QtCore.QCoreApplication.translate
        DialogEmail.setWindowTitle(_translate("DialogEmail", "Адресная книга"))
        self.editEmailButton.setText(_translate("DialogEmail", "Обновить"))
