import pymongo

clientSch = pymongo.MongoClient('localhost', 27017)
dbSch = clientSch['TgBot']
collectionSch = dbSch['TgBotSchedule']


def upd_schedule(pgroup, o_date, o_time, n_date, n_time, scheduledClass):
    collectionSch.update_one({"pgroup": pgroup, "date": o_date, "time": o_time, "scheduledClass": scheduledClass},
                             {"$set": {"date": n_date, "time": n_time}})


def add_schedule(pgroup, date, ClassName):
    collectionSch.insert_one({"pgroup": pgroup, "date": date, "scheduledClass": ClassName})


def read_schedule(date):
    schVar = collectionSch.find_one({"date": date}, {"_id": 0})
    if schVar == None:
        try:
            check_schedule_collection_availability()
        except Exception:
            return None
    return schVar


def check_schedule_collection_availability():
    collectionSchList = collectionSch.find()
    if collectionSchList == None:
        raise Exception("Collection is empty")
