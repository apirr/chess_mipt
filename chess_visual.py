

class Drawer:
    def __init__(self, board):
        self.board = board
        self.board_for_print = [[[0] for i in range(8)] for i in range(8)]
        self.smth_is_moved = False
    def move(self, pos): #Вообще кажется, что эта проверка не должна происходить в дровере. Дровер он рисует
        for chess_piece in self.board:
            if chess_piece.moved:
                self.smth_is_moved = True
        if not self.smth_is_moved:
            return False #дальше уже в telegram_connect.py/bot_main.py сделать вывод сообщения 'Your turn is wrong'
    def bot_print(self):
        for row in self.board_for_print:
            for cell in row:
                if cell is row[7]:
                    print(cell[0])
                else:
                    print(cell[0], end=' ')
    def make_board_for_print(self):
        for chess_piece in self.board:
            if chess_piece.color == 'white':
                self.board_for_print[chess_piece.position[1]][chess_piece.position[0]] = chess_piece.type[0].upper()
            else:
                self.board_for_print[chess_piece.position[1]][chess_piece.position[0]] = chess_piece.type[0]
