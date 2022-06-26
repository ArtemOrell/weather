""" This module contains data structures that helps to define our data more specifically"""

import datetime
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

Celsius: TypeAlias = int


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime.datetime
    sunset: datetime.datetime
    city: str
