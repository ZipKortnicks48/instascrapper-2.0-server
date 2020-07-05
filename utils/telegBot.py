import telebot
from telebot import apihelper

TOKEN = '1191171470:AAFD2RFpUR0-W_RTqO4uco2WpCAZOCT1b4M'
bot = telebot.TeleBot(TOKEN)

bot.send_message('-379497515', "*Привет!*_Это я_",parse_mode= 'Markdown' )
bot.polling(none_stop=True)