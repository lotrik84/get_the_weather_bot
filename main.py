import os
from dotenv import load_dotenv
import telebot
from telebot import types
from datetime import date
from datetime import datetime
import locale
import emoji
import weatherAPI

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)
get_emoji = emoji
start = types.BotCommand("start", "Головна")
m_c_weather = types.BotCommand("weather", "Поточна погода")
m_1d_weather = types.BotCommand("todayweather", "Погода на сьогодні")
m_3d_weather = types.BotCommand("3daysweather", "Погода на 3 дні")
m_7d_weather = types.BotCommand("7daysweather", "Погода на тиждень")
bot.set_my_commands(commands=[start, m_c_weather, m_1d_weather, m_3d_weather, m_7d_weather], )
get_weather_api = weatherAPI
weather_hours = ["03", "06", "09", "12", "15", "18", "21"]


@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}, я бот погоди. Можешь скористатися меню'
                                      f' для отримання погоди у твоєму місті.', )


def current_weather(message):
    # bot.delete_message(call.message.chat.id, call.message.id)
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    response = get_weather_api.get_weather(message.text)
    if response:
        # print(response)
        temp = round(response["current"]["temp"])
        humidity = round(response["current"]["humidity"])
        wind_speed = round(response["current"]["wind_speed"])
        pressure = round(response["current"]["pressure"] * 0.75006)
        weather_emoji = get_emoji.getemoji(response["current"]["weather"][0]["id"])
        description = response["current"]["weather"][0]["description"]
        time_stamp = datetime.fromtimestamp(response["current"]["dt"]).strftime("%H:%M")
        bot.send_message(message.chat.id, f'Поточна погода у місті {message.text.title()}:\n\n{time_stamp} {weather_emoji} '
                                          f'{description.capitalize()}\nТемпература: {temp}°C\nВологість: {humidity}%'
                                          f'\nТиск: {pressure} mm\nВітер: {wind_speed} м/с')
    else:
        bot.send_message(message.chat.id, f'Місто "{message.text}" не знайдено')


def today_weather(message):
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    response = get_weather_api.get_weather(message.text)

    if response:
        temp = {}
        humidity = {}
        wind_speed = {}
        pressure = {}
        weather_emoji = {}
        description = {}
        hours = []
        msg = f'Погода на сьогодні {date.today().strftime("%d %B, %A").title()} у місті {message.text.title()}:\n'
        day_today = date.today().strftime("%d")

        for time in response["hourly"]:
            hour = datetime.fromtimestamp(time["dt"]).strftime("%H")
            day = datetime.fromtimestamp(time["dt"]).strftime("%d")
            if day == day_today and hour in weather_hours or (int(day) == int(day_today) + 1 and hour == "00"):
                hours.append(hour)
                temp[hour] = round(time["temp"])
                humidity[hour] = round(time["humidity"])
                wind_speed[hour] = round(time["wind_speed"])
                pressure[hour] = round(time["pressure"] * 0.75006)
                weather_emoji[hour] = get_emoji.getemoji(time["weather"][0]["id"])
                description[hour] = time["weather"][0]["description"]
        for hour in hours:
            msg += f'\n{hour}:00 {weather_emoji[hour]} {description[hour].capitalize()}\nТемпература: {temp[hour]}' \
                   f'°C\nВологість: {humidity[hour]}%\nТиск: {pressure[hour]} mm\nВітер: {wind_speed[hour]} м/с\n'

        bot.send_message(message.chat.id, msg)

    else:
        bot.send_message(message.chat.id, f'Місто "{message.text}" не знайдено')


def couple_days_weather(message, c_days):
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    response = get_weather_api.get_weather(message.text)

    if response:
        temp_day = {}
        temp_night = {}
        humidity = {}
        wind_speed = {}
        pressure = {}
        weather_emoji = {}
        description = {}
        days = []
        msg = f'Погода на найближчі {c_days + 1} дня(ів) у місті {message.text.title()}:\n'
        end = int(date.today().strftime("%d")) + c_days

        for day in response["daily"]:
            c_day = datetime.fromtimestamp(day["dt"]).strftime("%d %B, %A")
            if end >= int(datetime.fromtimestamp(day["dt"]).strftime("%d")):
                days.append(c_day)
                temp_day[c_day] = round(day["temp"]["day"])
                temp_night[c_day] = round(day["temp"]["night"])
                humidity[c_day] = round(day["humidity"])
                wind_speed[c_day] = round(day["wind_speed"])
                pressure[c_day] = round(day["pressure"] * 0.75006)
                description[c_day] = day["weather"][0]["description"]
                weather_emoji[c_day] = get_emoji.getemoji(day["weather"][0]["id"])

        for day in days:
            msg += f'\n{day.title()} {weather_emoji[day]} {description[day].capitalize()}\nТемпература вдень: ' \
                   f'{temp_day[day]}°C\nТемпература вночі:  {temp_night[day]}°C\nВологість: {humidity[day]}%\nТиск: ' \
                   f'{pressure[day]} mm\nВітер: {wind_speed[day]} м/с\n'

        bot.send_message(message.chat.id, msg)

    else:
        bot.send_message(message.chat.id, f'Місто "{message.text}" не знайдено')


@bot.message_handler(commands=['weather'])
def weather(message):
    print(f'weather - {message.from_user.first_name} @{message.from_user.username} '
          f'{datetime.today().strftime("%Y-%m-%d %H:%M")}')

    msg = bot.send_message(message.chat.id, f'Введіть назву міста:')
    bot.register_next_step_handler(msg, current_weather)


@bot.message_handler(commands=['todayweather'])
def weather(message):
    print(f'todayweather - {message.from_user.first_name} @{message.from_user.username} '
          f'{datetime.today().strftime("%Y-%m-%d %H:%M")}')

    msg = bot.send_message(message.chat.id, f'Введіть назву міста:')
    bot.register_next_step_handler(msg, today_weather)


@bot.message_handler(commands=['3daysweather'])
def weather(message):
    print(f'3daysweather - {message.from_user.first_name} @{message.from_user.username} '
          f'{datetime.today().strftime("%Y-%m-%d %H:%M")}')

    msg = bot.send_message(message.chat.id, f'Введіть назву міста:')
    bot.register_next_step_handler(msg, couple_days_weather, 2)


@bot.message_handler(commands=['7daysweather'])
def weather(message):
    print(f'7daysweather - {message.from_user.first_name} @{message.from_user.username} '
          f'{datetime.today().strftime("%Y-%m-%d %H:%M")}')

    msg = bot.send_message(message.chat.id, f'Введіть назву міста:')
    bot.register_next_step_handler(msg, couple_days_weather, 7)


bot.polling()
