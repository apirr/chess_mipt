from PIL import Image
from os import remove

'PIL version is 8.3.2'


def resized_chess_piece_image(where_to_paste_image: Image, what_to_paste_image: Image):
    '''
    Change chess_piece image size so it fits board image size.
    :param where_to_paste_image: board .png PIL image
    :param what_to_paste_image: chess_piece .png PIL image
    :return: resized chess_piece .png PIL image
    '''

    ch_p_image_size_width = (where_to_paste_image.size[0] - 100) // 8
    ch_p_image_size_height = (where_to_paste_image.size[1] - 103) // 8
    return what_to_paste_image.resize((ch_p_image_size_width, ch_p_image_size_height))


def paste_box_creator(chess_piece, what_to_paste_image: Image):
    '''
    Create tuple (a,b,c,d) where a,b is coordinates of left upper corner
    and c,d is coordinates of right lower corner of what_to_paste_image in where_to_paste_image.
    :param chess_piece: Chess_piece object
    :param what_to_paste_image: chess_piece .png PIL image
    :return: 4-tuple (left, upper, right, lower).
    '''

    left = 50 + chess_piece.position[0] * what_to_paste_image.size[0]
    upper = 52 + (7 - chess_piece.position[1]) * what_to_paste_image.size[1]
    right = left + what_to_paste_image.size[0]
    lower = upper + what_to_paste_image.size[1]
    return (left, upper, right, lower)


class Drawer:
    def __init__(self, board):

        '''
        :param board: объект класса Board, доска с фигурами
        '''

        self.board = board.chess_pieces
        self.board_for_print_txt = [[['**'] for i in range(8)] for i in range(8)]
        self.board_for_print_png = Image.open('visual/images/chessboard.png')
        self.print_type = 'none'

    def bot_print(self):

        '''
        Make board image for user. Board image can be a string or a .png file.
        :return: board image in chosen format or request to choose format
        '''

        if self.print_type == 'text':
            print_string = ''
            for row in self.board_for_print_txt:
                for cell in row:
                    if cell is row[7]:
                        print_string = print_string + cell[0] + '\n'
                    else:
                        print_string = print_string + cell[0] + ' '
            return print_string
        elif self.print_type == 'image':
            ingame_board_image_filename = self.board_for_print_png.filename
            self.board_for_print_png = Image.open('visual/images/chessboard.png')
            return ingame_board_image_filename
        elif self.print_type == 'none':
            'Можно убрать этот пункт, если перед началом партии просить выбрать юзера формат вывода шахматной доски'
            return 'Please choose board image type: text or image'
        else:
            return f'Chosen board image type <<{self.print_type}>> is not supported. ' \
                   f'Please choose board image type: text or image'

    def make_board_for_print(self, print_type):

        '''
        Обновляет board_for_print_txt на основе позиций фигур, хранящихся в board.
        print_type = 'text' or 'image'
        '''

        'ch_p --- chess_piece'

        if print_type == 'text':
            for ch_p in self.board:
                self.board_for_print_txt[7 - ch_p.position[1]][ch_p.position[0]][0] = ch_p.color + ch_p.type
            self.print_type = 'text'
        elif print_type == 'image':
            for ch_p in self.board:
                with Image.open(f'Visual/images/wikipedia/{ch_p.color + ch_p.type}.png') as ch_p_image:
                    ch_p_image = resized_chess_piece_image(self.board_for_print_png, ch_p_image)
                    paste_box = paste_box_creator(ch_p, ch_p_image)
                    self.board_for_print_png.paste(ch_p_image, paste_box, mask=ch_p_image)
                    self.board_for_print_png.save('visual/images/ingame.png')
                self.board_for_print_png = Image.open('visual/images/ingame.png')
            self.print_type = 'image'
        else:
            self.print_type = print_type

        def cleaner(self):
            remove('visual/images/ingame.png')


class Ch_p:
    def __init__(self):
        self.color = 'w'
        self.type = 'K'
        self.position = [3, 4]
ch_p = Ch_p()
class Board():
    def __init__(self):
        self.chess_pieces = [ch_p]
board = Board()
drawer = Drawer(board)
drawer.make_board_for_print('image')
drawer.bot_print()

