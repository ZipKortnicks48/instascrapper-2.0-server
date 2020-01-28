import smtplib
 
def send_email(host, subject, to_addr, from_addr, body_text): 
    separator=", "
    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % separator.join(to_addr),
        "Subject: %s" % subject ,
        "",
        body_text
    ))
 
    server = smtplib.SMTP_SSL(host,port=465)
    server.login('instagram@rkvv.ru','asdqwe123')
    server.sendmail(from_addr, to_addr, BODY)
    server.quit()
 
 
if __name__ == "__main__":
    host = "smtp.yandex.ru"
    subject = "Test email from Python"
    to_addr = ["alex.sirokvasoff2011@yandex.ru","it@rkvv.ru"]
    from_addr = "instagram@rkvv.ru"
    body_text = "str"
    error=0
    try:
        send_email(host, subject, to_addr, from_addr, body_text)
    except Exception as e:
        error+=1