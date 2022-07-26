# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import telebot
import matbi

bot = telebot.TeleBot("5151066340:AAGxI-5HIyEtlJeJL3WwX67wUvTUqZaZshQ")
words = matbi.censured


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


@bot.message_handler(commands=['start'])
def star(m, res=False):
    bot.send_message(m.chat.id, 'отправь, что-либо, а я поищу на википедии')


@bot.message_handler(commands=['weather'])
def weather(m, res=False):
    bot.send_message(m.chat.id, '454565')
    print(6)
    url = 'https://yandex.ru/pogoda/details?lat=47.222078&lon=39.720349&via=ms'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find('div', class_="b-page__container").find('div', class_="content").find('div', class_="forecast"
                                                                                                           "-details"
                                                                                                           "-segment").\
        find('div', class_="forecast-details-segment__container").find('div', class_="forecast-details i-bem "
                                                                                     "forecast-details_js_inited").find(
        "article", class_="card").find("div", class_="forecast-details__day-info").find('table', class_="weather-table")\
        .find("tbody", class_="weather-table__body").find_all("tr", class_="weather-table__row")
    print(quotes)
    for item in quotes:
        print(item.text)
    bot.send_message(m.chat.id, 'Погода сейчас: ' + '')


@bot.message_handler(content_types=["text"])
def cleaner(message):
    print(message)
    censured = False
    phrase = message.text.lower().replace(" ", "")

    d = {'а': ['а', 'a', '@'],
         'б': ['б', '6', 'b'],
         'в': ['в', 'b', 'v'],
         'г': ['г', 'r', 'g'],
         'д': ['д', 'd'],
         'е': ['е', 'e'],
         'ё': ['ё', 'e'],
         'ж': ['ж', 'zh', '*'],
         'з': ['з', '3', 'z'],
         'и': ['и', 'u', 'i'],
         'й': ['й', 'u', 'i'],
         'к': ['к', 'k', 'i{', '|{'],
         'л': ['л', 'l', 'ji'],
         'м': ['м', 'm'],
         'н': ['н', 'h', 'n'],
         'о': ['о', 'o', '0'],
         'п': ['п', 'n', 'p'],
         'р': ['р', 'r', 'p'],
         'с': ['с', 'c', 's'],
         'т': ['т', 'm', 't'],
         'у': ['у', 'y', 'u'],
         'ф': ['ф', 'f'],
         'х': ['х', 'x', 'h', '}{'],
         'ц': ['ц', 'c', 'u,'],
         'ч': ['ч', 'ch'],
         'ш': ['ш', 'sh'],
         'щ': ['щ', 'sch'],
         'ь': ['ь', 'b'],
         'ы': ['ы', 'bi'],
         'ъ': ['ъ'],
         'э': ['э', 'e'],
         'ю': ['ю', 'io'],
         'я': ['я', 'ya']
         }

    for key, value in d.items():
        for letter in value:
            for phr in phrase:
                if letter == phr:
                    phrase = phrase.replace(phr, key)

    for word in words:
        for part in range(len(phrase)):
            fragment = phrase[part: part + len(word)]
            if distance(fragment, word) <= len(word) * 0.25:
                bot.send_message(message.chat.id, "Найдено запрещённое слово у " + message.from_user.username)
                censured = True

    if censured:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass


bot.polling(none_stop=True, interval=0)
