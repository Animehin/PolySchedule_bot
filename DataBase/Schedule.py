from pymongo import MongoClient

clientSch = MongoClient('localhost', 27017)
dbSch = clientSch['TgBot']
collectionSch = dbSch['TgBotSchedule']


def updSchedule(pgroup, date, updClassScheduledName):
    post_id = collectionSch.update_one({"pgroup": pgroup, "date": date},
                                       {"$set": {"scheduledClass": updClassScheduledName}})


def addSchedule(pgroup, date, ClassName):
    post_id = collectionSch.insert_one({"pgroup": pgroup, "date": date, "scheduledClass": ClassName})
