import telebot
from chess_internals import Board
from visual.chess_visual import Drawer

boards = []


bot = telebot.TeleBot("5018966046:AAH_8hqUJuQbEUJEGYTwNM4U5PK2rvcjfI4")
@bot.message_handler(content_types=['text'])

def get_start(message):
    if message.text.lower() == "начать игру":
        bot.send_message(message.from_user.id, "хотите присоединиться или начать новую?")
        bot.register_next_step_handler(message, password_choose)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши начать игру")
        bot.register_next_step_handler(message, get_start)

def password_choose(message):
    if message.text.lower() == "начать новую" or message.text.lower() == "новую":
        bot.send_message(message.from_user.id, "придумайте пароль")
        bot.register_next_step_handler(message, password_creating)
    elif message.text == "хочу присоединиться" or message.text == "присоединиться":
        bot.send_message(message.from_user.id, "напишите пароль своего соперника")
        bot.register_next_step_handler(message, password_writing)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, скажи хочешь начать новую игру или присоединиться")
        bot.register_next_step_handler(message, password_choose)

def password_creating(message):
    if message.text.lower() == "вернуться" or message.text.lower() == "назад":
        bot.register_next_step_handler(message, get_start)
    flag = True
    for board in boards:
        if message.text == board.game_password:
            flag = False
            bot.send_message(message.from_user.id, "такой пароль уже существует, придумайте другой")
            bot.register_next_step_handler(message, password_creating)
            break
    if flag:
        bot.send_message(message.from_user.id, "теперь отправьте этот пароль человеку с которым хотите играть")
        board = Board(message.from_user.id, message.text)
        boards.append(board)
        while 1:
            if board.black_id != "black":
                bot.send_message(message.from_user.id, "игра началась")
                break
        bot.register_next_step_handler(message, get_move)

def password_writing(message):
    if message.text.lower() == "вернуться" or message.text.lower() == "назад":
        bot.register_next_step_handler(message, get_start)
    flag = True
    for board in boards:
        if message.text == board.game_password:
            flag = False
            bot.send_message(message.from_user.id, "пароль найден вы играете за черных")
            board.black_id = message.from_user.id
            wait(message)
            #bot.register_next_step_handler(message, wait_for_move)
            break
    if flag:
        bot.send_message(message.from_user.id, "пароль не найден попробуйте еще раз")
        bot.register_next_step_handler(message, password_writing)

def get_move(message):
  #  if (message.text[0] >= "a" and message.text[0] <= "h"):
  #      if (message.text[1] >= "1" and message.text[1] <= "8"):
  #          if (message.text[2] == " " or message.text[2] == "-"):
  #              if (message.text[3] >= "a" and message.text[3] <= "h"):
  #                  if (message.text[1] >= "1" and message.text[1] <= "8"):
                        bot.send_message(message.from_user.id, "я в муве")
                        for board in boards:
                            if ((message.from_user.id == board.black_id and
                                 board.whose_move_it_is == "black")
                                    or
                                    (message.from_user.id == board.white_id and
                                     board.whose_move_it_is == "white")):
                                if board.move_this_chess_piece(move_coordinates_creator(message.text)[0], move_coordinates_creator(message.text)[1]):
                                    bot.send_message(message.from_user.id, "принято")
                                    drawer = Drawer(board)
                                    drawer.make_board_for_print()
                                    with open(drawer.bot_print(), 'rb') as photo:
                                        bot.send_photo(message.from_user.id, photo)
                                    wait(message)
                                    #bot.register_next_step_handler(message, wait_for_move)
                                else:
                                    bot.send_message(message.from_user.id, "этот ход невозможно сделать")
                                    bot.register_next_step_handler(message, get_move)
     #               else:
    #                   bot.send_message(message.from_user.id, "это не похоже на ход")
    #                    bot.register_next_step_handler(message, get_move)

def wait(message):
    while 1:
        for board in boards:
            if ((message.from_user.id == board.black_id and
            board.whose_move_it_is == "black")
            or
            (message.from_user.id == board.white_id and
            board.whose_move_it_is == "white")):
                drawer = Drawer(board)
                drawer.make_board_for_print()
                with open(drawer.bot_print(), 'rb') as photo:
                    bot.send_photo(message.from_user.id, photo)
                bot.send_message(message.from_user.id, "ходите")
                bot.register_next_step_handler(message, get_move)

'''
def wait_for_move(message):
    if message.text and tmp == 0:
        bot.send_message(message.from_user.id, "Ждите пока сходит ваш соперник")
        tmp += 1
    for board in boards:
        if ((message.from_user.id == board.black_id and
        board.whose_move_it_is == "black")
        or
        (message.from_user.id == board.white_id and
        board.whose_move_it_is == "white")):
            drawer = Drawer(board)
            drawer.make_board_for_print()
            with open(drawer.bot_print(), 'rb') as photo:
                    bot.send_photo(message.from_user.id, photo)
            bot.register_next_step_handler(message, get_move
                                           
                                           '''

def move_coordinates_creator(move):
    mas = []
    for i in [0, 3]:
        if move[i] == 'a':
            mas.append(0)
        if move[i] == 'b':
            mas.append(1)
        if move[i] == 'c':
            mas.append(2)
        if move[i] == 'd':
            mas.append(3)
        if move[i] == 'e':
            mas.append(4)
        if move[i] == 'f':
            mas.append(5)
        if move[i] == 'g':
            mas.append(6)
        if move[i] == 'h':
            mas.append(7)
    start_position = [mas[0], int(move[1]) - 1]
    finish_position = [mas[1], int(move[4]) - 1]
    return start_position, finish_position

bot.polling(none_stop=True, interval=0)
