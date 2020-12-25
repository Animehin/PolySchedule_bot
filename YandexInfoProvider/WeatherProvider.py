import requests
import datetime
from YandexInfoProvider import Utils
from Config import Configuration
from dateutil.parser import parse
from bs4 import BeautifulSoup

lat = 60.007624
lon = 30.373195
xYandexAPIKey = Configuration.get_config_by_key('yandex-api-key')


def getYandexResponse():
    global xYandexAPIKey
    global lat, lon

    response = requests.get(url=f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}',
                            headers={"X-Yandex-API-Key": xYandexAPIKey})
    return response.json()


def getWeatherForDate(date):
    basicWeatherInformation = {}
    response = getYandexResponse()
    neededDate = date

    if neededDate == datetime.date.today():
        for key in response["fact"]:
            if key in ("temp", "feels_like", "wind_speed", "wind_gust"):
                basicWeatherInformation[key] = response["fact"][key]
            if key in ("condition", "wind_dir"):
                basicWeatherInformation[key] = Utils.convertFromEnToRu(response["fact"][key])
    else:
        forecasts = response["forecasts"]
        n = len(forecasts)
        for i in range(n):
            if forecasts[i]["date"] in str(date):
                for key in forecasts[i]["parts"]["morning"]:
                    if key in ("temp_avg", "wind_speed", "wind_gust"):
                        basicWeatherInformation[key] = forecasts[i]["parts"]["morning"][key]
                    if key in ("condition", "wind_dir"):
                        basicWeatherInformation[key] = Utils.convertFromEnToRu(forecasts[i]["parts"]["morning"][key])
    return basicWeatherInformation
