from ScheduleUtil import convertDate as convertDate, convertToDateFormat as convertToDateFormat
import requests
from bs4 import BeautifulSoup

scheduleUrl = "https://ruz.spbstu.ru"


def getSchedule(groupNumber, date):
    searchUrl = scheduleUrl + "/search/groups?q=" + groupNumber.replace('/', '%2F')
    startDate = convertDate(date)

    response = requests.get(url=searchUrl)
    soup = BeautifulSoup(str(response.text), 'lxml')
    try:
        for group in soup.ul:
            if group.text == groupNumber:
                groupUrl = scheduleUrl + group.a.attrs['href']
                response = requests.get(url=groupUrl)
                schedule = parseSchedule(response, date)
    except TypeError:
        return ""


def parseSchedule(response, date):
    soup = BeautifulSoup(str(response.text), 'lxml')
    try:
        schedule = {}
        for day in soup.findAll("li", "schedule__day"):
            lessions = {}
            currentDate = convertToDateFormat(day.find("div", "schedule__date").text)
            schedule[currentDate] = []
            for lesson in day.findAll("li", "lesson"):
                dataReactId = lesson.find("span", "lesson__time").attrs['data-reactid']
                lessonTime = lesson.find("span", "lesson__time").text
                lessonName = lesson.find("span", {"data-reactid":dataReactId[:-1]+str(2)}).text
                temp = [lessonTime, lessonName] #{'10:00-11:40', 'Нейронные сети'}
                schedule[currentDate].append(temp)
        return schedule
    except Exception:
        print("Something went wrong")


getSchedule("3530904/70105", "26.09.2020")
