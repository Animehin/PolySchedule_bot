import pymongo

clientUS = pymongo.MongoClient('localhost', 27017)
dbUS = clientUS['TgBot']
collectionUS = dbUS['UserStatus']
collectionUSList = []


def upd_user_status(tgLogin, step, data):
    collectionUS.update_one({"tgLogin": tgLogin, "step": step},
                            {"$set": {"step": step, "data": data}})


def add_user_status(tgLogin, step, data):
    if collectionUS.find_one({"tgLogin": tgLogin, "step": step, "data": data}) is None:
        try:
            collectionUS.insert_one({"tgLogin": tgLogin, "step": step, "data": data})
        except pymongo.errors.WriteError:
            return "User cannot be added"
    else:
        upd_user_status(tgLogin, step, data)
    return "User added"


def del_user_status(tgLogin):
    if collectionUS.find_one({"tgLogin": tgLogin}) is None:
        return "Status for {} is not exist".format(tgLogin)
    else:
        collectionUS.delete_one({"tgLogin": tgLogin})
        return "Status for {} deleted".format(tgLogin)
