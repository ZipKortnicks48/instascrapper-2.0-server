import sqlite3
import datetime
import pymysql.cursors
from src.mysql_settings import mysqlSettings
class bdAPI():
    def __init__(self):
        msqlSet=mysqlSettings()
        serv=msqlSet.getServerSettings()
        self.connection = pymysql.connect(host=serv["host"],
                             user=serv['user'],
                             password=serv["password"],                             
                             db=serv["db_name"],
                             charset=serv["charset"],
                             cursorclass=pymysql.cursors.DictCursor)
    def disconnect(self):
        self.connection.close()
    #получаем быстро из базы id пользователя по имени
    def getUserIdFromName(self,name): 
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM people WHERE user_name='%s';"%(name))
            rows = cursor.fetchall()
            return rows[0]["user_id"]
    #добавить новую запись в базу с указанием количества комментариев и ссылкой на нее
    def addMediaItem(self,feed):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT into media (media_id,media_date,user_id,comment_count,media_link) values ('%s','%s','%s','%s','https://www.instagram.com/p/%s/');"%(feed['pk'], feed['device_timestamp'],feed['user']['pk'],feed.get('comment_count',0),feed['code']))
            self.connection.commit()
    #получаем айдишники всех записей 
    def getMediaIds(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT media_id FROM media")
            rows = cursor.fetchall()
            rows.reverse()
            return rows 
    #получаем все записи ЮЗЕРА по айди ЮЗЕРА
    def getMediaOfUser(self,id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT media_id FROM media WHERE user_id='%s'",id)
            rows = cursor.fetchall()
            rows.reverse()
            return rows
    #добавить новый комментарий в базу с отметкой НОВЫЙ
    def addComment(self,comment,media_id):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT into comments (comment_id,comment_text,comment_date,media_id,comment_meet,comment_new) values ('%s','%s','%s','%s',0,1);"%(comment['pk'],comment['text'].lower(),comment['created_at'],media_id))
            self.connection.commit()
    #тащит все последние комменты айди (по 60 штук) из базы
    def takeOldCommentsIds(self,media):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT comment_id FROM comments WHERE media_id='%s';"%(media))
            rows = cursor.fetchall()
            return rows
    #отмечает ВСЕ комменты в базе по словарю, (не нужные в 0) 
    def checkComments(self):
        self.__commentsUnMeet()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT abc_text FROM abc;")
            rows = cursor.fetchall()
            i=1
            if len(rows)==0:
                return
            s=""
            for row in rows:
                if i!=len(rows):
                    s+="comment_text LIKE '%"+row['abc_text']+"%' OR "
                else: 
                    s+="comment_text LIKE '%"+row['abc_text']+"%'"
                i+=1
            s="SELECT comment_id,comment_text FROM comments WHERE %s;"%(s)
            cursor.execute(s)
            rows=cursor.fetchall()
            for row in rows:
                cursor.execute("UPDATE comments SET comment_meet = '1' WHERE comment_id = '%s';"%(row['comment_id']))
            self.connection.commit()
        #отмечает совпавшие новые комменты в базе по словарю
    #отмечает НОВЫЕ комменты в базе по словарю
    def checkNewComments(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT abc_text FROM abc")
            rows = cursor.fetchall()
            i=1
            s=""
            for row in rows:
                if i!=len(rows):
                    s+="comment_text LIKE '%"+row['abc_text']+"%' OR "
                else: 
                    s+="comment_text LIKE '%"+row['abc_text']+"%'"
                i+=1
            cursor.execute("SELECT comment_id,comment_text FROM comments WHERE comment_new='1' AND %s;"%(s))
            rows=cursor.fetchall()
            for row in rows:
                cursor.execute("UPDATE comments SET comment_meet = '1' WHERE comment_id = '%s';"%(row['comment_id']))
            self.connection.commit()
        #вывод нужных по словарю
    #показывает комменты базы, совпадающие со словарем
    def showGoodComments(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE comment_meet='1';")
            rows = cursor.fetchall()
            return rows
    #показывает новые комменты базы, совпадающие со словарем
    def showGoodNewComments(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE comment_meet='1' AND comment_new='1';")
            rows = cursor.fetchall()
            return rows 
    #получает ссылку на запись поста по ид комментария
    def getLinkByCommentId(self,id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT media_link FROM media WHERE media_id IN (SELECT media_id FROM comments WHERE comment_id='%s');"%id)
            comment=cursor.fetchall()
            return comment[0]['media_link']
    #все комменты вернуть в meet=0
    def __commentsUnMeet(self):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE comments SET comment_meet = '0';")
            self.connection.commit()
    #отмечает прочитанные комменты
    def commentsUnNew(self):
       with self.connection.cursor() as cursor:
        cursor.execute("UPDATE comments SET comment_new = '0';")
        self.connection.commit()
    #возвращает слова по строке поиска 
    def getCommentHandsearch(self,word):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE comment_text LIKE '%"+word+"%';")
            comments=cursor.fetchall()
            return comments
    #возвращает словарь
    def getABC(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT abc_text FROM abc;")
            abc=cursor.fetchall()
            return abc
    def updateABC(self,strings):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM abc;")
            self.connection.commit()
            i=0
            for s in strings:
                if s != "": 
                    cursor.execute("INSERT into abc (abc_id,abc_text) values ('%s','%s');"%(i,s))
                i+=1
            self.connection.commit()
        #возвращает адреса
    def getMail(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT email_text FROM emails;")
            emails=cursor.fetchall()
            return emails
    def updateMail(self,strings):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM emails;")
            self.connection.commit()
            i=0
            for s in strings:
                if s != "": 
                    cursor.execute("INSERT into emails (email_id,email_text) values ('%s','%s');"%(i,s))
                i+=1
            self.connection.commit()
if __name__ == "__main__":
    m=bdAPI()
    m.getUserIdFromName("igor_artamonov48")
    m.checkNewComments()