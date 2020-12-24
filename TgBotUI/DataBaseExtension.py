from DataBase import Schedule, HomeWork


def get_schedule_dates(pgroup):
    schedule_dates = Schedule.read_schedule(pgroup).distinct("date")
    return schedule_dates


def get_scheduled_lessons(pgroup, date):
    scheduled_lessons = Schedule.read_schedule(pgroup, date).distinct("scheduledClass")
    return scheduled_lessons


def read_schedule_lesson(pgroup, date, className):
    is_lection = 0
    shedule_lesson = []
    sheduled_lessons = Schedule.read_schedule(pgroup, date)
    for lesson in sheduled_lessons:
        if className in lesson["scheduledClass"]:
            shedule_lesson.append(lesson["classType"])
        print(lesson)
    if len(shedule_lesson) > 1:
        for i in shedule_lesson:
            if i != "Лекция":
                is_lection += 1
                return i
            elif is_lection > 0:
                return i
    return shedule_lesson[0]


def get_home_tasks(pgroup):
    request = HomeWork.read_home_work(pgroup)
    home_tasks = []
    for task in request:
        home_tasks.append(
            task["date"] + "\n" + task["className"] + "\n" + task["classType"] + "\n" + "Задание: " + task[
                "homeWork"] + "\n" + "Aвтор: " + task[
                "tgLogin"])
    return home_tasks
