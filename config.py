""" Module contains some config variables. """
import os

API_IPSTACK_KEY = os.getenv('API_IPSTACK_KEY')
API_WEATHER_KEY = os.getenv('API_WEATHER_KEY')

URL = 'http://api.ipstack.com/check?access_key={API_IPSTACK_KEY}'

USE_ROUNDED_COORDS = True
