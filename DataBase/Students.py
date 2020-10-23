from pymongo import MongoClient

clientSt = MongoClient('localhost', 27017)
dbSt = clientSt['TgBot']
collectionSt = dbSt['TgBotStudents']


def bdStudents():
    lineList = [line.rstrip('\n') for line in open('../Students parsed.txt', encoding="utf8")]
    split = {}
    # fname = {}
    # name = {}
    # pgroup = {}
    i = 0
    while i < len(lineList):
        split[str(i)] = lineList[i].split(' ')
        post_id = collectionSt.insert_one(
            {"fname": split[str(i)][0], "name": split[str(i)][1], "pgroup": split[str(i)][2]}).inserted_id
        i += 1


# Заполнение бд студентами(фаил уже должен быть приведен к стандарту "фамилия имя номер_потока/номер_группы\n")

def changeGroupNum(fname, name, pgroupOld, pgroupNew):
    post_id = collectionSt.update_one({"fname": fname, "name": name, "pgroup": pgroupOld},
                                      {"$set": {"pgroup": pgroupNew}})


# Изменение номера группы(проводится поиск по фамилии, имени и номер_потока/номер_группы(старый), после чего старый номер группы меняется на новый)

def updateTGLogin(fname, name, pgroup, tglogin):
    post_id = collectionSt.update_one({"fname": fname, "name": name, "pgroup": pgroup},
                                      {"$set": {"tglogin": tglogin}})


def addSt(fname, name, pgroup):
    post_id = collectionSt.insert_one(
        {"fname": fname, "name": name, "pgroup": pgroup})
