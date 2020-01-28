# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'abc.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogABC(object):
    def setupUi(self, DialogABC):
        DialogABC.setObjectName("DialogABC")
        DialogABC.setFixedSize(382, 276)
        self.textEdit = QtWidgets.QTextEdit(DialogABC)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 361, 231))
        self.textEdit.setObjectName("textEdit")
        self.editABCButton = QtWidgets.QPushButton(DialogABC)
        self.editABCButton.setGeometry(QtCore.QRect(300, 250, 75, 23))
        self.editABCButton.setObjectName("editABCButton")

        self.retranslateUi(DialogABC)
        QtCore.QMetaObject.connectSlotsByName(DialogABC)

    def retranslateUi(self, DialogABC):
        _translate = QtCore.QCoreApplication.translate
        DialogABC.setWindowTitle(_translate("DialogABC", "Словарь"))
        self.editABCButton.setText(_translate("DialogABC", "Обновить"))
