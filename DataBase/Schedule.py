import pymongo

clientSch = pymongo.MongoClient('localhost', 27017)
dbSch = clientSch['TgBot']
collectionSch = dbSch['TgBotSchedule']


def updSchedule(pgroup, date, updClassScheduledName):
    collectionSch.update_one({"pgroup": pgroup, "date": date},
                             {"$set": {"scheduledClass": updClassScheduledName}})


def addSchedule(pgroup, date, ClassName):
    collectionSch.insert_one({"pgroup": pgroup, "date": date, "scheduledClass": ClassName})
