import telebot
from chess_internals import Board
from visual.chess_visual import Drawer

boards = []  # массив объектов Board

bot = telebot.TeleBot(input())  # принимаем токен бота


@bot.message_handler(content_types=['text'])  # выбираем формат сообщений, которые будем принимать
def get_start(message):
    ''' эта функция встречает игрока в начале игры'''
    if message.text.lower() == "начать игру":
        bot.send_message(message.from_user.id, "хотите присоединиться или начать новую?")
        bot.register_next_step_handler(message, password_choose)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши начать игру")
        bot.register_next_step_handler(message, get_start)


def password_choose(message):
    ''' эта функция определяет хочет человек задать новый пароль или вписать пароль соперника'''
    if message.text.lower() == "вернуться" or message.text.lower() == "назад":
        bot.register_next_step_handler(message, get_start)
    if message.text.lower() == "начать новую" or message.text.lower() == "новую":
        bot.send_message(message.from_user.id, "придумайте пароль")
        bot.register_next_step_handler(message, password_creating)
    elif message.text.lower() == "хочу присоединиться" or message.text.lower() == "присоединиться":
        bot.send_message(message.from_user.id, "напишите пароль своего соперника")
        bot.register_next_step_handler(message, password_writing)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, скажи хочешь начать новую игру или присоединиться")
        bot.register_next_step_handler(message, password_choose)


def password_creating(message):
    ''' создание доски с новым паролем'''
    if message.text.lower() == "вернуться" or message.text.lower() == "назад":
        bot.register_next_step_handler(message, get_start)
    else:
        flag = True
        for board in boards:
            # проверка на существование такого пароля в других играх
            if message.text == board.game_password:
                flag = False
                bot.send_message(message.from_user.id, "такой пароль уже существует, придумайте другой")
                bot.register_next_step_handler(message, password_creating)
                break
        if flag:
            bot.send_message(message.from_user.id, "теперь отправьте этот пароль человеку с которым хотите играть")
            board = Board(message.from_user.id, message.text)
            boards.append(board)
            # ждем пока зайдет второй игрок чтобы начать игру
            while 1:
                if board.black_id != "black":
                    bot.send_message(message.from_user.id, "игра началась")
                    bot.send_message(message.from_user.id, "ход пишите в формате e2 e4 или e2-e4")
                    break
            bot.register_next_step_handler(message, get_move)


def password_writing(message):
    '''поиск доски с вписанным паролем соперника'''
    if message.text.lower() == "вернуться" or message.text.lower() == "назад":
        bot.register_next_step_handler(message, get_start)
    flag = True
    for board in boards:
        if message.text == board.game_password:
            flag = False
            board.black_id = message.from_user.id
            bot.send_message(message.from_user.id, "пароль найден вы играете за черных")
            bot.send_message(message.from_user.id, "не пишите ничего пока не сходит ваш соперник")
            wait(message)  # мы отправляем игрока в функцию wait, потому что первых ход делает соперник
            bot.send_message(message.from_user.id, "ход пишите в формате e2 e4 или e2-e4")
            bot.register_next_step_handler(message, get_move)
            # как только цикл в функции wait обрывается мы попадаем в функцию move
            break
    if flag:
        bot.send_message(message.from_user.id, "пароль не найден попробуйте еще раз")
        bot.register_next_step_handler(message, password_writing)


def get_move(message):
    ''' функция нужна чтобы сделать ход
    сначала она проверяет что ход удовлетворяет формату, потом что его можно сделать
    если ход все хорошо, то функция делает ход, присылает картинку доски со сделанным ходом'''
    if ((len(message.text) == 5) and
            (message.text.lower()[0] >= "a" and message.text.lower()[0] <= "h") and
            (message.text.lower()[1] >= "1" and message.text.lower()[1] <= "8") and
            (message.text.lower()[2] == " " or message.text.lower()[2] == "-") and  # проверка на правильный формат
            (message.text.lower()[3] >= "a" and message.text.lower()[3] <= "h") and
            (message.text.lower()[1] >= "1" and message.text.lower()[1] <= "8")):
        for board in boards:
            if ((message.from_user.id == board.black_id and
                 board.whose_move_it_is == "b")
                    or
                    (message.from_user.id == board.white_id and
                     board.whose_move_it_is == "w")):
                # проверка на возможность сделать ход
                if board.move_this_chess_piece(move_coordinates_creator(message.text.lower())[0],
                                               move_coordinates_creator(message.text.lower())[1]):
                    bot.send_message(message.from_user.id, "принято")
                    drawer = Drawer(board)
                    drawer.make_board_for_print()
                    with open(drawer.bot_print(), 'rb') as photo:
                        bot.send_photo(message.from_user.id,
                                       photo)  # функция присылает картинку доски со сделанным ходом
                    wait(message)  # перенапрявляем игрока в другую функцию
                    bot.register_next_step_handler(message,
                                                   get_move)  # сюда мы попадаем когда цикл в функции wait обрывается
                else:
                    bot.send_message(message.from_user.id, "этот ход невозможно сделать")
                    bot.register_next_step_handler(message, get_move)

    else:
        bot.send_message(message.from_user.id, "это не похоже на ход")
        bot.register_next_step_handler(message, get_move)


def wait(message):
    ''' эта функция ждет пока сходит соперник игрока и постоянно проверяет это
    как только это произошло бот присылает игроку картинку доски с ходом соперника
    цикл обрывается и мы попадаем снова в get_move'''
    flag = True
    while 1:
        if flag:
            for board in boards:
                # проверка совпадает ли id человека который сейчас должен ходить c id нашего игрока
                if ((message.from_user.id == board.black_id and
                     board.whose_move_it_is == "b")
                        or
                        (message.from_user.id == board.white_id and
                         board.whose_move_it_is == "w")):
                    # если совпадает значит теперь ходит наш игрок
                    drawer = Drawer(board)
                    drawer.make_board_for_print()
                    # отправка картинки со сделанным ходом соперника
                    with open(drawer.bot_print(), 'rb') as photo:
                        bot.send_photo(message.from_user.id, photo)
                    bot.send_message(message.from_user.id, "ходите")
                    flag = False
                    break
        else:
            break


def move_coordinates_creator(move):
    ''' эта функция преобразует формат хода, написанный игроком, 
    в формат хода необходимый методу move_this_chess_piece'''
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
