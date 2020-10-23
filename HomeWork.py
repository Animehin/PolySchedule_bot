from pymongo import MongoClient

clientHW = MongoClient('localhost', 27017)
dbHW = clientHW['TgBot']
collectionHW = dbHW['TgBotHW']


def updHomeWork(pgroup, date, className, homeWork):
    post_id = collectionHW.update_one({"pgroup": pgroup, "date": date, "className": className},
                                      {"$set": {"homeWork": homeWork}})


def addHomeWork(pgroup, date, className, homeWork):
    post_id = collectionHW.insert_one({
        "pgroup": pgroup, "date": date, "className": className, "homeWork": homeWork})
