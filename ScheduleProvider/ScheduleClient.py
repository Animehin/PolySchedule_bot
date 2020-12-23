import re
from datetime import timedelta
import datetime

import requests
from ScheduleProvider import ScheduleUtil
from bs4 import BeautifulSoup
from dateutil.parser import parse

scheduleUrl = "https://ruz.spbstu.ru"


# getSchedule("3530904/70105", "25.12.2020") - call example
# If anything goes wrong, returns empty string ("")

def getSchedule(groupNumber, date):
    searchUrl = scheduleUrl + "/search/groups?q=" + groupNumber.replace('/', '%2F')

    response = requests.get(url=searchUrl)
    soup = BeautifulSoup(str(response.text), 'lxml')
    try:
        for group in soup.ul:
            if group.text == groupNumber:
                groupUrl = scheduleUrl + group.a.attrs['href']
                response = requests.get(url=groupUrl)
                schedule = parseSchedule(response, date)
                return schedule
    except TypeError:
        return ""


def parseSchedule(response, date):
    startDate = parse(date, dayfirst=True)
    finishDate = startDate + timedelta(14)

    soup = BeautifulSoup(str(response.text), 'lxml')
    try:
        schedule = {}
        for day in soup.findAll("li", "schedule__day"):
            currentDate = ScheduleUtil.convertToDateFormat(day.find("div", "schedule__date").text)
            convertedCurrentDate = parse(currentDate, dayfirst=True)
            if convertedCurrentDate < startDate: continue
            if convertedCurrentDate > finishDate: break
            schedule[currentDate] = []  # {'time':'10:00-11:40', 'scheduledClass':'Нейронные сети', 'classType':'Практика'}
            for lesson in day.findAll("li", "lesson"):
                dataReactId = lesson.find("span", "lesson__time").attrs['data-reactid']
                lessonTime = lesson.find("span", "lesson__time").text
                lessonType = lesson.find("div", "lesson__type").text
                lessonName = lesson.find("span", {"data-reactid": dataReactId[:-1] + str(2)}).text
                schedule[currentDate].append({'time': lessonTime, 'scheduledClass': lessonName, 'classType': lessonType})
        nextPageUrl = soup.find("a", "switcher__link", "text", "Следующая неделя").attrs['href']
        nextPageDate = parse(re.match(".+date=(.+)", nextPageUrl).group(1))
        if nextPageDate < finishDate:
            newResponse = requests.get(url=scheduleUrl + nextPageUrl)
            schedule.update(parseSchedule(newResponse, date))
        return schedule
    except Exception:
        return ""

