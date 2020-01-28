import sqlite3
import datetime

#создает БД если запустить __main__
def makeSettingsDataBase():
    sqlite3.SQLITE_PRAGMA
    connection = sqlite3.connect("mysql_settings.db") 
    cursor = connection.cursor()
    # Создание таблицы адресов
    cursor.execute("CREATE TABLE IF NOT EXISTS emails (email_id text primary key, email_text text)")
    # Создание таблицы настроек подключения к базе данных MySql
    cursor.execute("CREATE TABLE IF NOT EXISTS mysql_set (set_id text prinary key,host text, user text, password text, db_name text, charset text)")
    connection.close()
class mysqlSettings():
    def connection(self):
        sqlite3.SQLITE_PRAGMA
        connection = sqlite3.connect("./src/mysql_settings.db") 
        cursor = connection.cursor()
        return connection,cursor
    def getServerSettings(self):
        connection,cursor=self.connection()
        cursor.execute("SELECT * FROM mysql_set;")
        settings = cursor.fetchall()
        settings=settings[0]
        connection.close()
        return {"set_id":settings[0],"host":settings[1],"user":settings[2],"password":settings[3],"db_name":settings[4],"charset":settings[5]}
    def updateServerSettings(self,settings):
        connection,cursor=self.connection()
        cursor.execute("DELETE FROM mysql_set;")
        connection.commit()
        i=0
        if settings != "": 
            cursor.execute("INSERT into mysql_set values ('0','%s','%s','%s','%s','%s');"%(settings[0],settings[1],settings[2],settings[3],settings[4]))
        i+=1
        connection.commit()
        connection.close()
        #возвращает адреса
    def getMail(self):
        connection,cursor=self.connection()
        cursor.execute("SELECT email_text FROM emails;")
        emails=cursor.fetchall()
        connection.close()
        return emails
        #обновляет настройки
    def updateMail(self,strings):
        connection,cursor=self.connection()
        cursor.execute("DELETE FROM emails;")
        connection.commit()
        i=0
        for s in strings:
            if s != "": 
                cursor.execute("INSERT into emails values ('%s','%s');"%(i,s))
            i+=1
        connection.commit()
        connection.close()
        
    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    #makeSettingsDataBase()  
    s=mysqlSettings()
    s.updateServerSettings(['192.168.28.147', 'admin', 'admin', 'instagram', 'utf8mb4'])
    r=s.getServerSettings()
    s.getMail()