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
    DUST = "Пыльная буря"
    SAND = "Песчаная буря"
    ASH = "Пепел"
    SQUALL = "Порывы"
    TORNADO = "Ураган"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str
    description: str


weather_type = {
    2: WeatherType.THUNDERSTORM,
    3: WeatherType.DRIZZLE,
    5: WeatherType.RAIN,
    6: WeatherType.SNOW,
    701: WeatherType.FOG,
    711: WeatherType.FOG,
    721: WeatherType.FOG,
    731: WeatherType.DUST,
    741: WeatherType.FOG,
    751: WeatherType.SAND,
    761: WeatherType.DUST,
    762: WeatherType.ASH,
    771: WeatherType.SQUALL,
    781: WeatherType.TORNADO,
    800: WeatherType.CLEAR,
    801: WeatherType.CLOUDS,
    802: WeatherType.CLOUDS,
    803: WeatherType.CLOUDS,
    804: WeatherType.CLOUDS,
    80: WeatherType.CLOUDS
}
