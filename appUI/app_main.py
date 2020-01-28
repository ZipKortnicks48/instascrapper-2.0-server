
import formsUI.form_main as form_main
from appUI.app_abc import AppABC
from appUI.app_email import AppEmail
from appUI.app_server_settings import AppServerSettings
from src.formHandler import formHandler
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon,QStyle,QAction,qApp,QMenu
from datetime import datetime
from threading import Thread
import schedule
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
class App(QtWidgets.QMainWindow, QtWidgets.QTableWidgetItem, form_main.Ui_Dialog,QtWidgets.QErrorMessage,QtWidgets.QHeaderView):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.startEvent = True
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.showCommentsButton.pressed.connect(self.showCommentsButtonClick)
        self.findNewComButton.pressed.connect(self.searchNewCommentsClickInThread)
        self.autoButton.pressed.connect(self.autoClick)
        self.buttonHand.pressed.connect(self.handSearch)
        self.buttonStop.pressed.connect(self.stopClick)
        self.buttonStop.setEnabled(False)
        #иконка трея
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
 
        '''
            show - показать окно
            hide - скрыть окно
            exit - выход из программы
        '''
        show_action = QAction("Развернуть", self)
        quit_action = QAction("Выход", self)
        hide_action = QAction("Скрыть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.newBDItem.triggered.connect(self.btnMediaClick)
        self.newABCItem.triggered.connect(self.showNewABCWindow)
        self.newAddressItem.triggered.connect(self.showNewAddressWindow)
        self.newServerSettingsItem.triggered.connect(self.showNewServerSettingsWindow)
    def showNewABCWindow(self):
        self.windowABC = AppABC()  # Создаём объект класса ExampleApp
        self.windowABC.show()  # Показываем окно
    def showNewAddressWindow(self):
        self.windowEmail = AppEmail()  # Создаём объект класса ExampleApp
        self.windowEmail.show()  # Показываем окно
    def showNewServerSettingsWindow(self):
        self.windowServer = AppServerSettings()  # Создаём объект класса ExampleApp
        self.windowServer.show()  # Показываем окно
    #ручной поиск по словам 
    def handSearch(self):
        word=self.textBoxSearch.text()
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        self.tableComments.clear()
        comments=self.handler.bdAPI.getCommentHandsearch(word)
        self.tableComments.setRowCount(len(comments))
        row=0
        for comment in comments:
                self.tableComments.setItem(row, 0,  QtWidgets.QTableWidgetItem(datetime.fromtimestamp(int(comment["comment_date"])).strftime("%d-%m-%Y %H:%M")))
                self.tableComments.setItem(row, 1,  QtWidgets.QTableWidgetItem(comment["comment_text"]))
                self.tableComments.setItem(row, 2,  QtWidgets.QTableWidgetItem(self.handler.bdAPI.getLinkByCommentId(comment["comment_id"])))
                row += 1
        self.setHeaderTittle()
        QMessageBox.about(self,"Уведомление","Поиск завершен")
    #остановка автопроцесса
    def stopClick(self):
        self.startEvent=False
        self.buttonStop.setEnabled(False)
        QMessageBox.about(self,"Уведомление","Остановка авторежима. Программа остановится после завершения цикла проверки.")
    def enableButtons(self):
        self.autoButton.setEnabled(True)
        self.findNewComButton.setEnabled(True)
    #обработчик кнопки "Авторежим"
    def autoClick(self):
        self.startEvent=True
        self.buttonStop.setEnabled(True)
        self.autoButton.setEnabled(False)
        self.findNewComButton.setEnabled(False)
        QMessageBox.about(self,"Уведомление","Запущен авто-режим. Некоторые действия недоступны. Уведомления об отслеживании будут приходить на почту.")
        thread = Thread(target=self.jobThread,daemon=True)
        thread.start()
    #поток авторежима
    def jobThread(self):
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        schedule.every(2).minutes.do(self.jobException)
        while self.startEvent==True:
            schedule.run_pending()
            time.sleep(1)
        self.autoButton.setEnabled(True)
        self.findNewComButton.setEnabled(True)
    def jobException(self):
        # try:
        #     self.job()
        # except Exception as e:
        #     self.writeReport("Ошибка в цикле авторежима: "+str(e))
        #     time.sleep(600)
        #subprocess.run(['python','scrap.py'],timeout=1)
        proc = subprocess.Popen(['python','scrap.py'])
        try:
            self.writeReport("Начало процесса")
            outs, errs = proc.communicate(timeout=900)
        except subprocess.TimeoutExpired:
            proc.terminate()
            outs, errs = proc.communicate()
            self.writeReport("Процесс завершился по таймауту.")
    def setHeaderTittle(self):
        self.tableComments.setHorizontalHeaderLabels(['Дата', 'Текст', 'Ссылка на запись'])
    #циклы авторежима
    def job(self):  
            username=self.comboBoxAcc.currentText()
            self.handler=None
            self.handler=formHandler(username)
            self.handler.bdAPI.commentsUnNew()#комментарии прочитаны БД
            self.handler.searchAndAddNewMediaItems()
            rows=self.handler.bdAPI.getMediaIds()
            for row in rows:
                commentsOld=self.handler.bdAPI.takeOldCommentsIds(row[0])#старые 50
                commentsOldN=list(map(lambda x: int(x[0]),commentsOld))
                commentsNew=self.handler.f.takeCommentsWithoutCircle(row[0],50)#новые 50
                for comment in commentsNew:
                    if comment['pk'] in commentsOldN:
                        break
                    else:
                        self.handler.bdAPI.rComment(comment,row[0])#добавляем в базу новые комментарии
            self.handler.bdAPI.checkNewComments()#отмечает все новые комменты по словарю
            rows=self.handler.bdAPI.showGoodNewComments()#получает новые и отмеченные для единовременной их отправки на почту
            if len(rows)!=0:
                host = "smtp.yandex.ru"
                to_addr = self.handler.bdAPI.getMail()
                from_addr = "instagram@rkvv.ru"
                error=0
                self.writeReport("Найдено (%s) комментариев(комментарий)."%str(len(rows)))
                self.send_email(rows,host, to_addr, from_addr)
            else:
                self.writeReport("Подходящие комментарии не обнаружены.")
            self.handler.bdAPI.commentsUnNew()#комментарии прочитаны
            self.writeReport("Успешный цикл авторежима.")
    #отправка сообщения на имейл
    def send_email(self,rows,host, to_addr, from_addr): 
        to_addr=list(map(lambda x: x[0],to_addr))
        body_text="На странице были отслежены следующие комментарии:\n"
        for row in rows:
            body_text+="\nТекст комментария:\n%s\nСсылка на запись в инстаграм:\n%s\nВремя публикации:\n%s\n"%(row[1],self.handler.bdAPI.getLinkByCommentId(row[0]),datetime.fromtimestamp(row[2]).strftime("%d-%m-%Y %H:%M"))
        msg = MIMEText(body_text, 'plain', 'utf-8')
        msg['Subject'] = Header('Обнаружение комментариев', 'utf-8')
        msg['From'] = from_addr     
        separator=", "
        msg['To'] = separator.join(to_addr)
        server = smtplib.SMTP_SSL(host,port=465)
        server.login('instagram@rkvv.ru','asdqwe123')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        self.writeReport("Успешная рассылка.")
    #отобразить найденные комменты по словарю
    def showCommentsButtonClick(self):
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        self.tableComments.clear()
        comments=self.handler.bdAPI.showGoodComments()
        self.tableComments.setRowCount(len(comments))
        row=0
        for comment in comments:
                self.tableComments.setItem(row, 0,  QtWidgets.QTableWidgetItem(datetime.fromtimestamp(int(comment['comment_date'])).strftime("%d-%m-%Y %H:%M")))
                self.tableComments.setItem(row, 1,  QtWidgets.QTableWidgetItem(comment['comment_text']))
                self.tableComments.setItem(row, 2,  QtWidgets.QTableWidgetItem(self.handler.bdAPI.getLinkByCommentId(comment['comment_id'])))
                row += 1
        self.setHeaderTittle()
        QMessageBox.about(self,"Уведомление","Поиск завершен")
    #поиск по новому словарю
    def searchButtonClick(self):
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        #QMessageBox.about(self,"Уведомление","Ищем по новому словарю") 
        self.handler.bdAPI.checkComments()
        #QMessageBox.about(self,"Уведомление","Поиск завершен")
    #обновление базы
    def btnMediaClick(self):
        self.buttonMedia.setEnabled(False)
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        QMessageBox.about(self,"Уведомление","Старт обновления БД. Не закрывайте окно") 
        try:
            self.handler.LoadAll(username)
        except Exception as e:
            self.writeReport(str(e))
            QMessageBox.about(self,"Ошибка получения записей",str(e))
            return
        QMessageBox.about(self,"Успешно","База данных комментариев успешно обновлена")
        return
    #событие закрытия окна
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Программа свернута",
            "Программа была свернута в трей.",
            QSystemTrayIcon.Information,
            2000
            )
    #поиск новых комментариев

    def searchNewCommentsClickInThread(self):
        try:
            QMessageBox.about(self,"Уведомление","Поиск новых комментариев") 
            thread = Thread(target=self.searchNewCommentsClick,daemon=True)
            thread.start()
        except Exception as e:
            self.writeReport(str(e))
            QMessageBox.about(self,"Уведомление",str(e))
            self.findNewComButton.setEnabled(True)  
            self.buttonStop.setEnabled(False)
    def searchNewCommentsClick(self):
      
        self.findNewComButton.setEnabled(False)
        self.autoButton.setEnabled(False)
        self.tableComments.clear()
        self.setHeaderTittle()
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        self.handler.searchAndAddNewMediaItems()

        self.setHeaderTittle()
        rows=self.handler.findAbcAllCommentsAndSendIt()
        self.tableComments.setRowCount(len(rows))
        i=0
        for comment in rows:
                self.tableComments.setItem(i, 0,  QtWidgets.QTableWidgetItem(datetime.fromtimestamp(int(comment["comment_date"])).strftime("%d-%m-%Y %H:%M")))
                self.tableComments.setItem(i, 1,  QtWidgets.QTableWidgetItem(comment["comment_text"]))
                self.tableComments.setItem(i, 2,  QtWidgets.QTableWidgetItem(self.handler.bdAPI.getLinkByCommentId(comment['comment_id'])))
                i += 1
        self.setHeaderTittle()
        # QMessageBox.about(self,"Уведомление","Поиск завершен")
        self.findNewComButton.setEnabled(True)
        self.autoButton.setEnabled(True)
        self.searchButtonClick()


    def writeReport(self,text):
        now=datetime.now()
        with open('report.info' , 'a') as file:
            file.write('\n%s\t%s'%(now.strftime("%d-%m-%Y %H:%M"),text)) #дозапись в файл