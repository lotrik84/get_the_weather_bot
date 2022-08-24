import os
from dotenv import load_dotenv
import pymongo

load_dotenv("./config/.env")

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWD = os.getenv('MONGO_PASSWD')

client = pymongo.MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWD}@mongodb:27017/")
db = client["weather_users"]
collection = db["users_cities"]


def get_user_cities(user):
    return collection.find_one({"user": f"{user}"})


def update_user_cities(user, city):
    if collection.find_one({"user": f"{user}"}) is None:
        item = {"user": f"{user}", "cities": f"{city}"}
        collection.insert_one(item)
    else:
        cities = collection.find_one({"user": f"{user}"})
        list_cities = cities["cities"].split()
        if city not in list_cities:
            if len(list_cities) >= 4:
                list_cities.pop(0)
                list_cities.append(city)
            else:
                list_cities.append(city)

            filter = {"user": f"{user}"}
            cities = ' '.join(list_cities)
            item = { "$set": {"cities": f"{cities}"}}
            collection.update_one(filter, item)
