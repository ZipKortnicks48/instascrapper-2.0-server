#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError,MediaTypes
from datetime import datetime
import asyncio
import time
import sched
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.header    import Header
import threading
from threading import Thread
import schedule
from appUI.app_main import App 

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    #обработчик формы



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()