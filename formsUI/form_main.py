# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(629, 638)
        self.textBoxSearch = QtWidgets.QLineEdit(Dialog)
        self.textBoxSearch.setGeometry(QtCore.QRect(390, 61, 211, 21))
        self.textBoxSearch.setObjectName("textBoxSearch")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(460, 40, 181, 16))
        self.label.setObjectName("label")
        self.comboBoxAcc = QtWidgets.QComboBox(Dialog)
        self.comboBoxAcc.setGeometry(QtCore.QRect(20, 60, 141, 22))
        self.comboBoxAcc.setObjectName("comboBoxAcc")
        self.comboBoxAcc.addItem("")
        self.comboBoxAcc.addItem("")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 201, 20))
        self.label_2.setObjectName("label_2")
        self.tableComments = QtWidgets.QTableWidget(Dialog)
        self.tableComments.setSizeAdjustPolicy(
        QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableComments.setGeometry(QtCore.QRect(20, 90, 581, 471))
        self.tableComments.setObjectName("tableComments")
        self.tableComments.setColumnCount(3)
        self.tableComments.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableComments.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableComments.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableComments.setHorizontalHeaderItem(2, item)
        self.buttonHand = QtWidgets.QPushButton(Dialog)
        self.buttonHand.setGeometry(QtCore.QRect(350, 60, 41, 23))
        self.buttonHand.setObjectName("buttonHand")
        self.autoButton = QtWidgets.QPushButton(Dialog)
        self.autoButton.setGeometry(QtCore.QRect(460, 600, 141, 23))
        self.autoButton.setObjectName("autoButton")
        self.findNewComButton = QtWidgets.QPushButton(Dialog)
        self.findNewComButton.setGeometry(QtCore.QRect(460, 570, 141, 23))
        self.findNewComButton.setObjectName("findNewComButton")
        self.showCommentsButton = QtWidgets.QPushButton(Dialog)
        self.showCommentsButton.setGeometry(QtCore.QRect(314, 60, 41, 23))
        self.showCommentsButton.setObjectName("showCommentsButton")
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('Опции')
        self.newBDItem=self.fileMenu.addAction("Обновить базу данных пользователя")
        self.newABCItem=self.fileMenu.addAction("Словарь")
        self.newAddressItem=self.fileMenu.addAction("Адресная книга")
        self.newServerSettingsItem=self.fileMenu.addAction("Настройки сервера")
        self.helpMenu=menubar.addMenu("Помощь")
        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exitAction)
        self.buttonStop = QtWidgets.QPushButton(Dialog)
        self.buttonStop.setGeometry(QtCore.QRect(20, 570, 75, 23))
        self.buttonStop.setObjectName("buttonStop")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Instascrapper"))
        self.label.setText(_translate("Dialog", "Введите слово для поиска"))
        self.comboBoxAcc.setItemText(0, _translate("Dialog", "igor_artamonov48"))
        self.comboBoxAcc.setItemText(1, _translate("Dialog", "igor_artamonov48"))
        self.label_2.setText(_translate("Dialog", "Выберите аккаунт для отслеживания"))
        item = self.tableComments.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Дата"))
        item = self.tableComments.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Текст"))
        self.tableComments.setColumnWidth(1, 260)
        self.tableComments.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        item = self.tableComments.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Ссылка на запись"))
        self.buttonHand.setText(_translate("Dialog", "🔍"))
        self.autoButton.setText(_translate("Dialog", "Авторежим"))
        self.findNewComButton.setText(_translate("Dialog", "Проверить страницу"))
        self.showCommentsButton.setText(_translate("Dialog", "🕮"))
        self.buttonStop.setText(_translate("Dialog", "Стоп"))
