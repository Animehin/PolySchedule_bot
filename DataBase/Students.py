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

def change_group_num(fname, name, pgroupNew, tgLogin):
    if collectionSt.find_one({"fname": fname, "name": name, "tgLogin": tgLogin}) is None:
        return "Пользователь не существует"
    else:
        collectionSt.update_one({"fname": fname, "name": name, "tgLogin": tgLogin},
                                {"$set": {"tgLogin": ""}})
        collectionSt.update_one({"fname": fname, "name": name, "pgroup": pgroupNew},
                                {"$set": {"tgLogin": tgLogin}})
        return "Номер группы успешно изменён"


# Изменение номера группы(проводится поиск по фамилии, имени и номер_потока/номер_группы(старый), после чего старый
# номер группы меняется на новый)

def update_tg_login(fname, name, pgroup, tgLogin):
    if collectionSt.find_one({"fname": fname, "name": name, "pgroup": pgroup}) is None:
        return "Такого студента нет"
    else:
        collectionSt.update_one({"fname": fname, "name": name, "pgroup": pgroup},
                                {"$set": {"tgLogin": tgLogin}})
        return "Телеграм логин успешно изменён"


def get_group_num(tgLogin):
    group_num = collectionSt.find_one({"tgLogin": tgLogin}, {"_id": 0, "pgroup": 1})
    if group_num is None:
        return False
    else:
        return group_num["pgroup"]


def get_student_by_login(tgLogin):
    student = collectionSt.find_one({"tgLogin": tgLogin})
    if student is None:
        return False
    else:
        return student


def get_student_by_fname(fname, name, pgroup):
    student = collectionSt.find_one({"fname": fname, "name": name, "pgroup": pgroup})
    if student is None:
        return False
    else:
        return student


def add_student(fname, name, pgroup):
    collectionSt.insert_one(
        {"fname": fname, "name": name, "pgroup": pgroup})
