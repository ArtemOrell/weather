""" This module allows you to interact with remote services to obtain local computer's ip adderss, gps coordinates,
and weather relative to corresponding coordinates"""

import subprocess
import requests
from config import URL, ENCODING, HEADERS
from custom_exceptions import CanNotGetLocalIp
from data_structures import Coordinates


def _fetch_public_ip() -> str:
    """ Function gets public ip of the local computer via 'curl ifconfig.me' """

    process = subprocess.Popen(['curl', 'ifconfig.me'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CanNotGetLocalIp
    return out.decode(ENCODING)


def get_gps_coordinates() -> Coordinates:
    """ Get gps coordinates from 'https://ipstack.com/' """

    public_ip = _fetch_public_ip()
    coordinates = requests.get(url=URL.format(ip=public_ip), headers=HEADERS).json()
    latitude, longitude = coordinates.get('latitude'), coordinates.get('longitude')
    return Coordinates(latitude=latitude, longitude=longitude)


def get_weather(coordinates: Coordinates):
    """ Sends request to https://openweathermap.org/
    API and returns weather relative to corresponding coordinates
    """
    pass
