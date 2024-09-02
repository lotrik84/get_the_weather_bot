import os
from dotenv import load_dotenv
import requests

load_dotenv("./config/.env")

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
API_GEO_URL = "https://api.openweathermap.org/geo/1.0"
API_WEATHER_URL = "https://api.openweathermap.org/data/2.5"


def get_weather(city: str, uri: str):
    parameters = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ua"
    }
    response = requests.get(f"{API_GEO_URL}/direct", params=parameters)
    if response.status_code == 200:
        try:
            lat = response.json()[0]["lat"]
            lon = response.json()[0]["lon"]
            return get_full_weather(lat, lon, uri)
        except:
            return False
    else:
        return False


def get_full_weather(lat, lon, uri: str):
    parameters = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ua"
    }
    response = requests.get(f"{API_WEATHER_URL}/{uri}", params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        return False
