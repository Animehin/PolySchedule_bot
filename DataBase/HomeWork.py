import re

import pymongo

clientHW = pymongo.MongoClient('localhost', 27017)
dbHW = clientHW['TgBot']
collectionHW = dbHW['TgBotHW']


def updHomeWork(pgroup, date, className, homeWork):
    collectionHW.update_one({"pgroup": pgroup, "date": date, "className": className},
                            {"$set": {"homeWork": homeWork}})


def addHomeWork(pgroup, date, className, homeWork, telegLogin):
    if (re.search('[0-9]', pgroup) == None) or (re.search('[а-яА-Я]', className) == None) or (
            re.search('[а-яА-Я]', homeWork) == None) or (re.search('[a-zA-Z]', telegLogin) == None):
        return False

    if collectionHW.find_one(
            {"pgroup": pgroup, "date": date, "className": className, "telegLogin": telegLogin}) == None:
        try:
            collectionHW.insert_one({
                "pgroup": pgroup, "date": date, "className": className, "homeWork": homeWork, "telegLogin": telegLogin
            })
        except pymongo.errors.WriteError:
            return False
    else:
        updHomeWork(pgroup, date, className, homeWork)

    return True


def readHomeWork(pgroup, date, className):
    if collectionHW.find_one({"pgroup": pgroup, "date": date, "className": className, }) == None:
        return False
    else:
        return collectionHW.find_one({
            "pgroup": pgroup, "date": date, "className": className,
        })
