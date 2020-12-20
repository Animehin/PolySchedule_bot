import pymongo

global last_updated
clientSch = pymongo.MongoClient('localhost', 27017)
dbSch = clientSch['TgBot']
collectionSch = dbSch['TgBotSchedule']


def upd_schedule(pgroup, o_date, o_time, n_date, n_time, scheduledClass):
    collectionSch.update_one({"pgroup": pgroup, "date": o_date, "time": o_time, "scheduledClass": scheduledClass},
                             {"$set": {"date": n_date, "time": n_time}})


def add_schedule(pgroup, time, date, ClassName):
    collectionSch.insert_one({"pgroup": pgroup, "time": time, "date": date, "scheduledClass": ClassName})


def read_schedule(pgroup, date=None, time=None):
    global last_updated
    if last_updated is None:
        raise Exception("Расписание не обновлялось")
    if date and time is None:
        schVar = collectionSch.find_one({"pgroup": pgroup}, {"_id": 0})
    else:
        schVar = collectionSch.find_one({"date": date, "pgroup": pgroup}, {"_id": 0})
    if schVar is None:
        try:
            check_schedule_collection_availability()
        except Exception:
            return "Ошибка {}".format(Exception)
    last_updated = date
    return schVar


def check_schedule_collection_availability():
    collectionSchList = collectionSch.find()
    if collectionSchList is None:
        raise Exception("Расписания нет")
    return "Расписание есть!"
