import os
import bot
from flask import Flask, request
from telegram import Update

import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime
import logging
import random


application = Flask(__name__, instance_path=os.environ['OPENSHIFT_REPO_DIR'])
update_queue, bot_instance = bot.setup(webhook_url='https://{}/{}'.format(
    os.environ['OPENSHIFT_GEAR_DNS'],
    bot.TOKEN
))


@application.route('/')
def not_found():
    """Server won't respond in OpenShift if we don't handle the root path."""
    return ''


@application.route('/' + bot.TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.json:
        update_queue.put(Update.de_json(request.json, bot_instance))
    return ''


if __name__ == '__main__' or __name__ == '__bot__':
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
application.run(host=ip, port=port)


def r():
    a = random.randint(50,100)
    return a

def start(bot, update):
    a = r()
    asd = "Your Wind is:" , a , " %"
    bot.sendMessage(chat_id=update.message.chat_id, text=("Your Wind is:" , a , " %"))


def getCm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Thanks")
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

updater = Updater(token='398344625:AAEBd9EeQB-5YHeuzYtV2LCX87hXQCeSn80')
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
