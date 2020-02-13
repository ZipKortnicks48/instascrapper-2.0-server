from src.bdmeth import bdAPI
import formsUI.form_abc as form_abc
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon,QStyle,QAction,qApp,QMenu
class AppABC(QtWidgets.QMainWindow, QtWidgets.QTableWidgetItem, form_abc.Ui_DialogABC,QtWidgets.QErrorMessage,QtWidgets.QHeaderView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bdAPI=bdAPI()
        self.showABC()
        self.editABCButton.pressed.connect(self.saveWords)
    def showABC(self):
        words=self.bdAPI.getABC()
        for word in words:
            self.textEdit.append(word['abc_text'])
    def saveWords(self):
        try:
            s=self.textEdit.toPlainText()
            strList=s.split('\n') 
            self.bdAPI.updateABC(strList)
            self.bdAPI.checkComments()
            QMessageBox.about(self,"Обновление словаря","Словарь обновлен")
        except Exception as e:
            QMessageBox.about(self,"Обновление словаря",str(e))
