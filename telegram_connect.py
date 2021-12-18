import telebot


token = input()

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])


def get_start(message):
    if message.text == "Начать игру":
        bot.send_message(message.from_user.id, "Выберите тип доски:text или image")
        bot.register_next_step_handler(message, get_board_type)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши Начать игру")

def get_board_type(message):
    if message.text == "text":
        bot.send_message(message.from_user.id, "Напишите через пробел или тире ход который вы хотите сделать(используйте маленькие буквы)")
        bot.register_next_step_handler(message, get_move)
        return("text")
    if message.text == "image":
        bot.send_message(message.from_user.id, "Напишите через пробел или тире ход который вы хотите сделать(используйте маленькие буквы)")
        bot.register_next_step_handler(message, get_move)
        return("image")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, попробуй еще раз")
        bot.register_next_step_handler(message, board_type)


def get_move(message):
    if (message.text[0] >= "a" and message.text[0] <= "h"):
        if (message.text[1] >= "1" and message.text[1] <= "8"):
            if (message.text[2] == " " or message.text[2] == "-"):
                if (message.text[3] >= "a" and message.text[3] <= "h"):
                    if (message.text[1] >= "1" and message.text[1] <= "8"):
                        bot.send_message(message.from_user.id, "Принято") 
                        bot.register_next_step_handler(message, wait_for_move)
                        return message.text
                    else:
                        bot.send_message(message.from_user.id, "Я тебя не понимаю, попробуй написать ход еще раз")     
                        bot.register_next_step_handler(message, get_move)

def wait_for_move(message):
    if message.text:
        bot.send_message(message.from_user.id, "Ждите пока сходит ваш соперник")
        bot.register_next_step_handler(message, wait_for_move)

bot.polling(none_stop=True, interval=0)
