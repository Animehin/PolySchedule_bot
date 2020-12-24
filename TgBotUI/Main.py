import telebot
from TgBotUI import Utils, CommonMessages
from DataBase import Students, Schedule, UserStatus

token = ''
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_button(message):
    message_text = 'Пример команды:\n/setgroup Группа Фамилия Имя - указание своей группы'
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['setgroup'])
def set_group(message):
    args = Utils.get_args_from_message(message)
    if len(args) < 3:
        bot.send_message(message.chat.id, CommonMessages.invalid_arguments)
        return
    Students.update_tg_login(args[1], args[2], args[0], message.from_user.username)  # name, surname, group, username


@bot.message_handler(commands=['getgroup'])
def get_group(message):
    pass
    group = Students.get_group_num(message.from_user.username)
    bot.send_message(message.chat.id, f"Текущая установленная группа: {group}")


@bot.message_handler(commands=['schedule'])
def get_schedule(message):
    schedule_var = ["26.12.2020", "27.12.2020", "29.12.2020", "07.01.2020"]  # Add data from another module
    keyboards = Utils.create_keyboard_from_string_array(schedule_var, "schedule", days=True)
    bot.send_message(message.chat.id, "Выберите даты для получения расписания на число:", reply_markup=keyboards[0])


@bot.message_handler(commands=['hometask'])
def add_home_task(message):
    schedule_var = ["26.12.2020", "27.12.2020", "29.12.2020", "07.01.2020"]  # Add data from another module
    keyboards = Utils.create_keyboard_from_string_array(schedule_var, "hometask", days=True)
    bot.send_message(message.chat.id, "Выберите дату для домашнего задания:", reply_markup=keyboards[0])


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    args_dict = Utils.parse_callback_data(call.data)  # command-name, step, text, page
    user_login = call.from_user.username

    # schedule and hometask pages check, also schedule day selection included
    if args_dict['command'] == 'schedule' or (args_dict['command'] == 'hometask' and args_dict['step'] == '0'):
        if args_dict['text'] == "👉🏿":
            schedule_var = ["26.12.2020", "27.12.2020", "29.12.2020", "07.01.2020"]  # Add data from another module
            keyboards = Utils.create_keyboard_from_string_array(schedule_var, args_dict['command'], days=True)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=call.message.text,
                                  reply_markup=keyboards[int(args_dict['page']) + 1])
            return
        elif args_dict['text'] == "👈🏿":
            schedule_var = ["26.12.2020", "27.12.2020", "29.12.2020", "07.01.2020"]  # Add data from another module
            keyboards = Utils.create_keyboard_from_string_array(schedule_var, args_dict['command'], days=True)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=call.message.text,
                                  reply_markup=keyboards[int(args_dict['page']) - 1])
            return
    if args_dict['command'] == 'schedule':
        schedule = ["Рус яз", "Матан"]
        nl = '\n'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f"Предметы на {args_dict['text']}:{nl}{f'{nl}'.join(f'{lesson}' for lesson in schedule)}")
        return

    if args_dict['command'] == 'hometask':
        if args_dict['step'] == '0':
            schedule = ["Рус яз", "Матан", "Рус яз", "Матан", "Рус яз", "Матан", "Рус яз", "Матан", "Рус яз", "Матан",
                        "Рус яз", "Матан"]
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
                                  text=f"Выбран предмет {args_dict['text']} на {date}.\n"
                                       f"Отправьте текст задания сообщением.\nДля отмены введите 'Отмена'")
            UserStatus.add_user_status(user_login, args_dict['step'], [command, date, args_dict['text']])
            pass


if __name__ == '__main__':
    bot.polling()
