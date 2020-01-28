from src.mysql_settings import mysqlSettings
import formsUI.form_server_settings as form_server
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon,QStyle,QAction,qApp,QMenu
class AppServerSettings(QtWidgets.QMainWindow, form_server.Ui_DialogServer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serverSettings=mysqlSettings()
        self.showServerSettings()
        self.editServerButton.pressed.connect(self.saveServerSettings)
    def showServerSettings(self):
        settings=self.serverSettings.getServerSettings()
        for setting in settings:
            if setting!="set_id":
                self.textEdit.append(settings[setting])
    def saveServerSettings(self):
        try:
            s=self.textEdit.toPlainText()
            strList=s.split('\n') 
            self.serverSettings.updateServerSettings(strList)
            QMessageBox.about(self,"Обновление настроек сервера","Настройки обновлены")
        except Exception as e:
            QMessageBox.about(self,"Обновление настроек сервера",str(e))