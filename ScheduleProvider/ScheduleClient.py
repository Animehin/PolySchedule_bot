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
                #print(schedule)
    except TypeError:
        return ""

def parseSchedule(response, date):
    soup = BeautifulSoup(str(response.text), 'lxml')
    try:
        for day in soup.ul:
            currentDate = convertToDateFormat(day.div.text)
            print(currentDate)
    except Exception:
        print("b")



getSchedule("3530904/70105", "26.09.2020")
