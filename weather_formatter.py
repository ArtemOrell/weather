""" Here we format all the data receiving from https://openweathermap.org/ """


from data_structures import Weather


def openweather_api_formatter(weather: Weather) -> str:
    """ """
    return (f"{weather.city}, температура {weather.temperature}°C, "
            f"{weather.weather_type}\n"
            f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
            f"Закат: {weather.sunset.strftime('%H:%M')}\n")
