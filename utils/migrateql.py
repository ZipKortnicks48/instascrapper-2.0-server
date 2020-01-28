import pymysql.cursors
import datetime  
import sqlite3
# Подключиться к базе данных.
connection = pymysql.connect(host='192.168.28.147',
                             user='admin',
                             password='admin',                             
                             db='instagram',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
 

tables=["comments","media","people","emails","abc"]
def takeSQLite(table):
        sqlite3.SQLITE_PRAGMA
        conn = sqlite3.connect("instagram.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+table)
        rows = cursor.fetchall()
        l=len(rows)
        conn.close()
        return rows
def deleteMySQL(table):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM "+table)
        # cursor.close()
        connection.commit()
        # connection.close()
def makeMig(table):
        arr=takeSQLite(table)
        for item in arr:
            sql=""
            for value in item:
                value=str(value).replace("'","\"")
                value=str(value).replace('"',"\"")
                sql+="'"+str(value)+"',"
            sql=sql[0:-1]
            with connection.cursor() as cursor:
                if(table=="people"):
                    sql="INSERT INTO "+table+" (user_id,user_name,user_surname) VALUES ("+sql+");"
                if(table=="emails"):
                    sql="INSERT INTO "+table+" (email_id,email_text) VALUES ("+sql+");"
                if(table=="abc"):
                    sql="INSERT INTO "+table+" (abc_id,abc_text) VALUES ("+sql+");"
                if(table=="media"):
                    sql="INSERT INTO "+table+" (media_id,media_date,user_id,comment_count,media_link) VALUES ("+sql+");"
                if(table=="comments"):
                    sql="INSERT INTO "+table+" (comment_id,comment_text,comment_date,media_id,comment_meet,comment_new) VALUES ("+sql+");"
                cursor.execute(sql)
                cursor.close()
                connection.commit()
                
def main():
    try:
        for table in tables:
            deleteMySQL(table)
    except Exception as e:
        print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))+str(e))
    print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))+" start")
    try:
        for table in reversed(tables):
            makeMig(table)
            print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))+" success table "+table)
    except Exception as e:
        print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))+str(e))
    print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))+" finish")
    connection.close()
if __name__ == "__main__":
    main()     
