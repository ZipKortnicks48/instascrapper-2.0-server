from src.mysql_settings import mysqlSettings
import formsUI.form_mailbook as form_mailbook
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon,QStyle,QAction,qApp,QMenu
class AppEmail(QtWidgets.QMainWindow, form_mailbook.Ui_DialogEmail):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mailSettings=mysqlSettings()
        self.showMails()
        self.editEmailButton.pressed.connect(self.saveMails)
    def showMails(self):
        mails=self.mailSettings.getMail()
        for mail in mails:
            self.textEdit.append(mail[0])
    def saveMails(self):
        try:
            s=self.textEdit.toPlainText()
            strList=s.split('\n') 
            self.mailSettings.updateMail(strList)
            QMessageBox.about(self,"Обновление адресной книги","Адресная книга обновлена")
        except Exception as e:
            QMessageBox.about(self,"Обновление адресной книги",str(e))