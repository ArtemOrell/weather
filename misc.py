""" This module provides some auxiliary functions"""

from custom_exceptions import CanNotHandleResponse, CanNotGetCoordinates
from data_structures import Coordinates
from config import USE_ROUNDED_COORDS
import json


def parse_coordinates(data: bytes) -> Coordinates:
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        raise CanNotHandleResponse
    coordinates = _parse_coord(data)
    return _round_coordinates(coordinates)


def _parse_coord(data: dict) -> Coordinates:
    try:
        latitude, longitude = data.get('latitude'), data.get('longitude')
    except KeyError:
        raise CanNotGetCoordinates
    return _parse_float_coordinates(latitude, longitude)


def _parse_float_coordinates(latitude: str, longitude: str) -> Coordinates:
    return Coordinates(*map(lambda c: float(c), [latitude, longitude]))


def _round_coordinates(coordinates: Coordinates):
    if not USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude]))
