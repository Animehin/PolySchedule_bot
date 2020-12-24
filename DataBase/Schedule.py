from datetime import datetime

import pymongo

from ScheduleProvider import ScheduleClient

global last_updated
clientSch = pymongo.MongoClient('localhost', 27017)
dbSch = clientSch['TgBot']
collectionSch = dbSch['TgBotSchedule']
last_updated = {}


def upd_schedule(pgroup):
    global last_updated

    today = datetime.today().strftime("%d.%m.%Y")
    schVar = ScheduleClient.getSchedule(pgroup, today)
    if schVar == "":
        return "Не удалось получить расписание"
    collectionSch.delete_many({"pgroup": pgroup})

    for day in schVar:
        for lesson in schVar[day]:
            collectionSch.insert_one(
                {"pgroup": pgroup, "date": day, "time": lesson["time"], "scheduledClass": lesson["scheduledClass"],
                 "classType": lesson["classType"]})
    last_updated[pgroup] = today
    return "Обновление расписания прошло успешно"


def read_schedule(pgroup, date=None):
    global last_updated

    if (pgroup not in last_updated) or (last_updated[pgroup] is not datetime.today()):
        upd_schedule(pgroup)
        last_updated[pgroup] = datetime.today()
    return get_schedule_from_database(pgroup, date)


def get_schedule_from_database(pgroup, date):
    if date is None:
        schVar = collectionSch.find({"pgroup": pgroup}, {"_id": 0})
    else:
        schVar = collectionSch.find({"date": date, "pgroup": pgroup}, {"_id": 0})
    if schVar is None:
        return []
    return schVar
