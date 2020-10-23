from PolySchedule_bot.DataBase import HomeWork as HW, Schedule as sch, Students as st
import datetime as dt


def testSt():
    st.addSt("Stashevskii", "Ian", "3530904/70105")


def testSch():
    date = dt.datetime.strptime("2020-10-26T14:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    sch.addSchedule("3530904/70105", date, "Практика : Нейронные сети")


def testHW():
    date = dt.datetime.strptime("2020-10-26T14:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    HW.addHomeWork("3530904/70105", date, "Практика : Нейронные сети", "FARMIT MORU")


testSt()
testSch()
testHW()
