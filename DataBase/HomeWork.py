import re
from datetime import datetime

import pymongo
from dateutil.parser import parse

clientHW = pymongo.MongoClient('localhost', 27017)
dbHW = clientHW['TgBot']
collectionHW = dbHW['TgBotHW']


def add_home_work(pgroup, date, className, classType, homeWork, tgLogin):
    if (re.search('[0-9]', pgroup) is None) or (re.search('[а-яА-Я]', className) is None) or (
            re.search('[а-яА-Я]', homeWork) is None) or (re.search('[a-zA-Z]', tgLogin) is None):
        return False

    if collectionHW.find_one(
            {"pgroup": pgroup, "date": date, "className": className, "classType": classType,
             "tgLogin": tgLogin}) is None:
        try:
            collectionHW.insert_one({
                "pgroup": pgroup, "date": date, "className": className, "classType": classType,
                "homeWork": homeWork,
                "tgLogin": tgLogin
            })
        except pymongo.errors.WriteError:
            return False
    else:
        collectionHW.update_one(
            {"pgroup": pgroup, "date": date, "className": className, "classType": classType,
             "tgLogin": tgLogin},
            {"$set": {"homeWork": homeWork}})

    return True


def read_home_work(pgroup):
    today = datetime.today().date()
    hwlist = []
    res = collectionHW.find({"pgroup": pgroup}, {"_id": 0})
    if res is None:
        return hwlist
    for lesson in res:
        if parse(lesson["date"], dayfirst=True).date() >= today:
            hwlist.append(lesson)
        else:
            collectionHW.delete_one({"date": lesson["date"]})
    return hwlist
