""" This module allows you to interact with remote services to obtain local computer's IP address,
and weather relative to corresponding IP """

import requests
from weather_app_config import URL, API_IPSTACK_KEY, OPENWEATHER_URL
from custom_exceptions import IpstackApiServiceError, OpenWeatherApiServiceError
from data_structures import Coordinates, Weather
from data_parsing import parse_coordinates, parse_openweather_response


def get_gps_coordinates() -> Coordinates:
    """ Get gps coordinates from 'http://api.ipstack.com/' """

    coordinates = _get_ipstack_coordinates()
    return coordinates


def _get_ipstack_coordinates() -> Coordinates:
    """ Handle response from 'http://api.ipstack.com/' """
    ipstack_output = _get_ipstack_output()
    coordinates = parse_coordinates(ipstack_output)
    return coordinates


def _get_ipstack_output() -> bytes:
    """ Get response form the 'http://api.ipstack.com/' """
    url = URL.format(API_IPSTACK_KEY=API_IPSTACK_KEY)
    try:
        coordinates = requests.get(url=url).content
    except requests.exceptions.RequestException:
        raise IpstackApiServiceError
    return coordinates


def get_weather(coordinates: Coordinates) -> Weather:
    """ Sends request to https://openweathermap.org/
    API and returns weather relative to corresponding coordinates
    """
    open_weather_response = _get_openweather_response(coordinates.latitude, coordinates.longitude)
    weather = parse_openweather_response(open_weather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> bytes:
    """ Get response form OpenWeather API """

    url = OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        response = requests.get(url).content
    except requests.exceptions.RequestException:
        raise OpenWeatherApiServiceError
    return response
