
import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime
import logging
import random

def r():
    a = random.randint(50,100)
    return a

def start(bot, update):
    a = r()
    asd = "Your Wind is:" , a , " %"
    bot.sendMessage(chat_id=update.message.chat_id, text=("Your Wind is:" , a , " %"))


def getCm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Thanks. Our channel address: telegram.me/zerotoheroir")
    userInfo = update.message.chat
    userMessage = update.message.text
    userId = userInfo['id']
    userName = userInfo['username']
    userFirstName = userInfo['first_name']
    userLastName = userInfo['last_name']
    cn = sqlite3.connect("zthb.sqlite")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    cn.execute("CREATE TABLE IF NOT EXISTS user_comment(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME);")
    cn.execute("INSERT INTO user_comment VALUES (?, ?, ?, ?, ?, ?);", (userId, userName, userFirstName, userLastName, userMessage, datetime.now()))
    cn.commit()
    cn.close()

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unknown Command!")

updater = Updater(token='398344625:AAGwZ74EKvNFWYrKNYaRdkb8doNfjxYb_uU')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

cm_handler = MessageHandler([Filters.text], getCm)
dispatcher.add_handler(cm_handler)

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
updater.stop()
