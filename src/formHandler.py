from src.bdmeth import bdAPI
from src.finder import Finder
from datetime import datetime, date, time
from PyQt5.QtWidgets import QMessageBox
class formHandler():
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
                comments=self.f.takeCommentsWithoutCircle(row[0],60)
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
        #self.bdAPI.commentsUnNew()#комментарии прочитаны ВЕРНУТЬ НА МЕСТО!!
        return rows
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
        oldMediaIds=list(map(lambda x: int(x["media_id"]),oldMediaIds))
        for media in newMediaIds:
            if media['pk'] in oldMediaIds:
                break
            else:
                self.bdAPI.addMediaItem(media)            
