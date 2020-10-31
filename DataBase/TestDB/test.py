import datetime as dt

from PolySchedule_bot.DataBase.DataBase import HomeWork as HW, Schedule as sch, Students as st


def testSt():
    st.addSt("Stashevskii", "Ian", "3530904/70105")


def testSch():
    date = dt.datetime.strptime("2020-10-26T14:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    sch.addSchedule("3530904/70105", date, "Практика : Нейронные сети")


def testHW():
    date = dt.datetime.strptime("2020-10-26T14:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    a = HW.addHomeWork("3530904/70105", date, "Практика : Нейронные сети", "Фармить мору", "@blamc")
    print(a)


def testHWR():
    date = dt.datetime.strptime("2020-10-26T14:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    print(HW.readHomeWork("3530904/70105", date, "Практика : Нейронные сети"))


# testSt()
# testSch()
testHW()
testHWR()
