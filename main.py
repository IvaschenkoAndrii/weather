import telebot
from pyowm.commons.exceptions import NotFoundError
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'  # язык, на котором сообщается погода

owm = OWM('e714165bcefb7fc7c6179a62ff108db8', config_dict)  # токен с OpenWeather
mgr = owm.weather_manager()

bot = telebot.TeleBot("5505413910:AAGnIzbNR99BrJRy4inbjRTfYL9r2IxOXQ0")  # токен бота


@bot.message_handler(content_types=["text"])  # Декоратор @message_handler реагирует на входящие сообщение.
def send_echo(message):
    try:  # проверка ошибки, если город не найден
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']

        answer = 'В городе ' + message.text + ' сейчас ' + w.detailed_status + "\n"
        answer2 = 'Температура воздуха ' + str(round(w.temperature('celsius')['temp'])) + ' °С' + "\n"

        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, answer2)
        bot.send_message(message.chat.id, 'Введите город')

    except NotFoundError:
        answer = 'Не найдено место: ' + message.text
        bot.send_message(message.chat.id, 'Такой город не найден')
        bot.send_message(message.chat.id, 'Введите город')


bot.polling(non_stop=True)
