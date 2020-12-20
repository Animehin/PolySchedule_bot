import datetime

import pymongo

from PolySchedule_bot.ScheduleProvider import ScheduleClient

global last_updated
clientSch = pymongo.MongoClient('localhost', 27017)
dbSch = clientSch['TgBot']
collectionSch = dbSch['TgBotSchedule']
last_updated = {}


def upd_schedule(pgroup):
    global last_updated

    today = datetime.date.today().strftime("%d.%m.%Y")
    schVar = ScheduleClient.getSchedule(pgroup, today)
    if schVar is "":
        return "Фейлед ту апдэйте"
    collectionSch.delete_many({"pgroup": pgroup})

    for day in schVar:
        for lesson in schVar[day]:
            collectionSch.insert_one(
                {"pgroup": pgroup, "date": day, "time": lesson["time"], "scheduledClass": lesson["scheduledClass"],
                 "classType": lesson["classType"]})
    last_updated[pgroup] = today
    return "Апдейт кумплитэд"


def read_schedule(pgroup, date=None):
    global last_updated

    if (last_updated is None) or (last_updated is not datetime.date.today().strftime("%d.%m.%Y")):
        upd_schedule(pgroup)

    if date is None:
        schVar = collectionSch.find_one({"pgroup": pgroup}, {"_id": 0})
    else:
        schVar = collectionSch.find_one({"date": date, "pgroup": pgroup}, {"_id": 0})
    if schVar is None:
        try:
            check_schedule_collection_availability()
        except Exception:
            return "Ошибка {}".format(Exception)
    return schVar


def check_schedule_collection_availability():
    collectionSchList = collectionSch.find()
    if collectionSchList is None:
        raise Exception("Расписания нет")
    return "Расписание есть!"
