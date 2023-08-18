import os
import telebot
from datetime import datetime
from telebot import types

import requests

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')


@bot.message_handler(commands=['start'])
def main(message):
    # markup = types.ReplyKeyboardMarkup()
    # markup.row(types.KeyboardButton('Начать'))
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Я - <b>бот</b>, который подсказывает курс валюты (<b>USD</b>/<b>EUR</b>).',
                     parse_mode='html')
    # bot.register_next_step_handler(message, function)
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton('USD \U0001F1FA\U0001F1F8', callback_data='USD')
    btn2 = types.InlineKeyboardButton('EUR \U0001F1EA\U0001F1FA', callback_data='EUR')
    btn3 = types.InlineKeyboardButton('GBP \U0001F1EC\U0001F1E7', callback_data='GBP')
    btn4 = types.InlineKeyboardButton('CNY \U0001F1E8\U0001F1F3', callback_data='CNY')
    btn5 = types.InlineKeyboardButton('JPY \U0001F1EF\U0001F1F5', callback_data='JPY')
    btn6 = types.InlineKeyboardButton('AED \U0001F1E6\U0001F1EA', callback_data='AED')
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'Интересующая валюта:', reply_markup=markup)
    # markup = types.InlineKeyboardMarkup(row_width=2)
    # btn1 = types.InlineKeyboardButton('Сейчас', callback_data='now')
    # btn2 = types.InlineKeyboardButton('За конкретную дату', callback_data='date')
    # markup.row(btn1, btn2)
    # bot.send_message(message.chat.id, 'Курс на текущий момент или за конкретную дату?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_data(call):
    currency = call.data
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY})
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Сейчас', callback_data='now')
    btn2 = types.InlineKeyboardButton('За конкретную дату', callback_data='date')
    markup.row(btn1, btn2)
    bot.send_message(call.message.chat.id, 'Курс на текущий момент или за конкретную дату?', reply_markup=markup)
    #rate = response.json()['rates']['RUB']
    # bot.send_message(call.message.chat.id, f'Курс {currency} к рублю: {rate:.2f}')
    @bot.callback_query_handler(func=lambda callback: True)
    def callback_data(call):
        time = call.data
        if time == 'now':
            rate = response.json()['rates']['RUB']
            bot.send_message(call.message.chat.id, f'Курс {currency} к рублю на данный момент: {rate:.2f}')
        elif time == 'date':
            bot.send_message(call.message.chat.id, f'Укажите дату в формате ДД.ММ.ГГ (не ранее 99г.)')


# try:
    #     time = ...
    # except ValueError:
    #     bot.send_message(message.chat.id, 'Курс на текущий момент или за конкретную дату?', reply_markup=markup)



bot.polling(none_stop=True)
