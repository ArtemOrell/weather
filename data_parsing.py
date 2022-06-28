""" This module provides functions that parse gps coordinates from ipstack.com
and parse response from openweathermap.org"""

from custom_exceptions import IpstackApiServiceError, CanNotGetCoordinates, OpenWeatherApiServiceError
from data_structures import Coordinates, Weather
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


def _parse_temperature():
    pass


def _parse_weather_type():
    pass


def _parse_sun_time():
    pass


def _parse_city():
    pass
