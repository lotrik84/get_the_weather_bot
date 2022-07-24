import os
from dotenv import load_dotenv
import requests

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
api = "https://api.openweathermap.org/data/2.5"


def get_weather(city):
    parameters = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ua"
    }
    response = requests.get(f"{api}/find", params=parameters)
    if response.status_code == 200:
        try:
            lat = response.json()["list"][0]["coord"]["lat"]
            lon = response.json()["list"][0]["coord"]["lon"]
            return get_full_weather(lat, lon)
        except:
            return False
    else:
        return False


def get_full_weather(lat, lon):
    parameters = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ua"
    }
    response = requests.get(f"{api}/onecall", params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        return False
