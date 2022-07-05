import datetime
from typing import Optional

from app.db.queries import INSERT_CITY, SELECT_CITY
from app.main import app
from app.models.cities import DBCity


class ServiceWeather:
    """Database service class for weather."""

    @staticmethod
    async def insert_record(city_name: str, temperature: float, wind_speed: float):
        """Insert record into open weathers table."""

        result = await app.ctx.db.execute(INSERT_CITY, city_name, temperature, wind_speed, datetime.datetime.now())
        return result

    @staticmethod
    async def fetch_weather_by_city(city_name: str) -> Optional[DBCity]:
        """Return weather by city."""

        result = await app.ctx.db.fetch_row(SELECT_CITY, city_name)
        return DBCity.from_dict(result) if result else None


