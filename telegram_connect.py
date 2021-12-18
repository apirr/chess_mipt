import telebot


token = input()

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])

class simple_bot(bot):
    def get_message(message):
        message.text =


def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Здесь можно словить хихи-хаха")
        photo = open('/Downloads/Figure_1.png', 'rb')
        bot.send_photo(message.from_user.id, photo)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "напиши число от 1 до 3 и получишь юмореску")
    elif message.text == "1":
        bot.send_message(message.from_user.id,
                        "Сидят в купе поезда два хохла, пьют водку, ведут разговоры на разные философские темы. ")
    elif message.text == "2":
        bot.send_message(message.from_user.id,
                        "Папа с сыном пошли однажды на горы, и сын, ударившись о камень, крикнул: ")
    elif message.text == "3":
        bot.send_message(message.from_user.id,
                        "Подходит карлик к Макаревичу:")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
