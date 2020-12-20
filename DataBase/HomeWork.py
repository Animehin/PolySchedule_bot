import re
from datetime import datetime

import pymongo

clientHW = pymongo.MongoClient('localhost', 27017)
dbHW = clientHW['TgBot']
collectionHW = dbHW['TgBotHW']


def upd_home_work(pgroup, date, className, homeWork):
    collectionHW.update_one({"pgroup": pgroup, "date": date, "className": className},
                            {"$set": {"homeWork": homeWork}})


def add_home_work(pgroup, date, time, className, homeWork, tgLogin):
    if (re.search('[0-9]', pgroup) is None) or (re.search('[а-яА-Я]', className) is None) or (
            re.search('[а-яА-Я]', homeWork) is None) or (re.search('[a-zA-Z]', tgLogin) is None):
        return False

    if collectionHW.find_one(
            {"pgroup": pgroup, "date": date, "className": className, "tgLogin": tgLogin}) is None:
        try:
            collectionHW.insert_one({
                "pgroup": pgroup, "date": date, "time": time, "className": className, "homeWork": homeWork,
                "tgLogin": tgLogin
            })
        except pymongo.errors.WriteError:
            return False
    else:
        upd_home_work(pgroup, date, className, homeWork)

    return True


def read_home_work(pgroup):
    today = datetime.date.today().format("%d.%m.%Y")
    hwlist = []
    res = collectionHW.find({"pgroup": pgroup}, {"_id": 0})
    if res is None:
        return hwlist
    for lesson in res:
        if lesson["date"].format("%d.%m.%Y") >= today:
            hwlist.append(lesson)
        else:
            collectionHW.delete_one({"date": lesson["date"]})
    return hwlist
