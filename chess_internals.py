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
		#assert (((0 <= position[0] <= 7) and (0 <= position[0] <= 7)) or position == 'empty')
		self.type = type
		self.color = color
		self.dead = False
		self.position = position
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
		# assert self.type != 'P'
		can_it_go_there = False
		if not self.is_in_bounds(target_position):
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
	def __init__(self, white_id, game_password):
		self.chess_pieces = [[1]*8, [1]*8, [1]*8, [1]*8, [1]*8, [1]*8, [1]*8, [1]*8]
		for i in range(8):
			for j in range(8):
				self.chess_pieces[i][j] = Chess_piece()
		for i in range(8):
			self.chess_pieces[i][1] = Chess_piece('P', 'w', [i, 1])
			self.chess_pieces[i][6] = Chess_piece('P', 'b', [i, 6])
		self.chess_pieces[0][0] = Chess_piece('R', 'w', [0, 0])
		self.chess_pieces[1][0] = Chess_piece('N', 'w', [1, 0])
		self.chess_pieces[2][0] = Chess_piece('B', 'w', [2, 0])
		self.chess_pieces[3][0] = Chess_piece('Q', 'w', [3, 0])
		self.chess_pieces[4][0] = Chess_piece('K', 'w', [4, 0])
		self.chess_pieces[5][0] = Chess_piece('B', 'w', [5, 0])
		self.chess_pieces[6][0] = Chess_piece('N', 'w', [6, 0])
		self.chess_pieces[7][0] = Chess_piece('R', 'w', [7, 0])
		self.chess_pieces[0][7] = Chess_piece('R', 'b', [0, 7])
		self.chess_pieces[1][7] = Chess_piece('N', 'b', [1, 7])
		self.chess_pieces[2][7] = Chess_piece('B', 'b', [2, 7])
		self.chess_pieces[3][7] = Chess_piece('Q', 'b', [3, 7])
		self.chess_pieces[4][7] = Chess_piece('K', 'b', [4, 7])
		self.chess_pieces[5][7] = Chess_piece('B', 'b', [5, 7])
		self.chess_pieces[6][7] = Chess_piece('N', 'b', [6, 7])
		self.chess_pieces[7][7] = Chess_piece('R', 'b', [7, 7])
		self.black_id = 'black'
		self.white_id = white_id
		self.game_password = game_password
		self.whose_move_it_is = 'white' #меняйте после каждого успешного хода
		self.is_there_a_check_against_the_white = False
		self.is_there_a_check_against_the_black = False

	def is_in_bounds(self, position=None):
		return ((0 <= position[0] <= 7) and (0 <= position[1] <= 7))	

	def is_this_move_pseudo_legal_without_interruptions(self, initial_position, target_position):
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]

		if(moving_figure.position == 'empty'):
			return False
		#if moving_figure.can_it_go_there(target_position) == False:
			#return False

		move_vector = [target_position[0] - initial_position[0], target_position[1] - initial_position[1]]

		#этот кусок кода проверяет, как может есть пешка, если ходящая фигура пешка

		if(moving_figure.type == "P" and self.chess_pieces[initial_position[0]][initial_position[1]].color == 'w' and resulting_figure.color == 'b'): 
			if ([moving_figure.position[0] + 1, moving_figure.position[1] + 1] == target_position) and (self.chess_pieces[target_position[0]][target_position[1]].position != 'empty'):
				return True
			elif ([moving_figure.position[0] - 1, moving_figure.position[1] + 1] == target_position) and (resulting_figure.position != 'empty'):
				return True
		elif(moving_figure.type == "P" and self.chess_pieces[initial_position[0]][initial_position[1]].color == 'w' and resulting_figure.color == 'empty' and move_vector == [0, 2]):
			return True
		elif(moving_figure.type == "P" and self.chess_pieces[initial_position[0]][initial_position[1]].color == 'b' and resulting_figure.color == 'empty' and move_vector == [0, -2]):
			return True				
		elif(moving_figure.type == "P" and moving_figure.color == 'b' and resulting_figure.color == 'w'):
			if ([moving_figure.position[0] + 1, moving_figure.position[1] - 1] == target_position) and (resulting_figure.position != 'empty'):
				return True
			elif ([moving_figure.position[0] - 1, moving_figure.position[1] - 1] == target_position) and (self.chess_pieces[target_position[0]][target_position[1]].position != 'empty'): # тут кончается кусок кода с проверкой на пешку
				return True			
		elif(moving_figure.type == "R" and moving_figure.have_i_moved == False and resulting_figure.type == 'K' and resulting_figure.have_i_moved == False):
			return 'Рокировка возможна'
		elif moving_figure.color == resulting_figure.color:
			return False
		else:
			return moving_figure.can_it_go_there(target_position) 

	def is_this_move_pseudo_legal_with_interruptions(self, initial_position, target_position):
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]
		move_vector = [target_position[0] - initial_position[0], target_position[1] - initial_position[1]]
		legality = self.is_this_move_pseudo_legal_without_interruptions(initial_position, target_position)
		if legality != True:
			return legality
		else:
			if moving_figure.type == 'P' or moving_figure.type == 'N':
				return legality
			unit_vector = moving_figure.return_a_unit_vector(move_vector)
			print(unit_vector)
			iterating_vector = unit_vector
		# кусок кода далее проверяет, можно ли так походить, проверяя можно ли так походить на каждую клетку по прямой соединяющей начальную и конечную точки
			while(iterating_vector != move_vector and (abs(iterating_vector[0])+abs(iterating_vector[1]) < 200)): #второе условие на всякий случай -- если вдруг все пойдет неправильно чтобы цикл не стал бесконечным 
				temporary_target_position = [initial_position[0] + iterating_vector[0], initial_position[1] + iterating_vector[1]]
				if self.chess_pieces[temporary_target_position[0]][temporary_target_position[1]].type != 'empty':
					return False
				else:
					iterating_vector = [iterating_vector[0] + unit_vector[0], iterating_vector[1] + unit_vector[1]]
			return legality

		
	def pseudo_move_this_chess_piece(self, initial_position, target_position):
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]
		is_this_move_legal = self.is_this_move_pseudo_legal_with_interruptions(initial_position, target_position)
		if is_this_move_legal != True:
			return False
		elif is_this_move_legal == 'Рокировка возможна':
			moving_figure, resulting_figure = resulting_figure, moving_figure
			moving_figure.position = target_position
			resulting_figure.position = initial_position
			self.chess_pieces[initial_position[0]][initial_position[1]] = moving_figure
			self.chess_pieces[target_position[0]][target_position[1]] = resulting_figure

		elif is_this_move_legal == True:
			moving_figure.position = target_position
			resulting_figure = Chess_piece()
			self.chess_pieces[initial_position[0]][initial_position[1]] = Chess_piece()
			self.chess_pieces[target_position[0]][target_position[1]] = moving_figure

	def is_it_a_check(self, initial_position, target_position):
		check_against_the_white = False
		check_against_the_black = False
		backup = self.chess_pieces
		if self.is_this_move_pseudo_legal_with_interruptions(initial_position, target_position)!=True:
			return 'This move you are trying to make is not possible'
		move = self.pseudo_move_this_chess_piece(initial_position, target_position)
		white_king = Chess_piece()
		black_king = Chess_piece()
		for arrays in self.chess_pieces:
			for el in arrays:
				if el.type == 'K' and el.color == 'w':
					white_king = el
				elif el.type == 'K' and el.color == 'b':
					black_king = el
		if self.whose_move_it_is == 'white':
			for arrays in self.chess_pieces:
				for el in arrays:
					if el.color == 'w' and self.is_this_move_pseudo_legal_with_interruptions(el.position, black_king.position) == True:
						check_against_the_black = True
						print(el.position, 'AGAINSTBLACK')
					if el.color == 'b' and self.is_this_move_pseudo_legal_with_interruptions(el.position, white_king.position) == True:
						check_against_the_white = True
						print(el.position, 'AGAINSTW')
		self.chess_pieces = backup
		return [check_against_the_white, check_against_the_black]


	def is_this_move_legal(self, initial_position, target_position):
		legality = self.is_this_move_pseudo_legal_with_interruptions(initial_position, target_position)
		check = self.is_it_a_check(initial_position, target_position)
		check = [False, False]
		if self.whose_move_it_is == 'white':
			check = check[0]
		else:
			check = check[1]
		if self.chess_pieces[target_position[0]][target_position[1]].type == "K":
			return "Нельзя есть короля."
		if check == True:
			return "Под шахом следующий ход должен снимать шах. Есть три попытки выйти из-под шаха. После этого объявляется мат."
		if legality != True:
			return "Так нельзя ходить."
		else:
		 return True

	def move_this_chess_piece(self, initial_position, target_position):
		legality = self.is_this_move_legal(initial_position, target_position)
		if legality != True:
			return False
		else:
			self.pseudo_move_this_chess_piece(initial_position, target_position)
			if self.whose_move_it_is == 'white':
				self.whose_move_it_is = 'black'
			else:
				self.whose_move_it_is = 'white'
			return True


brd = Board('oieef', 'uinfui')

print(brd.is_this_move_legal([0, 0], [0,1]))






















