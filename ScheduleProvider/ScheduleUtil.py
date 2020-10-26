import datetime
import re


def nameToNumber(month):
    return {
        'янв': 1,
        'фев': 2,
        'март': 3,
        'апр': 4,
        'май': 5,
        'июнь': 6,
        'июль': 7,
        'авг': 8,
        'сент': 9,
        'окт': 10,
        'нояб': 10,
        'дек': 10
    }[month]


def convertDate(date):
    splittedDateString = [int(x) for x in date.split(".")]
    return datetime.date(
        int(splittedDateString[2]),
        int(splittedDateString[1]),
        int(splittedDateString[0])
    )


def convertToDateFormat(date):
    pattern = r"(\d+)\s([\u0400-\u0500]+)\..+"
    match = re.match(pattern, date)
    return match.group(1) + "." + str(nameToNumber(match.group(2))) + "." + str(datetime.datetime.now().year)
