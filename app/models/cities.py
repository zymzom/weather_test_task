from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class City:
    city_id: int
    city_name: str
    frequency: int
    threshold: int


@dataclass_json
@dataclass(frozen=True)
class DBCity:
    id: int
    time: datetime
    city_name: str
    temperature: float
    wind_speed: float


@dataclass_json
@dataclass(frozen=True)
class APICity:
    city_name: str
    temperature: float
    wind_speed: float

    @classmethod
    def from_response(cls, response):
        """ Parse response to city object"""
        return APICity(
            city_name=response['name'],
            temperature=response['main']['temp'],
            wind_speed=response['wind']['speed']
        )



