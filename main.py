# НЕОБХОДИМЫЕ ССЫЛКИ ---------------------------------------------------------------------------------------------------


# http://t.me/Zykov_Daniil_1MD4_bot
# 5200175751:AAFJankWp1rVgTuwls8TFtNcp4WejkdLo5Y
# https://docs.google.com/document/d/1PkfPLCUJMPPj8xeTwqUHu20rQhOXxBwAZ3EbudSbYOU/ed


# ИМПОСТЕРЫ ------------------------------------------------------------------------------------------------------------


import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as b
from datetime import datetime
from pycbrf import ExchangeRates
import json
import bs4
from gettext import find
from io import BytesIO
import BotGames
import SECRET
from menuBot import Menu
import menuBot
from BotGames import Dice
import random
import logging


# ----------------------------------------------------------------------------------------------------------------------


bot = telebot.TeleBot(SECRET.TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE1HZikA-X4PsOYWekoxPv8voOobWn5wACGxQAAk9VcEn_Ed1DKZ44WSQE")
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=Menu.getMenu("Главное меню").markup)




@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Спросить у разработчика', url='@alo0ooooo'))
    bot.send_message(message.chat.id, '  Это первый созданный его руками бот.\n' + 'Бот является проектной работой по предмету "Алоритмизация и програмирование"\n' + 'Наставником на верный путь был ... .\n', reply_markup=keyboard)
    bot.send_message(chat_id, "<b>{1.first_name}</b> обнаружил активными этих пользователей:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, message.json["from"])

    result = goto_menu(chat_id,ms_text)
    if result == True:
        return

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:


        if ms_text == "Уныние (курсы валют)":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton('USD')
            btn2 = telebot.types.KeyboardButton('EUR')
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(chat_id, text='Выбери валюту', reply_markup=markup, parse_mode="html")


        elif ms_text =='USD':
                message_norm = ms_text.strip().lower()
                if message_norm in ['usd', 'eur']:
                    rates = ExchangeRates(datetime.now())
                    bot.send_message(chat_id, text=f"Курс {message_norm.upper()} {float(rates[message_norm.upper()].rate)} мать его рублей!",
                                     parse_mode="html")

        elif ms_text == 'EUR':
                message_norm = ms_text.strip().lower()
                if message_norm in ['usd', 'eur']:
                    rates = ExchangeRates(datetime.now())
                    bot.send_message(chat_id,
                                     text=f"Курс {message_norm.upper()} {float(rates[message_norm.upper()].rate)} мать его рублей!",
                                     parse_mode="html")



        elif ms_text == "АнекдоТ-МЭН":
            bot.send_message(chat_id, text=get_anekdot())


        elif ms_text == "Показать собачку":
            bot.send_message(chat_id, text=f"{get_dog()}\nВот твоя собака <3")


        elif ms_text == "Показать лисичку":
            bot.send_message(chat_id, text=f"{get_fox()}\nВот твоя лисичка <3")


        elif ms_text == "Числа":
            dc = Dice()
            text_game = dc.playerChoice()
            bot.send_message(chat_id, text=text_game)


        elif ms_text in BotGames.GameRPS.values:
            gameRSP = BotGames.getGame(chat_id)
            if gameRSP == None:
                goto_menu(chat_id, "Выход")
                return
            text_game = gameRSP.playerChoice(ms_text)
            bot.send_message(chat_id, text=text_game)
            gameRSP.newGame()


        else:
            bot.send_message(chat_id, text="К сожалению, я не распознал твою команду: " + ms_text)
            goto_menu(chat_id, "Главное меню")


# ----------------------------------------------------------------------------------------------------------------------


def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)
    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)



def get_fox():
    contents = requests.get('https://randomfox.ca/floof/').json()
    urlFOX= contents['image']
    return urlFOX



def get_dog():
    contents = requests.get('https://random.dog/woof.json').json()
    urlDOG = contents['url']
    return urlDOG


import requests
from bs4 import BeautifulSoup



#def parse_rate():

#    URL = "https://www.fontanka.ru/currency.html"
#    HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0", "accept": "*/*"}

#    html = requests.get(URL, headers=HEADERS, params=None)
#    soup = BeautifulSoup(html.text, "html.parser")
#    if html.status_code == 200:
#        #items = soup.find_all("table", class_="J-af9")
#        items = soup.find_all("tbody", class_="J-agb")
#        rates = []
#        for i in items:
#            rates.append({
#                "str": i.find("td", class_="J-d3").get_text(),
#                "val": i.find("td", class_="J-agl").get_text()
#            })
#       return(rates)


#import pandas as pd

#def parse_rate():
    #url = "https://www.fontanka.ru/currency.html"
    #df = pd.read_html(url)[0]
    #return(df.loc[df['Валюта'].isin(['usd','eur']), ['Валюта','Курс']])
    #      (df.loc[df['Валюта'].isin(['usd','eur']), ['Валюта.1','Курс']].apply(lambda x: print(f'{x[0]}: {x[1]}'), axis=1))


#@bot.message_handler(commands=['text'])
#def send_welcome(message):

#    config_dict = get_default_config()
#    config_dict['language'] = 'ru'
#
#    owm = OWM('MY_TOKEN', config_dict)
#    bot = telebot.TeleBot("MY_TOKEN")
#
#    bot.reply_to(message, message.text)
#    mgr = owm.weather_manager()
#    status = weather.detailed_status
#    observation = mgr.weather_at_place(message.text)
#    observation.weather.detailed_status
#    weather = mgr.weather_at_place(message.text).weather
#    temp = weather.temperature('celsius')['temp']
#
#    answer = f"В городе {message.text} сейчас {status}\n"
#    answer += f"Температура воздуха равна {temp}\n\n"
#    if temp < 5:
#       answer += "На улице холодно, рекомендуется одеть курту, шапку и теплый свитер."
#    elif temp < 10:
#        answer += "На улице прохладно, рекомендуется одеть сезонную куртку и свитер."
#    elif temp > 15:
#        answer += "На улице благоприятная погода, но не рекомендуется выходить без кофты."
#    elif temp > 20:
#        answer += "На улице жарко, не забудьте одеть головной убор."

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    bot.send_message(message.chat.id, message)


bot.infinity_polling()

def get_anekdot(url):
    array_anekdots = []
    r = requests.get('https://www.anekdot.ru/last/good')
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    for result in anekdots:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]


# ПУСК -----------------------------------------------------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)
