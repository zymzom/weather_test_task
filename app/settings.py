import json
import logging
import os

from dotenv import load_dotenv

from app.models.cities import City

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

OPEN_WEATHER_MAP_API_KEY = os.getenv('OPEN_WEATHER_MAP_API_KEY')
OPEN_WEATHER_MAP_URL = os.getenv('OPEN_WEATHER_MAP_URL')

CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'cities.json')

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

CITY_LIST = []
try:
    with open(CONFIG_FILE_PATH) as file:
        CITY_LIST = [City.from_dict(city) for city in json.load(file).get('cities')]
except Exception as exp:
    logging.error(f"Error while parsing cities: {exp}")

