# -*- coding: utf-8 -*-
import sys
from src.finder import Finder
from src.bdmeth import bdAPI
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError,MediaTypes
from datetime import datetime
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.header    import Header
from PyQt5.QtWidgets import QMessageBox
import time
class scrapper():
    def __init__(self,username):
        self.bdAPI=bdAPI()#экземпяр БД класса
        self.user_id=self.bdAPI.getUserIdFromName(username)
        self.f=Finder(self.user_id) #экземпяр инстаграм класса
    #добавление всех записей
    def asyncLoadAllMediaInfo(self,username):
        max_id=-1
        errors=0
        while max_id!=-2:
            feed,max_id = self.f.findFeed(max_id)
            #сохранение записей из feed
            for item in feed:
                try: 
                    self.bdAPI.addMediaItem(item)    
                except:
                    errors+=1
                    continue
    #загрузка комментариев
    def loadComments(self):#все комментарии здесь попадают в базу  
        rows=self.bdAPI.getMediaIds()
        for row in rows:
            max_id=-1
            errors=0
            try:
                comments=self.f.takeCommentsWithoutCircle(row[0],60) #было 20
                for item in comments:
                    try: 
                        self.bdAPI.addComment(item,row[0])    
                    except:
                        errors+=1
                        continue
            except Exception as e:
                self.writeReport(str(e))
                QMessageBox.about(self,"Ошибка получения комментариев",str(e))
    #поиск комментариев их запись и выдача подходящих
    def findAbcAllCommentsAndSendIt(self):
        self.bdAPI.commentsUnNew()#комментарии прочитаны
        rows=self.bdAPI.getMediaIds()
        for row in rows:
            commentsOld=self.bdAPI.takeOldCommentsIds(row['media_id'])#старые 50
            commentsOldN=list(map(lambda x: int(x['comment_id']),commentsOld))
            commentsNew=self.f.takeCommentsWithoutCircle(row['media_id'],50)#новые 50
            for comment in commentsNew:
                if comment['pk'] in commentsOldN:
                    break
                else:
                    self.bdAPI.addComment(comment,row['media_id'])#добавляем в базу новые комментарии
        self.bdAPI.checkNewComments()#отмечает все новые комменты по словарю
        rows=self.bdAPI.showGoodNewComments()#получает новые и отмеченные для единовременного их вывода на экран
        self.bdAPI.commentsUnNew()#комментарии прочитаны
    #перезагрузка базы
    def LoadAll(self,name):
        self.asyncLoadAllMediaInfo(name)  
        self.loadComments()
        self.bdAPI.checkComments()
    def writeReport(self,text):
        now=datetime.now()
        with open('report.info' , 'a') as file:
            file.write('\n%s\t%s'%(now.strftime("%d-%m-%Y %H:%M"),text)) #дозапись в файл
    #проверка на наличие новой записи стены
    def searchAndAddNewMediaItems(self):
        oldMediaIds=self.bdAPI.getMediaIds()
        newMediaIds=self.f.findNewFeed()
        # igtvs=self.f.findIGTV()
        oldMediaIds=list(map(lambda x: int(x["media_id"]),oldMediaIds))
        for media in newMediaIds:
            if media['pk'] in oldMediaIds:
                break
            else:
                self.bdAPI.addMediaItem(media)  
        # for igtv in igtvs:
        #     if int(igtv['node']['id']) in oldMediaIds:
        #         break
        #     else:
        #         self.bdAPI.addIGTV(igtv['node'])   

class App():
    def __init__(self):
        try:
            username=sys.argv[1]
            self.handler=scrapper(username)
        except:
            username="igor_artamonov48"
            self.handler=scrapper(username)
    def jobException(self):
        try:
            self.job()
        except Exception as e:
            self.handler.writeReport("Ошибка в цикле авторежима: "+str(e))        
            error_text="Ошибка в цикле авторежима: "+str(e)
            self.send_email_error(error_text,"smtp.yandex.ru", ['alex.sirokvasoff2011@yandex.ru'], "instagram@rkvv.ru")
        #циклы авторежима
    def job(self):  
            self.handler.bdAPI.commentsUnNew()#комментарии прочитаны БД
            self.handler.searchAndAddNewMediaItems()
            rows=self.handler.bdAPI.getMediaIds()
            for row in rows:
                commentsOld=self.handler.bdAPI.takeOldCommentsIds(row['media_id'])#старые 50
                commentsOldN=list(map(lambda x: int(x['comment_id']),commentsOld))
                commentsNew=self.handler.f.takeCommentsWithoutCircle(row['media_id'],50)#новые 50 2235850379474987758
                for comment in commentsNew:
                    if comment['pk'] in commentsOldN:
                        break
                    else:
                        self.handler.bdAPI.addComment(comment,row['media_id'])#добавляем в базу новые комментарии
            self.handler.bdAPI.checkNewComments()#отмечает все новые комменты по словарю
            rows=self.handler.bdAPI.showGoodNewComments()#получает новые и отмеченные для единовременной их отправки на почту
            if len(rows)!=0:
                host = "smtp.yandex.ru"
                subject = "Test email from Python"
                to_addr = self.handler.bdAPI.getMail()
                from_addr = "instagram@rkvv.ru"
                error=0
                self.handler.writeReport("Найдено (%s) комментариев(комментарий)."%str(len(rows)))
                self.send_email(rows,host,  to_addr, from_addr)
            else:
                self.handler.writeReport("Комментарии не обнаружены.")
            self.handler.bdAPI.commentsUnNew()#комментарии прочитаны
            self.handler.writeReport("Успешный цикл авторежима.")
    #отправка сообщения на имейл
    def send_email(self,rows,host, to_addr, from_addr): 
        to_addr=list(map(lambda x: x['email_text'],to_addr))
        body_text="На странице были отслежены следующие комментарии:\n"
        for row in rows:
            body_text+="\nТекст комментария:\n%s\nСсылка на запись в инстаграм:\n%s\nВремя публикации:\n%s\n"%(row['comment_text'],self.handler.bdAPI.getLinkByCommentId(row['comment_id']),datetime.fromtimestamp(int(row['comment_date'])).strftime("%d-%m-%Y %H:%M"))
        msg = MIMEText(body_text, 'plain', 'utf-8')
        msg['Subject'] = Header('Обнаружение комментариев', 'utf-8')
        msg['From'] = from_addr     
        separator=", "
        msg['To'] = separator.join(to_addr)
        server = smtplib.SMTP_SSL(host,port=465)
        server.login('instagram@rkvv.ru','asdqwe123')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        self.handler.writeReport("Успешная рассылка.")
    def send_email_error(self,error_text,host, to_addr, from_addr): 
        body_text=error_text+"\n"
        msg = MIMEText(body_text, 'plain', 'utf-8')
        msg['Subject'] = Header('ОШИБКА СКРАППЕРА!!!', 'utf-8')
        msg['From'] = from_addr     
        separator=", "
        msg['To'] = separator.join(to_addr)
        server = smtplib.SMTP_SSL(host,port=465)
        server.login('instagram@rkvv.ru','asdqwe123')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        self.handler.writeReport("Успешная отправка ошибки.")
if __name__ == "__main__":
    app=App()
    app.jobException()