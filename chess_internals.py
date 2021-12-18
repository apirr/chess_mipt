GLOBAL_CHESS_PIECES_MOVES = {
	'K': [[1, 1], [0, 1], [1, 0], [-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1]],
	'R': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [0, 2], [2, 0], [-2, 0], [0, -2], [0, 3], [3, 0], [-3, 0], [0, -3], [0, 4], [4, 0], [-4, 0], [0, -4], [0, 5], [5, 0], [-5, 0], [0, -5], [0, 6], [6, 0], [-6, 0], [0, -6], [0, 7], [7, 0], [-7, 0], [0, -7]],
	'B': [[1, 1], [-1, -1], [2, 2], [-2, -2], [3, 3], [-3, -3], [4, 4], [-4, -4], [5, 5], [-5, -5], [6, 6], [-6, -6], [7, 7], [-7, -7], [1, -1], [-1, 1], [2, -2], [-2, 2], [3, -3], [-3, 3], [4, -4], [-4, 4], [5, -5], [-5, 5], [6, -6], [-6, 6], [7, -7], [-7, 7]],
	'Q': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [0, 2], [2, 0], [-2, 0], [0, -2], [0, 3], [3, 0], [-3, 0], [0, -3], [0, 4], [4, 0], [-4, 0], [0, -4], [0, 5], [5, 0], [-5, 0], [0, -5], [0, 6], [6, 0], [-6, 0], [0, -6], [0, 7], [7, 0], [-7, 0], [0, -7], [1, 1], [-1, -1], [2, 2], [-2, -2], [3, 3], [-3, -3], [4, 4], [-4, -4], [5, 5], [-5, -5], [6, 6], [-6, -6], [7, 7], [-7, -7], [1, -1], [-1, 1], [2, -2], [-2, 2], [3, -3], [-3, 3], [4, -4], [-4, 4], [5, -5], [-5, 5], [6, -6], [-6, 6], [7, -7], [-7, 7]],
	'N': [[2, 1], [1, 2], [-2, -1], [-1, -2], [-1, 2], [1, -2]],
	'P': [[0, 1], [1, 1], [-1, 1]]
}

def sign(x):
	if(x>0):
		return 1
	elif(x<0):
		return -1
	else:
		return 0

class Chess_piece:
	'''
	МЕТОДЫ
	
	move_vectors
	is_dead
	is_in_bounds
	can_it_go_there

	'''

	def __init__(self, type='empty', color='empty', position ='empty'):
		'''
		ПОЛЯ

		self.type --- строка с типом фигуры. 'K', 'R', 'B', 'Q', 'N', 'P'
		self.color --- строка с цветом фигуры 'b', 'w'
		self.dead --- bool с мертвостью фигуры
		self.position --- tuple с двумя числами от 0 до 7
		self.have_i_moved --- то, ходила ли фигура в этой игре
		'''
		assert (color == 'w' or color == 'b' or color == 'empty')
		assert (((0 <= position[0] <= 7) and (0 <= position[0] <= 7)) or position == empty)
		self.type = type
		self.color = color
		self.dead = False
		self.position = postion
		self.have_i_moved = False

	def move_vectors(self):
		'''
		Возвращает возможные векторы перемещения для этой фигуры (принципиально возможные)
		'''
		return GLOBAL_CHESS_PIECES_MOVES.get(self.type)

	def is_dead(self):
		return self.dead  

	def is_in_bounds(self, position=None):
		if position == None:
			position = self.position
		return ((0 <= position[0] <= 7) and (0 <= position[1] <= 7))

	def can_it_go_there(self, target_position):
		# НЕ РАБОТАЕТ ДЛЯ ПЕШЕК. РОКИРОВКИ ТОЖЕ НЕ ТУТ проверяет находится ли точка на которую хотим сходить. 
		# НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ ЭТОТ МЕТОД ЕСЛИ ВЫ НЕ ПОНИМАЕТЕ ЧТО ТВОРИТЕ С ЭТИМ МЕТОДОМ. ИСПОЛЬЗУЙТЕ МЕТОД В КЛАССЕ BOARD
		assert self.type != 'P'
		can_it_go_there = False
		if not self.is_in_bounds(target_coordinate):
			return False
		vector_set = self.move_vectors()

		move_vector = [target_position[0] - self.position[0],
					   target_position[1] - self.position[1]]
		for v in vector_set:
			if v == move_vector:
				can_it_go_there = True
		return can_it_go_there
	def return_a_unit_vector(self, vector):
		'''Возвращает единичный вектор в ту сторону, в которую хочется сходить. Нужно, чтобы итеративно проверить не стоит ли кого на пути. Принимает на вход вектор.'''
		if self.type == 'empty':
			return [0, 0]
		else:
			return [sign(vector[0]), sign(vector[1])]


class Board(Chess_piece):
	'''
	METHODS:

	The only methods to be used by an end user of this code are:

	is_this_move_legal(self, initial_position, target_position)  checks the legality of a move

	move_this_chess_piece(self, initial_position, target_position) makes the move if it is legal and returns False otherwise

	def checkmate(self, initial_position, target_position)

	'''
	def __init__(self):
		self.chess_pieces = [Сhess_piece() for i in range(7)]*8
		black_id = 'black'
		white_id = 'white'
		#game_id = 'this may not be required' #может быть не надо в зависимости от того как будете реализовывать
		whose_move_it_is = 'white' #меняйте после каждого успешного хода
		print(self.chess_pieces)

	def is_in_bounds(self, position=None):
		return ((0 <= position[0] <= 7) and (0 <= position[1] <= 7))	

	def is_this_move_pseudo_legal_without_interruptions(self, initial_position, target_position):
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]

		if(moving_figure.position == 'empty'):
			return False
		if self.moving_figure.can_it_go_there(target_position) == False:
			return False

		move_vector = [target_position[0] - self.position[0], target_position[1] - self.position[1]]

		#этот кусок кода проверяет, как может есть пешка, если ходящая фигура пешка

		if(moving_figure.type == "p" and self.chess_pieces[initial_position].color == 'w' and resulting_figure.color == 'b'): 
			if ([moving_figure.position + 1, moving_figure.position + 1] == target_position) and (self.chess_pieces[target_position[0]][target_position[1]].position != 'empty'):
				return True
			elif ([moving_figure.position - 1, moving_figure.position + 1] == target_position) and (resulting_figure.position != 'empty'):
				return True			
		elif(moving_figure.type == "p" and moving_figure.color == 'b' and resulting_figure.color == 'w'):
			if ([moving_figure.position + 1, moving_figure.position - 1] == target_position) and (resulting_figure.position != 'empty'):
				return True
			elif ([moving_figure.position - 1, moving_figure.position - 1] == target_position) and (self.chess_pieces[target_position[0]][target_position[1]].position != 'empty'): # тут кончается кусок кода с проверкой на пешку
				return True			
		elif(moving_figure.type == "r" and moving_figure.have_i_moved == False and resulting_figure.type == 'k' and resulting_figure.have_i_moved == False):
			return 'Рокировка возможна'
		else:
			return moving_figure.can_it_go_there[target_position]

	def is_this_move_pseudo_legal_with_interruptions(self, initial_position, target_position):
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]
		move_vector = [target_position[0] - self.position[0], target_position[1] - self.position[1]]
		legality = self.is_this_move_pseudo_legal_without_interruptions(initial_position, target_position)
		if legality == False:
			return legality
		else:
			if moving_figure.type == 'P' or moving_figure.type == 'N':
				return legality
			unit_vector = moving_figure.return_a_unit_vector(move_vector)
			iterating_vector = unit_vector
		# кусок кода далее проверяет, можно ли так походить, проверяя можно ли так походить на каждую клетку по прямой соединяющей начальную и конечную точки
			while(iterating_vector != unit_vector and (abs(iterating_vector[0])+abs(iterating_vector[1]) < 200)): #второе условие на всякий случай -- если вдруг все пойдет неправильно 
				temporary_target_position = [initial_position[0] + iterating_vector[0], initial_position[1] + iterating_vector[1]]
				if self.is_this_move_pseudo_legal_without_interruptions(initial_position, temporary_target_position) == False:
					return False
				else:
					iterating_vector = [iterating_vector[0] + unit_vector[0], iterating_vector[1] + unit_vector[1]]
			return legality
	def checkmate():
		#FIXME

	def is_this_move_legal(self, initial_position, target_position):
		#FIXME Эта функция будет работать когда появится распознание шахов (и матов)
		return True
		
	def move_this_chess_piece(self, initial_position, target_position):
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]
		is_this_move_legal = self.is_this_move_legal(initial_position, target_position)
		if is_this_move_legal == False:
			return False
		elif is_this_move_legal == 'Рокировка возможна':
			moving_figure, resulting_figure = resulting_figure, moving_figure
			moving_figure.position = target_position
			resulting_figure.position = initial_position
		elif is_this_move_legal == True:
			moving_figure, resulting_figure = resulting_figure, moving_figure
			moving_figure.position = target_position
			resulting_figure = Chess_piece()























