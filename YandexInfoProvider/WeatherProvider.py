import requests
import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup

lat = 60.007624
lon = 30.373195
xYandexAPIKey = ""


def getYandexResponse():
    global xYandexAPIKey
    global lat, lon

    response = requests.get(url=f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}',
                            headers={"X-Yandex-API-Key": xYandexAPIKey})
    return response.json()


def getWeatherForDate(date):
    basicWeatherInformation = {}
    response = getYandexResponse()
    neededDate = parse(date, dayfirst=True)

    if neededDate == datetime.date.today():
        for key in response["fact"]:
            if key in ("temp", "condition", "wind_speed", "wind_gust", "wind_dir"):
                basicWeatherInformation[key] = response["fact"][key]
    else:
        forecasts = response["forecasts"]
        n = len(forecasts)
        for i in range(n):
            if forecasts[i]["date"] in str(neededDate):
                for key in forecasts[i]["parts"]["morning"]:
                    if key in ("temp_avg", "condition", "wind_speed", "wind_gust", "wind_dir"):
                        basicWeatherInformation[key] = forecasts[i]["parts"]["morning"][key]
    return basicWeatherInformation
