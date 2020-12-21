import datetime as dt

from PolySchedule_bot.DataBase.DataBase import HomeWork as HW, Schedule as sch, Students as st


def testSt():
    st.add_student("Stashevskii", "Ian", "3530904/70105")


def testSch():
    sch.add_schedule("3530904/70105", "10:00-11:40 20.10.2020", "Практика : Нейронные сети")


def testHW():
    a = HW.add_home_work("3530904/70105", "10:00-11:40 20.10.2020", "Практика : Нейронные сети", "Фармить мору",
                         "@blamc1")
    print(a)


def testHWR():
    print(HW.read_home_work("3530904/70105", "10:00-11:40 20.10.2020", "Практика : Нейронные сети"))


def testSt_g_G_N():
    print(st.get_group_num("@Animehin"))


def testSt_u_TG_Login():
    st.update_tg_login("Stashevskii", "Ian", "3530904/70105", "@Animehin")


def testSchR():
    print(sch.read_schedule("27.10.2020"))


# testSt()
# testSch()
# testHW()
# testHWR()
# testSt_u_TG_Login()
# testSt_g_G_N()
# testSchR()
