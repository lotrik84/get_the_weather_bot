import os
from dotenv import load_dotenv
import telebot
from telebot import types
from datetime import date
from datetime import datetime
import locale
import emoji
import weatherAPI as get_weather_api
from weather_logs import weather_logs
from usersCities import get_user_cities, update_user_cities

load_dotenv("./config/.env")
os.environ["TZ"] = "Europe/Kiev"

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)
get_emoji = emoji
start = types.BotCommand("start", "Головна")
m_c_weather = types.BotCommand("weather", "Поточна погода")
m_1d_weather = types.BotCommand("todayweather", "Погода на сьогодні")
m_3d_weather = types.BotCommand("3daysweather", "Погода на 3 дні")
m_7d_weather = types.BotCommand("5daysweather", "Погода на 5 днів")
bot.set_my_commands(
    commands=[start, m_c_weather, m_1d_weather, m_3d_weather, m_7d_weather],
)

weather_hours = ["03", "06", "09", "12", "15", "18", "21", "00"]


@bot.message_handler(commands=["start"])
def greet(message):
    bot.send_message(
        message.chat.id,
        f"Привіт, {message.from_user.first_name}, я бот погоди. Можеш скористатися меню"
        f" для отримання погоди у твоєму місті.",
    )


def current_weather(message):
    # bot.delete_message(call.message.chat.id, call.message.id)
    locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
    response = get_weather_api.get_weather(message.text, "weather")
    markup = telebot.types.ReplyKeyboardRemove()
    if response:
        # print(response)
        temp = round(response["main"]["temp"])
        humidity = round(response["main"]["humidity"])
        wind_speed = round(response["wind"]["speed"])
        pressure = round(response["main"]["pressure"] * 0.75006)
        weather_emoji = get_emoji.getemoji(response["weather"][0]["id"])
        description = response["weather"][0]["description"]
        time_stamp = datetime.fromtimestamp(response["dt"]).strftime("%H:%M")
        bot.send_message(
            message.chat.id,
            f"Поточна погода у місті {message.text.title()}:\n\n{time_stamp} {weather_emoji} "
            f"{description.capitalize()}\nТемпература: {temp}°C\nВологість: {humidity}%"
            f"\nТиск: {pressure} mm\nВітер: {wind_speed} м/с",
            reply_markup=markup,
        )
        update_user_cities(message.from_user.username, message.text)
    else:
        bot.send_message(
            message.chat.id, f'Місто "{message.text}" не знайдено', reply_markup=markup
        )


def today_weather(message):
    locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
    response = get_weather_api.get_weather(message.text, "forecast")
    markup = telebot.types.ReplyKeyboardRemove()
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

        for time in response["list"]:
            hour = datetime.fromtimestamp(time["dt"]).strftime("%H")
            day = datetime.fromtimestamp(time["dt"]).strftime("%d")
            if (
                day == day_today
                and hour in weather_hours
                or (int(day) == int(day_today) + 1 and hour == "00")
            ):
                hours.append(hour)
                temp[hour] = round(time["main"]["temp"])
                humidity[hour] = round(time["main"]["humidity"])
                wind_speed[hour] = round(time["wind"]["speed"])
                pressure[hour] = round(time["main"]["pressure"] * 0.75006)
                weather_emoji[hour] = get_emoji.getemoji(time["weather"][0]["id"])
                description[hour] = time["weather"][0]["description"]
        for hour in hours:
            msg += (
                f"\n{hour}:00 {weather_emoji[hour]} {description[hour].capitalize()}\nТемпература: {temp[hour]}"
                f"°C\nВологість: {humidity[hour]}%\nТиск: {pressure[hour]} mm\nВітер: {wind_speed[hour]} м/с\n"
            )

        bot.send_message(message.chat.id, msg, reply_markup=markup)
        update_user_cities(message.from_user.username, message.text)

    else:
        bot.send_message(
            message.chat.id, f'Місто "{message.text}" не знайдено', reply_markup=markup
        )


def couple_days_weather(message, c_days):
    locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
    response = get_weather_api.get_weather(message.text, "forecast")
    markup = telebot.types.ReplyKeyboardRemove()
    if response:
        temp_day = {}
        temp_night = {}
        humidity = {}
        wind_speed = {}
        pressure = {}
        weather_emoji = {}
        description = {}
        days = []
        day_today = date.today().strftime("%d")
        if c_days == 3:
            msg = f"Погода на найближчі 3 дні у місті {message.text.title()}:\n"
        else:
            msg = f"Погода на найближчі 5 днів у місті {message.text.title()}:\n"

        for day in response["list"]:
            data_hour = datetime.fromtimestamp(day["dt"]).strftime("%H")
            data_day = datetime.fromtimestamp(day["dt"]).strftime("%d")
            if (
                    (int(day_today) < int(data_day) <= int(day_today) + c_days + 1)
                    and data_hour in weather_hours
                    or (int(data_day) == int(data_day) + + c_days + 1 and data_hour == "00")
            ):
                c_day = datetime.fromtimestamp(day["dt"]).strftime("%d %B, %A")
                if data_hour == "12":
                    days.append(c_day)
                    temp_day[c_day] = round(day["main"]["temp"])
                    humidity[c_day] = round(day["main"]["humidity"])
                    wind_speed[c_day] = round(day["wind"]["speed"])
                    pressure[c_day] = round(day["main"]["pressure"] * 0.75006)
                    description[c_day] = day["weather"][0]["description"]
                    weather_emoji[c_day] = get_emoji.getemoji(day["weather"][0]["id"])
                if data_hour == "00":
                    temp_night[c_day] = round(day["main"]["temp"])

            if c_days == 3 and len(days) == 3:
                break

        for day in days:
            msg += (
                f"\n{day.title()} {weather_emoji[day]} {description[day].capitalize()}\nТемпература вдень: "
                f"{temp_day[day]}°C\nТемпература вночі:  {temp_night[day]}°C\nВологість: {humidity[day]}%\nТиск: "
                f"{pressure[day]} mm\nВітер: {wind_speed[day]} м/с\n"
            )

        bot.send_message(message.chat.id, msg, reply_markup=markup)
        update_user_cities(message.from_user.username, message.text)

    else:
        bot.send_message(
            message.chat.id, f'Місто "{message.text}" не знайдено', reply_markup=markup
        )


@bot.message_handler(commands=["weather"])
def weather(message):
    # print(f'weather - {message.from_user.first_name} @{message.from_user.username} '
    #       f'{datetime.today().strftime("%Y-%m-%d %H:%M")}')
    msg_logs = (
        f'{datetime.today().strftime("%Y-%m-%d %H:%M")} '
        f"weather - {message.from_user.first_name} @{message.from_user.username}\n"
    )
    msg_date = datetime.today().strftime("%Y-%m-%d")
    weather_logs(msg_logs, msg_date)

    user_cities = get_user_cities(message.from_user.username)

    if user_cities is None:
        msg = bot.send_message(message.chat.id, f"Введіть назву міста:")
        bot.register_next_step_handler(msg, current_weather)
    else:
        cities = user_cities["cities"].split(", ")
        markup = telebot.types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True
        )
        for city in cities:
            markup.add(city)

        msg = bot.send_message(
            message.chat.id,
            f"Оберіть Ваше місто або введіть його назву:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, current_weather)


@bot.message_handler(commands=["todayweather"])
def weather(message):
    msg_logs = (
        f'{datetime.today().strftime("%Y-%m-%d %H:%M")} '
        f"todayweather - {message.from_user.first_name} @{message.from_user.username}\n"
    )
    msg_date = datetime.today().strftime("%Y-%m-%d")

    weather_logs(msg_logs, msg_date)

    user_cities = get_user_cities(message.from_user.username)

    if user_cities is None:
        msg = bot.send_message(message.chat.id, f"Введіть назву міста:")
        bot.register_next_step_handler(msg, today_weather)
    else:
        cities = user_cities["cities"].split(", ")
        markup = telebot.types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True
        )
        for city in cities:
            markup.add(city)

        msg = bot.send_message(
            message.chat.id,
            f"Оберіть Ваше місто або введіть його назву:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, today_weather)


@bot.message_handler(commands=["3daysweather"])
def weather(message):
    msg_logs = (
        f'{datetime.today().strftime("%Y-%m-%d %H:%M")} '
        f"3daysweather - {message.from_user.first_name} @{message.from_user.username}\n"
    )
    msg_date = datetime.today().strftime("%Y-%m-%d")

    weather_logs(msg_logs, msg_date)

    user_cities = get_user_cities(message.from_user.username)

    if user_cities is None:
        msg = bot.send_message(message.chat.id, f"Введіть назву міста:")
        bot.register_next_step_handler(msg, couple_days_weather, 3)
    else:
        cities = user_cities["cities"].split(", ")
        markup = telebot.types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True
        )
        for city in cities:
            markup.add(city)

        msg = bot.send_message(
            message.chat.id,
            f"Оберіть Ваше місто або введіть його назву:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, couple_days_weather, 3)


@bot.message_handler(commands=["5daysweather"])
def weather(message):
    msg_logs = (
        f'{datetime.today().strftime("%Y-%m-%d %H:%M")} '
        f"weekweather - {message.from_user.first_name} @{message.from_user.username}\n"
    )
    msg_date = datetime.today().strftime("%Y-%m-%d")

    weather_logs(msg_logs, msg_date)

    user_cities = get_user_cities(message.from_user.username)

    if user_cities is None:
        msg = bot.send_message(message.chat.id, f"Введіть назву міста:")
        bot.register_next_step_handler(msg, couple_days_weather, 5)
    else:
        cities = user_cities["cities"].split(", ")
        markup = telebot.types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True
        )
        for city in cities:
            markup.add(city)

        msg = bot.send_message(
            message.chat.id,
            f"Оберіть Ваше місто або введіть його назву:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, couple_days_weather, 7)


bot.polling()
