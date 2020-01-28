import sqlite3
import datetime

#создает БД если запустить
def makeDB():
    sqlite3.SQLITE_PRAGMA
    conn = sqlite3.connect("instagram.db") 
    cursor = conn.cursor()
    #включение внешнего ключа
    cursor.execute("PRAGMA foreign_keys = ON")
    # Создание таблицы людей
    cursor.execute("CREATE TABLE IF NOT EXISTS people (user_id text primary key, user_name text, user_surname text)")
    # Создание таблицы записей
    cursor.execute("CREATE TABLE IF NOT EXISTS media (media_id text primary key,media_date integer, user_id text, comment_count integer, media_link text, FOREIGN KEY (user_id) REFERENCES people (user_id) )")
    # Создание таблицы комментариев
    cursor.execute("CREATE TABLE IF NOT EXISTS comments (comment_id text primary key, comment_text text, comment_date integer, media_id text, comment_meet integer DEFAULT 0, comment_new integer DEFAULT 0, FOREIGN KEY (media_id) REFERENCES media (media_id) )")
    # Создание таблицы словаря
    cursor.execute("CREATE TABLE IF NOT EXISTS abc (abc_id text primary key, abc_text text)")
    # Создание таблицы адресов
    cursor.execute("CREATE TABLE IF NOT EXISTS emails (email_id text primary key, email_text text)")
class bdAPI():
    def __init__(self):
        sqlite3.SQLITE_PRAGMA
        self.conn = sqlite3.connect("instagram.db") 
        self.cursor = self.conn.cursor()
    #получаем быстро из базы id пользователя по имени
    def getUserIdFromName(self,name): 
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM people WHERE user_name='%s';"%(name))
        rows = cursor.fetchall()
        conn.close()
        return rows[0][0]
    #добавить новую запись в базу с указанием количества комментариев и ссылкой на нее
    def addMediaItem(self,feed):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("INSERT into media values ('%s','%s','%s','%s','https://www.instagram.com/p/%s/');"%(feed['pk'], feed['device_timestamp'],feed['user']['pk'],feed.get('comment_count',0),feed['code']))
        conn.commit()
        conn.close()
    #получаем айдишники всех записей 
    def getMediaIds(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT media_id FROM media")
        rows = cursor.fetchall()
        rows.reverse()
        conn.close()
        return rows  
    #получаем все записи ЮЗЕРА по айди ЮЗЕРА
    def getMediaOfUser(self,id):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT media_id FROM media WHERE user_id='%s'",id)
        rows = cursor.fetchall()
        rows.reverse()
        conn.close()
        return rows
    #добавить новый комментарий в базу с отметкой НОВЫЙ
    def addComment(self,comment,media_id):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("INSERT into comments values ('%s','%s','%s','%s',0,1);"%(comment['pk'],comment['text'].lower(),comment['created_at'],media_id))
        conn.commit()
        conn.close()
    #тащит все последние комменты айди (по 60 штук) из базы
    def takeOldCommentsIds(self,media):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT comment_id FROM comments WHERE media_id='%s';"%(media))
        rows = cursor.fetchall()
        conn.close()
        return rows
    #отмечает ВСЕ комменты в базе по словарю, (не нужные в 0) 
    def checkComments(self):
        self.__commentsUnMeet()
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT abc_text FROM abc")
        rows = cursor.fetchall()
        i=1
        if len(rows)==0:
            return
        str=""
        for row in rows:
            if i!=len(rows):
                str+="comment_text LIKE '%"+row[0]+"%' OR "
            else: 
                str+="comment_text LIKE '%"+row[0]+"%'"
            i+=1
        str="SELECT comment_id,comment_text FROM comments WHERE %s;"%(str)
        cursor.execute(str)
        rows=cursor.fetchall()
        for row in rows:
            cursor.execute("UPDATE comments SET comment_meet = '1' WHERE comment_id = '%s';"%(row[0]))
        conn.commit()
        conn.close()
        str=""
        #отмечает совпавшие новые комменты в базе по словарю
    #отмечает НОВЫЕ комменты в базе по словарю
    def checkNewComments(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT abc_text FROM abc")
        rows = cursor.fetchall()
        i=1
        str=""
        for row in rows:
            if i!=len(rows):
                str+="comment_text LIKE '%"+row[0]+"%' OR "
            else: 
                str+="comment_text LIKE '%"+row[0]+"%'"
            i+=1
        cursor.execute("SELECT comment_id,comment_text FROM comments WHERE comment_new='1' AND %s;"%(str))
        rows=cursor.fetchall()
        for row in rows:
            cursor.execute("UPDATE comments SET comment_meet = '1' WHERE comment_id = '%s';"%(row[0]))
        conn.commit()
        conn.close()

        #вывод нужных по словарю
    #показывает комменты базы, совпадающие со словарем
    def showGoodComments(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments WHERE comment_meet='1';")
        rows = cursor.fetchall()
        conn.close()
        return rows
    #показывает новые комменты базы, совпадающие со словарем
    def showGoodNewComments(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments WHERE comment_meet='1' AND comment_new='1';")
        rows = cursor.fetchall()
        conn.close()
        return rows 
    #получает ссылку на запись поста по ид комментария
    def getLinkByCommentId(self,id):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT media_link FROM media WHERE media_id IN (SELECT media_id FROM comments WHERE comment_id='%s');"%id)
        comment=cursor.fetchall()
        conn.close()
        return comment[0][0]
    #все комменты вернуть в meet=0
    def __commentsUnMeet(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("UPDATE comments SET comment_meet = '0' WHERE comment_id IN (SELECT comment_id FROM comments);")
        conn.commit()
        conn.close()
    #отмечает прочитанные комменты
    def commentsUnNew(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("UPDATE comments SET comment_new = '0' WHERE comment_id IN (SELECT comment_id FROM comments);")
        conn.commit()
        conn.close()
    #возвращает слова по строке поиска 
    def getCommentHandsearch(self,word):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments WHERE comment_text LIKE '%"+word+"%';")
        comments=cursor.fetchall()
        conn.close()
        return comments
    #возвращает словарь
    def getABC(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT abc_text FROM abc;")
        abc=cursor.fetchall()
        conn.close()
        return abc
    def updateABC(self,strings):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM abc;")
        conn.commit()
        i=0
        for s in strings:
            if s != "": 
                cursor.execute("INSERT into abc values ('%s','%s');"%(i,s))
            i+=1
        conn.commit()
        conn.close()
        #возвращает адреса
    def getMail(self):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT email_text FROM emails;")
        emails=cursor.fetchall()
        conn.close()
        return emails
    def updateMail(self,strings):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emails;")
        conn.commit()
        i=0
        for s in strings:
            if s != "": 
                cursor.execute("INSERT into emails values ('%s','%s');"%(i,s))
            i+=1
        conn.commit()
        conn.close()
        
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    makeDB()  # то запускаем функцию main()