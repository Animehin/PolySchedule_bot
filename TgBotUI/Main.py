import telebot
import schedule
from TgBotUI import Utils, CommonMessages
from DataBase import Students, Schedule, UserStatus, HomeWork
from TgBotUI import DataBaseExtension as dbExt
from YandexInfoProvider import WeatherProvider, NewsProvider
from datetime import datetime, timedelta

token = ''
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_button(message):
    message_text = 'Пример команды:\n/setgroup Группа Фамилия Имя - указание своей группы'
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['setgroup'])
def set_group(message):
    args = Utils.get_args_from_message(message)
    user_login = message.from_user.username
    if len(args) < 3:
        bot.send_message(message.chat.id, CommonMessages.invalid_arguments)
        UserStatus.del_user_status(user_login)
        return
    response = Students.update_tg_login(args[1], args[2], args[0], message.from_user.username)  # name, surname, group, username
    bot.send_message(message.chat.id, response)
    UserStatus.del_user_status(user_login)


@bot.message_handler(commands=['getgroup'])
def get_group(message):
    user_login = message.from_user.username
    group = Students.get_group_num(user_login)
    bot.send_message(message.chat.id, f"Текущая установленная группа: {group}")
    UserStatus.del_user_status(user_login)


@bot.message_handler(commands=['schedule'])
def get_schedule(message):
    user_login = message.from_user.username
    group_num = Students.get_group_num(user_login)
    if group_num:
        schedule_var = dbExt.get_schedule_dates(group_num)  # Add data from another module
        keyboards = Utils.create_keyboard_from_string_array(schedule_var, "schedule", days=True)
        bot.send_message(message.chat.id, "Выберите даты для получения расписания на число:", reply_markup=keyboards[0])
        UserStatus.del_user_status(user_login)
    else:
        bot.send_message(message.chat.id, CommonMessages.set_group)
        UserStatus.del_user_status(user_login)


@bot.message_handler(commands=['hometask'])
def add_home_task(message):
    user_login = message.from_user.username
    group_num = Students.get_group_num(user_login)
    if group_num:
        schedule_var = dbExt.get_schedule_dates(group_num)   # Add data from another module
        keyboards = Utils.create_keyboard_from_string_array(schedule_var, "hometask", days=True)
        bot.send_message(message.chat.id, "Выберите дату для домашнего задания:", reply_markup=keyboards[0])
        UserStatus.del_user_status(user_login)
    else:
        bot.send_message(message.chat.id, CommonMessages.set_group)
        UserStatus.del_user_status(user_login)


@bot.message_handler(commands=['tasklist'])
def task_list(message):
    user_login = message.from_user.username
    group_num = Students.get_group_num(user_login)
    if group_num:
        homeworks = dbExt.get_home_tasks(group_num)
        ln = '\n=============================\n'
        bot.send_message(message.chat.id, f"{ln.join(task for task in homeworks)}")
    else:
        bot.send_message(message.chat.id, CommonMessages.set_group)
        UserStatus.del_user_status(user_login)


@bot.message_handler(commands=['report'])
def task_list(message):
    user_login = message.from_user.username
    group_num = Students.get_group_num(user_login)
    today_date = datetime.today().date()
    if group_num:
        news = NewsProvider.getNews(3)
        news_text = Utils.create_human_readable_news(news)
        weather = WeatherProvider.getWeatherForDate(today_date)
        weather_text = Utils.create_weather_for_today(weather)
        bot.send_message(message.chat.id, f"{news_text}\n\n{weather_text}")
    else:
        bot.send_message(message.chat.id, CommonMessages.set_group)
        UserStatus.del_user_status(user_login)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    args_dict = Utils.parse_callback_data(call.data)  # command-name, step, text, page
    user_login = call.from_user.username
    group_num = Students.get_group_num(user_login)
    if not group_num:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=CommonMessages.set_group)

    # schedule and hometask pages check, also schedule day selection included
    if args_dict['command'] == 'schedule' or (args_dict['command'] == 'hometask' and args_dict['step'] == '0'):
        if args_dict['text'] == "👉🏿":
            schedule_var = dbExt.get_schedule_dates(group_num)  # Add data from another module
            keyboards = Utils.create_keyboard_from_string_array(schedule_var, args_dict['command'], days=True)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=call.message.text,
                                  reply_markup=keyboards[int(args_dict['page']) + 1])
            return
        elif args_dict['text'] == "👈🏿":
            schedule_var = dbExt.get_schedule_dates(group_num)  # Add data from another module
            keyboards = Utils.create_keyboard_from_string_array(schedule_var, args_dict['command'], days=True)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=call.message.text,
                                  reply_markup=keyboards[int(args_dict['page']) - 1])
            return
    if args_dict['command'] == 'schedule':
        schedule = dbExt.get_scheduled_lessons(group_num, args_dict['text'])
        nl = '\n'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f"Предметы на {args_dict['text']}:{nl}{f'{nl}'.join(f'{lesson}' for lesson in schedule)}")
        return

    if args_dict['command'] == 'hometask':
        if args_dict['step'] == '0':
            schedule = dbExt.get_scheduled_lessons(group_num, args_dict['text'])
            keyboards = Utils.create_keyboard_from_string_array(schedule, args_dict['command'], stage=1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"Выберите из списка предметов:",
                                  reply_markup=keyboards[0]
                                  )
            UserStatus.add_user_status(user_login, args_dict['step'], [args_dict['command'], args_dict['text']])
            return
        if args_dict['step'] == '1':
            status = UserStatus.read_user_status(user_login)
            command = status['data'][0]
            date = status['data'][1]

            if command != 'hometask':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=call.message.text)
                bot.send_message(call.message.chat.id, CommonMessages.invalid_button)
                UserStatus.del_user_status(user_login)
                return

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"Выбран предмет:\n{args_dict['text']} на {date}.\n"
                                       f"Отправьте текст задания сообщением.\nДля отмены введите 'Отмена'")
            UserStatus.add_user_status(user_login, args_dict['step'], [command, date, args_dict['text']])
            pass


@bot.message_handler(content_types=['text'])
def message_worker(message):
    user_login = message.from_user.username
    group_num = Students.get_group_num(user_login)
    user_status = UserStatus.read_user_status(user_login)
    print(user_status)
    if len(user_status['data']) < 3:
        return
    command = user_status['data'][0]
    date = user_status['data'][1]
    lesson = user_status['data'][2]
    if not group_num:
        bot.send_message(message.chat.id, CommonMessages.set_group)
        UserStatus.del_user_status(user_login)
        return
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, CommonMessages.canceled)
        UserStatus.del_user_status(user_login)
        return
    if command == "hometask":
        lesson_type = dbExt.read_schedule_lesson(group_num, date, lesson)
        print(HomeWork.add_home_work(group_num, date, lesson, lesson_type, message.text, user_login))
        bot.send_message(message.chat.id, "ДЗ успешно добавлено.")
        UserStatus.del_user_status(user_login)


def scheduled_schedule():
    students = Students.get_chat_ids()
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    groups_schedule = {}
    nl = '\n'
    for student in students:
        student_group = students['pgroup']
        chat_id = students['chat_id']
        if student_group not in groups_schedule:
            groups_schedule[student_group] = dbExt.get_scheduled_lessons(student_group, tomorrow)
        if len(groups_schedule[student_group]) > 0:
            text = f"Привет! Предметы на {tomorrow}:{nl}{f'{nl}'.join(f'{lesson}' for lesson in (groups_schedule[student_group]))}'"
            bot.send_message(chat_id, text)



def scheduled_news():
    pass


if __name__ == '__main__':
    bot.polling()
    schedule.every().day.at("20:00").do(scheduled_schedule())
