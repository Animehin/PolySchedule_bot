import pymongo

clientUS = pymongo.MongoClient('localhost', 27017)
dbUS = clientUS['TgBot']
collectionUS = dbUS['UserStatus']
collectionUSList = []


def upd_user_status(tgLogin, step, data):
    collectionUS.update_one({"tgLogin": tgLogin},
                            {"$set": {"step": step, "data": data}})


def add_user_status(tgLogin, step, data):
    if collectionUS.find_one({"tgLogin": tgLogin, "step": step, "data": data}) is None:
        try:
            collectionUS.insert_one({"tgLogin": tgLogin, "step": step, "data": data})
        except pymongo.errors.WriteError:
            return "Пользователь не может быть добавлен"
    else:
        upd_user_status(tgLogin, step, data)
    return "Пользователь добавлен"


def del_user_status(tgLogin):
    if collectionUS.find_one({"tgLogin": tgLogin}) is None:
        return "Статус для пользователя {} не найден".format(tgLogin)
    else:
        collectionUS.delete_one({"tgLogin": tgLogin})
        return "Статус для пользователя {} удалён".format(tgLogin)


def read_user_status(tgLogin):
    userStatus = collectionUS.find_one({"tgLogin": tgLogin})
    if userStatus is None:
        return "Пользовательский статус ненайден"
    else:
        return userStatus
