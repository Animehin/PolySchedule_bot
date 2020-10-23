import telebot

bot = telebot.TeleBot('1357980522:AAHNJq9kXb5JrvsscCYltfPJwqnA91CXJgQ')

@bot.message_handler(commands=['start'])
def start_menu(message):
    message_text = 'Здравствуйте!\n' \
                   + 'Наберите /setgroup - для выбора номера группы.'
    bot.send_message(message.chat.id, message_text)
    bot.register_next_step_handler(message, set_group)

# @bot.message_handler(commands=['help'])
# def print_menu(message):
#     message_text = 'Вот, что умеет этот бот:\n' \
#                    + '/help - отображает список доступных команд\n' \
#                    + '/setgroup - Необходимо ввести свой номер группы'
#     bot.send_message(message.chat.id, message_text)

# keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard1.row('/show', 'Пока')

group = ''
@bot.message_handler(commands=['setgroup'])
def set_group(message):
    bot.send_message(message.chat.id, 'Введите номер группы и Фамилию Имя через пробел')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '3530904/70105':
        bot.send_message(message.chat.id, 'Ваш номер группы ' + message.text)
    else:
        bot.send_message(message.chat.id, 'Такого номера группы не существует')



# keyboard2 = telebot.types.ReplyKeyboardMarkup(True,True)
# keyboard2.row('button1', 'button2', 'button3','button4')
# keyboard2.row('button5', 'button6', 'button7','button8')
# @bot.message_handler(commands=['show'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Привет, ты написал мне /show', reply_markup=keyboard2)

if __name__ == '__main__':
    bot.polling()
