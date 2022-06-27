""" This module allows you to interact with remote services to obtain local computer's ip address, gps coordinates,
and weather relative to corresponding coordinates"""

import requests
from config import URL, API_IPSTACK_KEY, API_WEATHER_KEY
from custom_exceptions import CanNotHandleResponse
from data_structures import Coordinates
from misc import parse_coordinates


def get_gps_coordinates() -> Coordinates:
    """ Get gps coordinates from 'http://api.ipstack.com/' """

    coordinates = _get_ipstack_coordinates()
    return coordinates


def _get_ipstack_coordinates() -> Coordinates:
    ipstack_output = _get_ipstack_output()
    coordinates = parse_coordinates(ipstack_output)
    return coordinates


def _get_ipstack_output() -> bytes:
    url = URL.format(API_IPSTACK_KEY=API_IPSTACK_KEY)
    try:
        coordinates = requests.get(url=url).content
    except requests.exceptions.RequestException:
        raise CanNotHandleResponse
    return coordinates


def get_weather(coordinates: Coordinates):
    """ Sends request to https://openweathermap.org/
    API and returns weather relative to corresponding coordinates
    """
    pass


print(get_gps_coordinates())
