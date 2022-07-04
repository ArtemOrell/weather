""" Module contains some config variables. """
import os

API_IPSTACK_KEY = os.getenv('API_IPSTACK_KEY')
API_WEATHER_KEY = os.getenv('API_WEATHER_KEY')

URL = 'http://api.ipstack.com/check?access_key={API_IPSTACK_KEY}'

USE_ROUNDED_COORD = True
assert API_WEATHER_KEY is not None
OPENWEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat={latitude}&lon={longitude}&"
        "appid=" + API_WEATHER_KEY + "&lang=ru&"
                                     "units=metric"
)
