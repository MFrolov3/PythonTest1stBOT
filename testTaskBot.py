import telebot
import time
import numpy as np
import pandas as pd
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

#здесь укажите токен вашего бота
token='6324734121:AAGySoXQrRvGLQ09MkbmgkHfgwBmJNbnjmA'
bot=telebot.TeleBot(token)
#здесь укажите телеграм id менеджера
manager_id = '1443316013'


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(manager_id,'Здравствуйте. Задание выдается командой /give_task')
	
doneButton = InlineKeyboardButton('сделано', callback_data = 'yes')
notDoneButton = InlineKeyboardButton('не сделано', callback_data = 'no')
markup = InlineKeyboardMarkup()
markup.add(doneButton, notDoneButton)
index = 0
not_ignored = True
#сюда можно загрузить таблицу аналогичную этой
df = pd.read_excel('TableForTTBot.xlsx')
task_quantity = df.shape[0]

@bot.message_handler(commands=['give_task'])
def button_message(message):
    global not_ignored
    global index
    global df
    tsk = str(df['task'][index]) + str(' / ') + str(df['date'][index]) + str(' / ') + str(df['time'][index])
    usr_id = str(int(df['tel_id'][index]))
    bot.send_message(usr_id, tsk, reply_markup=markup)
    not_ignored = False
    time.sleep(df['answer_time'][index])
    if not not_ignored:
        bot.send_message(manager_id, tsk + str(' / пользователь id-') + usr_id + ' / проигнорировал(а)')
        bot.delete_message(usr_id, message.message_id+1)
        if index < task_quantity-1:
            index += 1
               
@bot.callback_query_handler(func = lambda query: query.data == 'yes')
def process_callback_1(query):
    global not_ignored
    global df
    global index
    tsk = str(df['task'][index]) + str(' / ') + str(df['date'][index]) + str(' / ') + str(df['time'][index])
    usr_id = str(int(df['tel_id'][index]))
    bot.send_message(manager_id, tsk + str(' / пользователь id-') + usr_id + ' / сделал(а)')
    bot.delete_message(usr_id, query.message.message_id)
    not_ignored = True
    if index < task_quantity-1:
        index += 1

@bot.callback_query_handler(func = lambda query: query.data == 'no')
def process_callback_2(query):
    global not_ignored
    global df
    global index
    tsk = str(df['task'][index]) + str(' / ') + str(df['date'][index]) + str(' / ') + str(df['time'][index])
    usr_id = str(int(df['tel_id'][index]))
    bot.send_message(manager_id, tsk + str(' / пользователь id-') + usr_id + ' / не сделал(а)')
    bot.delete_message(usr_id, query.message.message_id) 
    not_ignored = True  
    if index < task_quantity-1:
        index += 1
        
                                    
bot.infinity_polling()