from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def resized_chess_piece_image(where_to_paste_image: Image, what_to_paste_image: Image):
    """Change chess_piece image size so it fits board image size.
    :param where_to_paste_image: board .png PIL image
    :param what_to_paste_image: chess_piece .png PIL image
    :return: resized chess_piece .png PIL image"""

    ch_p_image_size_width = (where_to_paste_image.size[0] - 100) // 8
    ch_p_image_size_height = (where_to_paste_image.size[1] - 103) // 8
    return what_to_paste_image.resize((ch_p_image_size_width, ch_p_image_size_height))


def paste_box_creator(chess_piece, what_to_paste_image: Image):
    """Create tuple (a,b,c,d) where a,b is coordinates of left upper corner
    and c,d is coordinates of right lower corner of what_to_paste_image in where_to_paste_image.
    :param chess_piece: Chess_piece object
    :param what_to_paste_image: chess_piece .png PIL image
    :return: 4-tuple (left, upper, right, lower)."""

    left = 50 + chess_piece.position[0] * what_to_paste_image.size[0]
    upper = 52 + (7 - chess_piece.position[1]) * what_to_paste_image.size[1]
    right = left + what_to_paste_image.size[0]
    lower = upper + what_to_paste_image.size[1]
    return (left, upper, right, lower)


class Drawer:
    def __init__(self, board):
        """:param board: объект класса Board, доска с фигурами"""

        self.board = board.chess_pieces
        self.board_for_print_png = Image.open('visual/images/chessboard.png')

    def bot_print(self):
        """Make board image for user.
        :return: board image"""
        ingame_board_image_filename = self.board_for_print_png.filename
        self.board_for_print_png = Image.open('visual/images/chessboard.png')
        return ingame_board_image_filename

    def make_board_for_print(self):
        """Обновляет board_for_print_png на основе позиций фигур, хранящихся в board."""

        'ch_p --- chess_piece'
        for row in self.board:
            for ch_p in row:
                if ch_p.type != 'empty' and not ch_p.dead:
                    with Image.open(f'Visual/images/wikipedia/{ch_p.color + ch_p.type}.png') as ch_p_image:
                        ch_p_image = resized_chess_piece_image(self.board_for_print_png, ch_p_image)
                        paste_box = paste_box_creator(ch_p, ch_p_image)
                        self.board_for_print_png.paste(ch_p_image, paste_box, mask=ch_p_image)
                        self.board_for_print_png.save('visual/images/ingame.png')
                    self.board_for_print_png = Image.open('visual/images/ingame.png')
