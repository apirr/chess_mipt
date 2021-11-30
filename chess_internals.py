GLOBAL_CHESS_PIECES_MOVES = {
    'K': [[1, 1], [0, 1], [1, 0], [-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1]],
    'R': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [0, 2], [2, 0], [-2, 0], [0, -2], [0, 3], [3, 0], [-3, 0], [0, -3], [0, 4], [4, 0], [-4, 0], [0, -4], [0, 5], [5, 0], [-5, 0], [0, -5], [0, 6], [6, 0], [-6, 0], [0, -6], [0, 7], [7, 0], [-7, 0], [0, -7]],
    'B': [[1, 1], [-1, -1], [2, 2], [-2, -2], [3, 3], [-3, -3], [4, 4], [-4, -4], [5, 5], [-5, -5], [6, 6], [-6, -6], [7, 7], [-7, -7], [1, -1], [-1, 1], [2, -2], [-2, 2], [3, -3], [-3, 3], [4, -4], [-4, 4], [5, -5], [-5, 5], [6, -6], [-6, 6], [7, -7], [-7, 7]],
    'Q': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [0, 2], [2, 0], [-2, 0], [0, -2], [0, 3], [3, 0], [-3, 0], [0, -3], [0, 4], [4, 0], [-4, 0], [0, -4], [0, 5], [5, 0], [-5, 0], [0, -5], [0, 6], [6, 0], [-6, 0], [0, -6], [0, 7], [7, 0], [-7, 0], [0, -7], [1, 1], [-1, -1], [2, 2], [-2, -2], [3, 3], [-3, -3], [4, 4], [-4, -4], [5, 5], [-5, -5], [6, 6], [-6, -6], [7, 7], [-7, -7], [1, -1], [-1, 1], [2, -2], [-2, 2], [3, -3], [-3, 3], [4, -4], [-4, 4], [5, -5], [-5, 5], [6, -6], [-6, 6], [7, -7], [-7, 7]],
    'N': [[2, 1], [1, 2], [-2, -1], [-1, -2], [-1, 2], [1, -2]],
    'P': [[0, 1], [1, 1], [-1, 1]]
}

class Chess_piece():
	'''
	МЕТОДЫ
	
	move_vectors
	is_dead
	is_in_bounds
	can_it_go_there

	'''

    def __init__(self, type, color, position):
        '''
        ПОЛЯ

        self.type --- строка с типом фигуры. 'K', 'R', 'B', 'Q', 'N', 'P'
        self.color --- строка с цветом фигуры 'b', 'w'
        self.dead --- bool с мертвостью фигуры
        self.position --- tuple с двумя числами от 0 до 7
        '''
        assert (color == 'w' or color == 'b')
        assert ((0 <= position[0] <= 7) and (0 <= position[0] <= 7))
        self.type = type
        self.color = color
        self.dead = False
        self.position = postion

    def move_vectors(self):
    	'''
    	Возвращает возможные векторы перемещения для этой фигуры (принципиально возможные)
    	'''
        return GLOBAL_CHESS_PIECES_MOVES.get(self.type)

    def is_dead(self):
        return self.dead

    def is_in_bounds(position=self.position):
        return ((0 <= position[0] <= 7) and (0 <= position[0] <= 7))

    def can_it_go_there(self, target_coordinate):
        # НЕ РАБОТАЕТ ДЛЯ ПЕШЕК. РОКИРОВКИ ТОЖЕ НЕ ТУТ
        assert self.type != 'P'
        can_it_go_there = False
        if not self.is_in_bounds(target_coordinate):
            return False
        vector_set = self.move_vectors()

        move_vector = [target_coordinate[0] - self.position[0],
                       target_coordinate[1] - self.position[1]]
        for v in vector_set:
            if v == move_vector:
                can_it_go_there = True
        return can_it_go_there

def Board(Chess_piece):
	def __init__(self):
		self.chess_pieces























