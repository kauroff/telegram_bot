import os
import telebot
from datetime import datetime
from telebot import types

import requests

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')


def function(message, currency):
    if message.text == 'текущий':
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
        response = requests.get(url, headers={"apikey": API_KEY})
        rate = response.json()['rates']['RUB']
        bot.send_message(message.chat.id, f'Курс {currency} к рублю: {rate:.2f}')
    else:
        date_list = message.text.split('.')
        formated_date = []
        for i in reversed(range(len(date_list))):
            formated_date.append(date_list[i])
        user_date = '-'.join(formated_date)
        # user_date = (datetime.strptime(date_str, '%Y.%m.%d'))
        url = f"https://api.apilayer.com/exchangerates_data/{user_date}?&base={currency}"
        response = requests.get(url, headers={"apikey": API_KEY})
        rate = response.json()['rates']['RUB']
        year, month, day = user_date.split('-')
        bot.send_message(message.chat.id, f'Курс {currency} к рублю: {rate:.2f} на момент {day}.{month}.{year}')


@bot.message_handler(commands=['start'])
def main(message):
    # markup = types.ReplyKeyboardMarkup()
    # markup.row(types.KeyboardButton('Начать'))
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Я - <b>бот</b>, который подсказывает курс валюты',
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


@bot.callback_query_handler(func=lambda callback: True)
def callback_data(call):
    currency = call.data
    bot.send_message(call.message.chat.id, 'Интересует текущий курс или за конкретную дату?')
    bot.send_message(call.message.chat.id,
                     'Если <b>текущий</b> - напишите "текущий"\nЗа <b>конкретную дату</b> - укажите дату в формате ДД.ММ.ГГГГ',
                     parse_mode='html')
    bot.register_next_step_handler(call.message, function, currency)


bot.polling(none_stop=True)
