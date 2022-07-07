""" Module provide functionality to save weather history """

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Protocol, TypedDict, Any

from custom_exceptions import CanNotWriteData
from data_structures import Weather
from weather_formatter import openweather_api_formatter

logger = logging.getLogger(__name__)

logger.debug('Hi from history.py ')


class HistoryRecord(TypedDict):
    date: str
    weather: str


class WeatherStorage(Protocol):
    """ Interface for any storage saving weather """

    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class JsonFileWeatherStorage:
    def __init__(self, jsonfile: Path):
        self._json_file = jsonfile
        self._init_storage()

    def save(self, weather: Weather) -> None:
        history_list = self._read_history()
        history_list.append(
            {
                'date': str(datetime.now()),
                'weather': openweather_api_formatter(weather)
            })
        self._write_history(history_list)

    def _init_storage(self) -> None:
        if not self._json_file.exists():
            try:
                self._json_file.write_text('[]')
            except IOError:
                raise CanNotWriteData

    def _read_history(self) -> Any:
        with open(self._json_file, mode='r', encoding='UTF-8') as file:
            return json.load(file)

    def _write_history(self, history: list[HistoryRecord]) -> None:
        try:
            with open(self._json_file, mode='w', encoding='UTF-8') as file:
                json.dump(history, file, ensure_ascii=False, indent=4)
        except IOError:
            raise CanNotWriteData


class PlainFileWeatherStorage:
    """ Storage weather in plain text file """

    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = openweather_api_formatter(weather)
        with open(self._file, mode='a') as file:
            file.write(f'{now}\n{formatted_weather}\n ')


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    """ Save weather in the storage """
    storage.save(weather)
