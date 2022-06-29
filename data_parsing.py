""" This module provides functions that parse gps coordinates from ipstack.com API
and parse the response from openweathermap.org API """


from datetime import datetime
from typing import Literal

from custom_exceptions import IpstackApiServiceError, CanNotGetCoordinates, OpenWeatherApiServiceError, \
    CanNotGetOpenWeatherData
from data_structures import Coordinates, Weather, weather_type, Celsius, WeatherType
from weather_app_config import USE_ROUNDED_COORDS
import json


def parse_coordinates(data: bytes) -> Coordinates:
    """ Get coordinates from json response"""
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        raise IpstackApiServiceError
    coordinates = _parse_coord(data)
    return _round_coordinates(coordinates)


def _parse_coord(data: dict) -> Coordinates:
    """ Get latitude and longitude """
    try:
        latitude, longitude = data.get('latitude'), data.get('longitude')
    except KeyError:
        raise CanNotGetCoordinates
    return _parse_float_coordinates(latitude, longitude)


def _parse_float_coordinates(latitude: str, longitude: str) -> Coordinates:
    """string to float"""
    return Coordinates(*map(lambda c: float(c), [latitude, longitude]))


def _round_coordinates(coordinates: Coordinates):
    """ Rounded coordinates to one digit after the dot if config.USE_ROUNDED_COORDS = True"""
    if not USE_ROUNDED_COORDS:
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
        city=_parse_city(openweather_dict)
    )


def _parse_temperature(open_weather_dict: dict[str, str | dict | list]) -> Celsius:
    """ Ger temperature """

    try:
        return round(open_weather_dict['main']['temp'])
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_weather_type(open_weather_dict: dict[str, slice | dict | list]) -> WeatherType:
    """ Get weather type"""

    try:
        weather_type_id = open_weather_dict['weather'][0]['id']
    except (KeyError, IndexError, TypeError):
        raise CanNotGetOpenWeatherData
    try:
        return weather_type[weather_type_id]
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_sun_time(open_weather_dict: dict, time: Literal['sunrise'] | Literal['sunset']) -> datetime:
    """ Get sunrise and sunset time """
    try:
        return datetime.fromtimestamp(open_weather_dict['sys'][time])
    except KeyError:
        raise CanNotGetOpenWeatherData


def _parse_city(open_weather_dict: dict) -> str:
    """ Get city """

    try:
        return open_weather_dict['name']
    except KeyError:
        raise CanNotGetOpenWeatherData
