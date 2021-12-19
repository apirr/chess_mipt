import telebot
from chess_internals import Board
from visual.chess_visual import Drawer

boards = []


bot = telebot.TeleBot(input())
@bot.message_handler(content_types=['text'])

def get_start(message):
    bot.send_message(message.from_user.id, "Напишите Начать игру")
    if message.text == "Начать игру":
        bot.send_message(message.from_user.id, "хотите присоединиться или начать новую?")
        bot.register_next_step_handler(message, password_choose)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши Начать игру")
        bot.register_next_step_handler(message, get_start)

def password_choose(message):
    if message.text == "начать новую":
        bot.register_next_step_handler(message, password_creating)
        bot.send_message(message.from_user.id, "придумайте пароль")
    elif message.text == "хочу присоединиться" or message.text == "присоединиться":
        bot.register_next_step_handler(message, password_writing)
        bot.send_message(message.from_user.id, "напишите пароль своего соперника")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши Начать игру")
        bot.register_next_step_handler(message, password_choose)

def password_creating(message):
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
                break
        bot.register_next_step_handler(message, get_move)

def password_writing(message):
    flag = True
    for board in boards:
        if message.text == board.game_password:
            flag = False
            bot.send_message(message.from_user.id, "пароль найден вы черный")
            board.black_id = message.from_user.id
            bot.register_next_step_handler(message, wait_for_move)
            break
    if flag:
        bot.send_message(message.from_user.id, "пароль не найден попробуйте еще раз")
        bot.register_next_step_handler(message, password_writing)

def get_move(message):
    if (message.text[0] >= "a" and message.text[0] <= "h"):
        if (message.text[1] >= "1" and message.text[1] <= "8"):
            if (message.text[2] == " " or message.text[2] == "-"):
                if (message.text[3] >= "a" and message.text[3] <= "h"):
                    if (message.text[1] >= "1" and message.text[1] <= "8"):
                        for board in boards:
                            if ((message.from_user.id == board.black_id and
                                 board.whose_move_it_is == "black")
                                    or
                                    (message.from_user.id == board.white_id and
                                     board.whose_move_it_is == "white")):
                                if board.move_this_chess_piece(move_coordinates_creator(message.text)):
                                    drawer = Drawer(board.chess_pieces)
                                    drawer.make_board_for_print()
                                    with open(drawer.bot_print(), 'rb') as photo:
                                        bot.send_photo(message.from_user.id, photo)
                                    bot.register_next_step_handler(message, wait_for_move)
                                else:
                                    bot.send_message(message.from_user.id, "этот ход невозможно сделать")
                    else:
                        bot.send_message(message.from_user.id, "это не похоже на ход")
                        bot.register_next_step_handler(message, get_move)

def wait_for_move(message):
    if message.text:
        bot.send_message(message.from_user.id, "Ждите пока сходит ваш соперник")
        bot.register_next_step_handler(message, wait_for_move)
    while 1:
        for board in boards:
            if ((message.from_user.id == board.black_id and
            board.whose_move_it_is == "black")
            or
            (message.from_user.id == board.white_id and
            board.whose_move_it_is == "white")):
                drawer = Drawer(board.chess_pieces)
                drawer.make_board_for_print()
                with open(drawer.bot_print(), 'rb') as photo:
                    bot.send_photo(message.from_user.id, photo)
                bot.register_next_step_handler(message, get_move)

def move_coordinates_creator(move):
    for i in [0, 3]:
        if move[i] == 'a':
            move[i] = 0
        if move[i] == 'b':
            move[i] = 1
        if move[i] == 'c':
            move[i] = 2
        if move[i] == 'd':
            move[i] = 3
        if move[i] == 'e':
            move[i] = 4
        if move[i] == 'f':
            move[i] = 5
        if move[i] == 'g':
            move[i] = 6
        if move[i] == 'h':
            move[i] = 7
    start_position = [move[0], move[1] - 1]
    finish_position = [move[3], move[4] - 1]
    return start_position, finish_position

bot.polling(none_stop=True, interval=0)
