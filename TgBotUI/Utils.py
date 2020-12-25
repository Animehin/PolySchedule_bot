import telebot
from datetime import datetime, timedelta
from dateutil import parser


def get_args_from_message(message):
    return message.text.split(" ")[1:]


def create_keyboard_from_string_array(array, command, stage=0, days=False):
    keyboard_max_elements = 6
    if not days:
        elem_number = -1
    else:
        elem_number = convertDate(array[0]) - timedelta(days=1)

    keyboard_elements_sorted = []
    elements = []
    for element in array:
        element = element[:25]
        if not days and len(elements) == keyboard_max_elements:
            keyboard_elements_sorted.append(elements)
            elements = [element]
            elem_number = 0
        elif not days:
            elements.append(element)
            elem_number += 1
        else:
            day = convertDate(element)
            day_num = day.weekday()
            prev_day = elem_number
            prev_day_num = prev_day.weekday()
            if prev_day_num == 7:
                prev_day_num = -1
            if (day - prev_day).days < 8 and day_num > prev_day_num:
                elements.append(element)
                elem_number = day
            else:
                keyboard_elements_sorted.append(elements)
                elements = [element]
                elem_number = convertDate(element)
    if len(elements) != 0:
        keyboard_elements_sorted.append(elements)

    keyboards = []
    for element_num in range(len(keyboard_elements_sorted)):
        current_elem = keyboard_elements_sorted[element_num]
        if len(keyboard_elements_sorted) > 1:
            if element_num != len(keyboard_elements_sorted) - 1:
                current_elem.append("👉🏿")
            if element_num != 0:
                current_elem.insert(0, "👈🏿")
        keyboard = telebot.types.InlineKeyboardMarkup()
        for key in current_elem:
            keyboard.add(telebot.types.InlineKeyboardButton(text=f"{key}",
                                                            callback_data=f"{command}_{stage}_{key}_{element_num}"))  # "hometask_0_25.12.2012_0"
        keyboards.append(keyboard)

    return keyboards


def convertDate(date):
    return parser.parse(date, dayfirst=True).date()


def parse_callback_data(data):
    args = data.split("_")
    return {'command': args[0], 'step': args[1], 'text': args[2], 'page': args[3]}


def create_human_readable_news(news_array):
    output = "Последние новости за сегодня ☠️\n"
    for element in news_array:
        output += f"{element['title']}\n{element['annotation']}\nПодробнее: {element['link'][0]}\n"
    return output


def create_weather_for_today(weather_dict):
        return f"🌪Сводка о состоянии погоды возле ГЗ: \n{weather_dict['temp']} градусов, ощущается как {weather_dict['feels_like']}\n" \
           f"{weather_dict['condition']}, направление ветра {weather_dict['wind_dir']}, {weather_dict['wind_speed']}м/c."


def generate_menu():
    commands = ["/start", "/getgroup", "/report", "/schedule", "/tasklist"]
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.row("/start", "/getgroup", "/report")
    keyboard.row("/schedule", "/tasklist")
    return keyboard


def generate_help_message():
    return "Возможные команды:\n" \
                   "/start - начать общение с ботом\n" \
                   "/help - помощь с командами\n" \
                   "/setgroup [номер группы] [Имя, Фамилия] - установить группу\n" \
                   "/changegroup [номер группы] [Имя, Фамилия] - изменить группу\n" \
                   "/schedule - выбор расписания на выбранную дату (с помощью меню)\n" \
                   "/hometask - создание домашнего задания\n" \
                   "/tasklist - просмотр активных заданий для группы\n"

  
def get_lessons_name_from_schedule(array):
    return {element['scheduledClass'] for element in array}
