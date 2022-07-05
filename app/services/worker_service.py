import logging
from decimal import Decimal

from aiohttp import ClientSession
from arq.connections import RedisSettings

from app import settings
from app.db.db_client import PgClient
from app.main import app
from app.models.cities import City, DBCity, APICity
from app.services.db_service import  ServiceWeather


async def weather_task(context, city: City):
    """ Task for fetch weather and check difference"""
    current_weather = await fetch_current_weather(context, city)
    last_weather_record = await ServiceWeather.fetch_weather_by_city(city_name=city.city_name)

    if last_weather_record:
        check_for_difference(current_weather, last_weather_record, city)


async def fetch_current_weather(context, city: City):
    """Fetch weather for given city."""

    params = {'appid': settings.OPEN_WEATHER_MAP_API_KEY, 'q': city.city_name, 'units': 'metric'}
    session: ClientSession = context['session']

    async with session.get(url=settings.OPEN_WEATHER_MAP_URL, params=params) as response:
        response.raise_for_status()

        response_data = await response.json()
        api_city_object = APICity.from_response(response_data)

        await save_weather_record(api_city=api_city_object)
    return api_city_object


def check_for_difference(api_city: APICity, db_record: DBCity, city: City) -> None:
    """ Check for difference"""
    temperature_diff = Decimal(
        abs(100 - (Decimal(api_city.temperature) / Decimal(db_record.temperature) * 100)).quantize(Decimal('0'))
    )

    if temperature_diff == city.threshold:
        logging.warning(f'Temperature for city "{city.city_name}" has been changed!')


async def save_weather_record(api_city: APICity):
    """Save current weather to DB."""

    await ServiceWeather.insert_record(
        city_name=api_city.city_name,
        temperature=api_city.temperature,
        wind_speed=api_city.wind_speed
    )


async def startup(context):
    """Worker startup function."""

    context['session'] = ClientSession()


async def shutdown(context):
    """Worker shutdown function."""

    await context['session'].close()


class WorkerSettings:
    """Worker settings."""

    functions = [weather_task]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
