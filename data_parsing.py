""" This module provides functions that parse IP coordinates from ipstack.com API
and parse the response from openweathermap.org API """

import json
import logging
from datetime import datetime
from typing import Literal, Any

from custom_exceptions import IpstackApiServiceError, CanNotGetCoordinates, OpenWeatherApiServiceError, \
    CanNotGetOpenWeatherData
from data_structures import Coordinates, Weather, weather_type, Celsius, WeatherType
from weather_app_config import USE_ROUNDED_COORD

logger = logging.getLogger(__name__)

logger.debug('Hi from data_parsing.py')


def parse_coordinates(data: bytes) -> Coordinates:
    """ Get coordinates from json response"""
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        raise IpstackApiServiceError
    coordinates = _parse_coord(data_dict)
    return _round_coordinates(coordinates)


def _parse_coord(data: dict[str, slice]) -> Coordinates:
    """ Get latitude and longitude """
    try:
        latitude, longitude = str(data.get('latitude')), str(data.get('longitude'))
    except KeyError:
        raise CanNotGetCoordinates
    return _parse_float_coordinates(latitude, longitude)


def _parse_float_coordinates(latitude: str, longitude: str) -> Coordinates:
    """string to float"""
    return Coordinates(*map(lambda c: float(c), [latitude, longitude]))


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    """ Rounded coordinates to one digit after the dot if config.USE_ROUNDED_COORD = True"""
    if not USE_ROUNDED_COORD:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude]))


def parse_openweather_response(open_weather_response: bytes) -> Weather:
    try:
        openweather_dict = json.loads(open_weather_response)
    except json.JSONDecodeError:
        raise OpenWeatherApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        city=_parse_city(openweather_dict),
        description=_parse_weather_description(openweather_dict, 'description')
    )


def _parse_temperature(open_weather_dict: dict[str, Any]) -> Celsius:
    """ Ger temperature """

    try:
        return round(open_weather_dict['main']['temp'])
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_weather_type(open_weather_dict: dict[str, Any]) -> WeatherType:
    """ Get weather type"""

    try:
        _type_id = open_weather_dict['weather'][0]['id']
        weather_type_id = _match_type_id(_type_id)
    except (KeyError, IndexError, TypeError):
        raise CanNotGetOpenWeatherData
    try:
        return weather_type[weather_type_id]
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_sun_time(open_weather_dict: dict[str, Any], time: Literal['sunrise'] | Literal['sunset']) -> datetime:
    """ Get sunrise and sunset time """
    try:
        return datetime.fromtimestamp(open_weather_dict['sys'][time])
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_city(open_weather_dict: dict[str, Any]) -> Any:
    """ Get city """

    try:
        return open_weather_dict['name']
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_weather_description(open_weather_dict: dict[str, Any], description: Literal['description']) -> str | Any:
    """ Get weather description """
    try:
        weather_description = open_weather_dict['weather'][0][description]
        return weather_description
    except KeyError:
        raise CanNotGetOpenWeatherData


def _match_type_id(type_id: int) -> int:
    match type_id:
        case type_id if 200 <= type_id < 233:
            type_id = 2
        case type_id if 300 <= type_id < 321:
            type_id = 3
        case type_id if 500 <= type_id < 532:
            type_id = 5
        case type_id if 600 <= type_id < 623:
            type_id = 6
    return type_id
