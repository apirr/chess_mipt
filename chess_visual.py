from PIL import Image
'PIL version is 8.3.2'

class Drawer:
    def __init__(self, board):
        '''
        :param board: объект класса Board, доска с фигурами
        '''
        self.board = board
        self.board_for_print = [[['*'] for i in range(8)] for i in range(8)]
    def bot_print(self):
        '''
        Make image for user.
        '''
        for row in self.board_for_print:
            for cell in row:
                if cell is row[7]:
                    print(cell[0])
                else:
                    print(cell[0], end=' ')
    def make_board_for_print(self):
        '''
        Обновляет board_for_print на основе позиций фигур, хранящихся в board.
        Ch_p = chess_piece
        '''
        for ch_p in self.board:
            self.board_for_print[ch_p.position[1]][ch_p.position[0]] = ch_p.color + ch_p.type


drawer = Drawer([])
drawer.bot_print()
