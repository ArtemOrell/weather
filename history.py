""" Module provide functionality to save weather history """

from datetime import datetime
from pathlib import Path
from typing import Protocol

from data_structures import Weather
from weather_formatter import openweather_api_formatter


class WeatherStorage(Protocol):
    """ Interface for any storage saving weather """

    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage:
    """ Storage weather in plain text file """

    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = openweather_api_formatter(weather)
        with open(self._file, mode='a') as file:
            file.write(f'{now}\n{formatted_weather}\n ')


def save_weather(weather: Weather, storage: WeatherStorage):
    """ Save weather in the storage """
    storage.save(weather)
