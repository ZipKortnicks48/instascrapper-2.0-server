    #отправка сообщения на имейл
from email.mime.text import MIMEText
import smtplib
from email.header    import Header
def send_email(host, to_addr, from_addr): 
        body_text="Test email from Python:\n"
        msg = MIMEText(body_text, 'plain', 'utf-8')
        msg['Subject'] = Header('Поиск комментариев', 'utf-8')
        msg['From'] = from_addr     
        separator=", "
        msg['To'] = separator.join(to_addr)
        server = smtplib.SMTP_SSL(host,port=465)
        server.login('vodokanal482019@gmail.com','Djljrfyfk48')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
if __name__ == "__main__":
    host = "smtp.gmail.com"
    subject = "Test email from Python"
    to_addr = ["it@rkvv.ru"]
    from_addr = "vodokanal482019@gmail.com"
    error=0
    send_email(host,  to_addr, from_addr)

# import telebot
# from telebot import apihelper

# TOKEN = '1191171470:AAFD2RFFpUR0-W_RTq04uco2WpCAZ0CT1b4M'
# bot = telebot.TeleBot(TOKEN)
# bot.send_message('379497515', 'Привет!' )
# bot.polling(none_stop=True)