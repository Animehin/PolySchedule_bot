import pymongo

clientSt = pymongo.MongoClient('localhost', 27017)
dbSt = clientSt['TgBot']
collectionSt = dbSt['TgBotStudents']


def bd_students():
    lineList = [line.rstrip('\n') for line in open('../Students parsed.txt', encoding="utf8")]
    split = {}
    i = 0
    while i < len(lineList):
        split[str(i)] = lineList[i].split(' ')
        var = collectionSt.insert_one(
            {"fname": split[str(i)][0], "name": split[str(i)][1], "pgroup": split[str(i)][2]}).inserted_id
        i += 1


# Заполнение бд студентами(фаил уже должен быть приведен к стандарту "фамилия имя номер_потока/номер_группы\n")

def change_group_num(fname, name, pgroupOld, pgroupNew):
    if collectionSt.find_one({"fname": fname, "name": name, "pgroup": pgroupOld}) == None:
        return ("This user is not exist")
    else:
        collectionSt.update_one({"fname": fname, "name": name, "pgroup": pgroupOld},
                                {"$set": {"pgroup": pgroupNew}})
        return "Group number updated successfully"


# Изменение номера группы(проводится поиск по фамилии, имени и номер_потока/номер_группы(старый), после чего старый номер группы меняется на новый)

def update_tg_login(fname, name, pgroup, tglogin):
    if collectionSt.find_one({"fname": fname, "name": name, "pgroup": pgroup}) == None:
        add_student(fname, name, pgroup)
        update_tg_login(fname, name, pgroup, tglogin)
    else:
        collectionSt.update_one({"fname": fname, "name": name, "pgroup": pgroup},
                                {"$set": {"tglogin": tglogin}})
        return "Telegram login updated successfully"


def get_group_num(tglogin):
    if collectionSt.find_one({"tglogin": tglogin}, {"_id": 0, "pgroup": 1}) == None:
        return ("This user is not exist")
    else:
        return collectionSt.find_one({"tglogin": tglogin}, {"_id": 0, "pgroup": 1})


def add_student(fname, name, pgroup):
    collectionSt.insert_one(
        {"fname": fname, "name": name, "pgroup": pgroup})
