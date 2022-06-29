""" This module contains data structures that help us to define our data more specifically"""

from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

Celsius: TypeAlias = int


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


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
    sunrise: datetime
    sunset: datetime
    city: str


weather_type = {
    1: WeatherType.THUNDERSTORM,
    3: WeatherType.DRIZZLE,
    5: WeatherType.RAIN,
    6: WeatherType.SNOW,
    7: WeatherType.FOG,
    800: WeatherType.CLEAR,
    80: WeatherType.CLOUDS
}
