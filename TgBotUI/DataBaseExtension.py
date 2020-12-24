from DataBase import Schedule, HomeWork


def get_schedule_dates(pgroup):
    schedule_dates = Schedule.read_schedule(pgroup).distinct("date")
    return schedule_dates


def get_scheduled_lessons(pgroup, date):
    scheduled_lessons = Schedule.read_schedule(pgroup, date).distinct("scheduledClass")
    return scheduled_lessons


def get_home_tasks(pgroup):
    request = HomeWork.read_home_work(pgroup)
    home_tasks = []
    for task in request:
        home_tasks.append(
            task["date"] + "\n" + task["className"] + "\n" + task["classType"] + "\n" + "Задание: " + task[
                "homeWork"] + "\n" + "Aвтор: " + task[
                "tgLogin"])
    return home_tasks
