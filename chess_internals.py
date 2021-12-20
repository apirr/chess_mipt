import copy

GLOBAL_CHESS_PIECES_MOVES = {
	'K': [[1, 1], [0, 1], [1, 0], [-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1]],
	'R': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [0, 2], [2, 0], [-2, 0], [0, -2], [0, 3], [3, 0], [-3, 0], [0, -3], [0, 4], [4, 0], [-4, 0], [0, -4], [0, 5], [5, 0], [-5, 0], [0, -5], [0, 6], [6, 0], [-6, 0], [0, -6], [0, 7], [7, 0], [-7, 0], [0, -7]],
	'B': [[1, 1], [-1, -1], [2, 2], [-2, -2], [3, 3], [-3, -3], [4, 4], [-4, -4], [5, 5], [-5, -5], [6, 6], [-6, -6], [7, 7], [-7, -7], [1, -1], [-1, 1], [2, -2], [-2, 2], [3, -3], [-3, 3], [4, -4], [-4, 4], [5, -5], [-5, 5], [6, -6], [-6, 6], [7, -7], [-7, 7]],
	'Q': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [0, 2], [2, 0], [-2, 0], [0, -2], [0, 3], [3, 0], [-3, 0], [0, -3], [0, 4], [4, 0], [-4, 0], [0, -4], [0, 5], [5, 0], [-5, 0], [0, -5], [0, 6], [6, 0], [-6, 0], [0, -6], [0, 7], [7, 0], [-7, 0], [0, -7], [1, 1], [-1, -1], [2, 2], [-2, -2], [3, 3], [-3, -3], [4, 4], [-4, -4], [5, 5], [-5, -5], [6, 6], [-6, -6], [7, 7], [-7, -7], [1, -1], [-1, 1], [2, -2], [-2, 2], [3, -3], [-3, 3], [4, -4], [-4, 4], [5, -5], [-5, 5], [6, -6], [-6, 6], [7, -7], [-7, 7]],
	'N': [[2, 1], [1, 2], [-2, -1], [-1, -2], [-1, 2], [1, -2], [2, -1], [-2, 1]],
	# 'Pw': [[0, 1], [1, 1], [-1, 1]],
	# 'Pb': [[0, -1], [-1, -1], [1, -1]]
	'Pw': [[0, 1]],
	'Pb': [[0, -1]]
}

def pr_br(brd):
	"""
	This function prints the board on input 

    Args:
        brd (Board): The board to be printed
    """
	for array in brd.chess_pieces:
		for el in array:
			print(el.type+el.color, end = ' ')
		print('\n')
	(brd.chess_pieces[1][6].can_it_go_there([1, 4]))

def sign(x):
	"""
	Calculates the sign of a variable

    Args:
        x (float): the variable.

    Returns:
        int: the sign(x) value. Is in the {-1, 0, 1} set.

    """
	if(x>0):
		return 1
	elif(x<0):
		return -1
	else:
		return 0

class Chess_piece:

	def __init__(self, type='empty', color='empty', position ='empty'):
		'''
	This is the __init__ of the chess piece

		self.dead --- bool с мертвостью фигуры
		self.have_i_moved --- то, ходила ли фигура в этой игре

    Args:
        type (string): Chess piece type. 'K', 'R', 'B', 'Q', 'N', 'P'
        color (string): Chess piece color. 'b' or 'w'
        position (tuple): the chess piece position: [x, y] 0 ≤ x ≤ 7, 0 ≤ y ≤ 7
		'''
		assert (color == 'w' or color == 'b' or color == 'empty')
		#assert (((0 <= position[0] <= 7) and (0 <= position[0] <= 7)) or position == 'empty')
		self.type = type
		self.color = color
		self.dead = False
		self.position = position
		self.have_i_moved = False

	def move_vectors(self):
		"""
	Calculates the possible move vectors. NOT FOR USE OUTSIDE THIS CODE!

    Returns:
        (tuple): the possible move vectors of a chess piece

	    """
		if self.type != "P":
			return GLOBAL_CHESS_PIECES_MOVES.get(self.type)
		else:
			return GLOBAL_CHESS_PIECES_MOVES.get(self.type + self.color)

	def is_dead(self):
		"""
	Checks if the chess_piece is dead. NOT FOR USE OUTSIDE THIS CODE!

    Returns:
        (bool): deadness of a piece

    	"""
		return self.dead  

	def is_in_bounds(self, position=None):
		"""
	Checks if a chess piece coords are in bounds. NOT FOR USE OUTSIDE THIS CODE!

    Returns:
        (bool):  is a piece out of bounds?

    	"""
		if position == None:
			position = self.position
		return ((0 <= position[0] <= 7) and (0 <= position[1] <= 7))

	def can_it_go_there(self, target_position):

		"""
	Checks if the chess_piece can go to target_position. Does not work for pawns or castling. NOT FOR USE OUTSIDE THIS FILE!

    Args:
       target_position (tuple): target position
    Returns:
    	(bool): if the chess_piece can go to target_position -- True, else -- False
    	"""

		can_it_go_there = False
		if not self.is_in_bounds(target_position):
			return False
		if self.position == 'empty':
			return False
		vector_set = self.move_vectors()
		move_vector = [target_position[0] - self.position[0],
					   target_position[1] - self.position[1]]
		for v in vector_set:
			if v == move_vector:
				can_it_go_there = True
		return can_it_go_there
	def return_a_unit_vector(self, vector):

		"""
	Returns a unit vector. NOT FOR USE OUTSIDE THIS FILE! Возвращает единичный вектор в ту сторону, в которую хочется сходить. Нужно, чтобы итеративно проверить не стоит ли кого на пути.
	Принимает на вход вектор.

    Args:
       vector (tuple): vector [a, b]
    Returns:
    	(tuple): [sign(vector[0]), sign(vector[1])]
    	"""
		if self.type == 'empty':
			return [0, 0]
		else:
			return [sign(vector[0]), sign(vector[1])]


class Board(Chess_piece):
		
	def __init__(self, white_id, game_password):
		self.chess_pieces = [[1]*8, [1]*8, [1]*8, [1]*8, [1]*8, [1]*8, [1]*8, [1]*8]
		for i in range(8):
			for j in range(8):
				self.chess_pieces[i][j] = Chess_piece()
		for i in range(8):
			self.chess_pieces[i][1] = Chess_piece('P', 'w', [int(i), 1])
			self.chess_pieces[i][6] = Chess_piece('P', 'b', [int(i), 6])
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
		self.whose_move_it_is = 'w' #меняйте после каждого успешного хода
		self.is_there_a_check_against_the_white = False
		self.is_there_a_check_against_the_black = False

	def next_move(self):
		"""Gives the move to the other side"""
		if(self.whose_move_it_is == 'w'):
			self.whose_move_it_is = 'b'
		else:
			self.whose_move_it_is = 'w'

	def is_in_bounds(self, position = [0, 0]):
		"""Checks if a position is in bounds 
		Args:
		position (tuple): position checked
		Returns:
		(bool): is it in bounds
		"""
		return ((0 <= position[0] <= 7) and (0 <= position[1] <= 7))	

	def is_this_move_pseudo_legal_without_interruptions(self, initial_position, target_position):

		"""
		NOT FOR USE OUTSIDE THIS FILE! Checks if a move vector within the allowed vectors for this piece.
		Args:
		initial_position (tuple): initial position
		target_position (tuple): target position
		Returns:
		(bool): if it is not a castling
		(string): if it is a castling and it is possible
		"""
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]

		if(moving_figure.position == 'empty'):
			return False
		# if(moving_figure.color != self.whose_move_it_is):
		# 	return False
		#if moving_figure.can_it_go_there(target_position) == False:
			#return False

		move_vector = [target_position[0] - initial_position[0], target_position[1] - initial_position[1]]

		#этот кусок кода проверяет, как может есть пешка, если ходящая фигура пешка

		if(moving_figure.type == "P" and self.chess_pieces[initial_position[0]][initial_position[1]].color == 'w' and resulting_figure.color == 'b'): 
			if ([moving_figure.position[0] + 1, moving_figure.position[1] + 1] == target_position) and (self.chess_pieces[target_position[0]][target_position[1]].position != 'empty'):
				return True
			elif ([moving_figure.position[0] - 1, moving_figure.position[1] + 1] == target_position) and (resulting_figure.position != 'empty'):
				return True
		elif(moving_figure.type == "P" and self.chess_pieces[initial_position[0]][initial_position[1]].color == 'w' and resulting_figure.color == 'empty' and move_vector == [0, 2]) and self.chess_pieces[moving_figure.position[0]][moving_figure.position[1] + 1].type == 'empty':
			return True
		elif(moving_figure.type == "P" and self.chess_pieces[initial_position[0]][initial_position[1]].color == 'b' and resulting_figure.color == 'empty' and move_vector == [0, -2]) and self.chess_pieces[moving_figure.position[0]][moving_figure.position[1] - 1].type == 'empty':
			return True				
		elif(moving_figure.type == "P" and moving_figure.color == 'b' and resulting_figure.color == 'w'):
			if ([moving_figure.position[0] + 1, moving_figure.position[1] - 1] == target_position) and (resulting_figure.position != 'empty'):
				return True
			elif ([moving_figure.position[0] - 1, moving_figure.position[1] - 1] == target_position) and (self.chess_pieces[target_position[0]][target_position[1]].position != 'empty'): # тут кончается кусок кода с проверкой на пешку
				return True			
		elif(moving_figure.type == "R" and moving_figure.have_i_moved == False and resulting_figure.type == 'K' and resulting_figure.have_i_moved == False):
			return 'Рокировка возможна'
		elif(moving_figure.type == "K" and moving_figure.have_i_moved == False and resulting_figure.type == 'R' and resulting_figure.have_i_moved == False):
			return 'Рокировка возможна'
		elif moving_figure.color == resulting_figure.color:
			return False
		else:
			return moving_figure.can_it_go_there(target_position) 

	def is_this_move_pseudo_legal_with_interruptions(self, initial_position, target_position):
		"""
		NOT FOR USE OUTSIDE THIS FILE! Checks if a move vector within the allowed vectors for this piece AND if there is standing in the way.
		Args:
		initial_position (tuple): initial position
		target_position (tuple): target position
		Returns:
		(bool): if it is not a castling
		(string): if it is a castling and it is possible
		"""
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]
		legality = self.is_this_move_pseudo_legal_without_interruptions(initial_position, target_position)

		if legality != True and legality != "Рокировка возможна":
			return legality
		else:
			if moving_figure.type == 'P' or moving_figure.type == 'N':
				return legality

		if moving_figure.type == "K" and resulting_figure.type == "R" and moving_figure.color == resulting_figure.color:
			return self.is_this_move_pseudo_legal_with_interruptions(resulting_figure.position, moving_figure.position)

		move_vector = [target_position[0] - initial_position[0], target_position[1] - initial_position[1]]
		unit_vector = [sign(copy.copy(move_vector[0])), sign(copy.copy(move_vector[1]))]
		result_vector = [move_vector[0] + unit_vector[0], move_vector[1] + unit_vector[1]] #должен получиться в результате цикла
		iterating_vector = copy.deepcopy(unit_vector)
		if legality == "Рокировка возможна":
			result_vector = copy.copy(move_vector)

		while iterating_vector != result_vector:
			print(iterating_vector, unit_vector)
			temporary_target = [initial_position[0]+iterating_vector[0], initial_position[1]+iterating_vector[1]]
			print(temporary_target)
			if self.chess_pieces[temporary_target[0]][temporary_target[1]].type != 'empty':
				return False
			if(temporary_target == target_position):
				break
			iterating_vector = [iterating_vector[0] + unit_vector[0], iterating_vector[1] + unit_vector[1]]
		return legality

		
	def pseudo_move_this_chess_piece(self, initial_position, target_position):
		"""
		NOT FOR USE OUTSIDE THIS FILE! Makes a move if it is pseudo legal. Returns stuff also.
		Args:
		initial_position (tuple): initial position
		target_position (tuple): target position
		Returns:
		(bool): if it is not a castling
		(string): if it is a castling and it is possible
		"""
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]
		is_this_move_legal = self.is_this_move_pseudo_legal_with_interruptions(initial_position, target_position)
		if is_this_move_legal != True and is_this_move_legal != "Рокировка возможна":
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
		"""
		Checks if a check is present after the following move.
		Args:
		initial_position (tuple): initial position
		target_position (tuple): target position
		Returns:
		(tuple): [check_against_the_white, check_against_the_black]
		"""
		check_against_the_white = False
		check_against_the_black = False
		backup = copy.deepcopy(self.chess_pieces)
		# for rows in backup:
		# 	for el in rows:
		# 		print(el.type, end = ' ')
		# 	print('\n')

		if self.is_this_move_pseudo_legal_with_interruptions(initial_position, target_position)!=True:
			return 'This move you are trying to make is not possible'
		self.pseudo_move_this_chess_piece(initial_position, target_position)
		white_king = Chess_piece()
		black_king = Chess_piece()
		for arrays in self.chess_pieces:
			for el in arrays:
				if el.type == 'K' and el.color == 'w':
					white_king = el
				elif el.type == 'K' and el.color == 'b':
					black_king = el
		for arrays in self.chess_pieces:
			for el in arrays:
				if el.color == 'w' and self.is_this_move_pseudo_legal_with_interruptions(el.position, black_king.position) == True:
					check_against_the_black = True
				if el.color == 'b' and self.is_this_move_pseudo_legal_with_interruptions(el.position, white_king.position) == True:
					check_against_the_white = True
		self.chess_pieces = backup
		return [check_against_the_white, check_against_the_black]


	def is_this_move_legal(self, initial_position, target_position):
		"""
		Checks if a move is legal.
		Args:
		initial_position (tuple): initial position
		target_position (tuple): target position
		Returns:
		(bool): if there is not problem
		(string): if there is a problem
		"""
		moving_figure = self.chess_pieces[initial_position[0]][initial_position[1]]
		resulting_figure = self.chess_pieces[target_position[0]][target_position[1]]

		legality = self.is_this_move_pseudo_legal_with_interruptions(initial_position, target_position)
		check = self.is_it_a_check(initial_position, target_position)
		# check = [False, False]
		if moving_figure.color == 'w':
			check = check[0]
		else:
			check = check[1]
		if resulting_figure.type == "K" and (moving_figure.color != resulting_figure.color or moving_figure.type != "R"):
			return "Нельзя есть короля."
		if check == True:
			return "Под шахом следующий ход должен снимать шах. Есть три попытки выйти из-под шаха. После этого объявляется мат."
		if legality != True and legality != "Рокировка возможна":
			return "Так нельзя ходить."
		else:
		 return True

	def move_this_chess_piece(self, initial_position, target_position):
		"""
		Makes a move if it is legal. Returns stuff also. Also gives the move to the other side if successful.
		Args:
		initial_position (tuple): initial position
		target_position (tuple): target position
		Returns:
		(bool): legality of a move
		"""
		legality = self.is_this_move_legal(initial_position, target_position)
		if legality != True:
			return False
		else:
			self.pseudo_move_this_chess_piece(initial_position, target_position)
			self.next_move()
			return True