""" Module contains custom exceptions that helps handle errors. """


class IpstackApiServiceError(Exception):
    """ Can not handle response from 'http://api.ipstack.com/'"""
    pass


class CanNotGetCoordinates(Exception):
    """ Raise in case if response does not contain latitude and longitude coordinates"""
    pass


class OpenWeatherApiServiceError(Exception):
    """ Raise in case if some errors occur while interact with openweathermap.org """
    pass


class CanNotGetOpenWeatherData(Exception):
    """ Raise in case if we can not get some data from OpenWeather API response"""
    pass


class CanNotWriteData(Exception):
    """ Raise in case if we cannot write data to json file """
    pass
