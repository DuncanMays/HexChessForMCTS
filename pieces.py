import numpy as np

def OOB_filter(p):
	a, b, c = p
	return max(abs(a), abs(b), abs(c)) < 6

class Piece():

	def __init__(self):
		self.position = np.array([5, -5, 0])

		self.moves = [
			np.array([-1, 0, 1]),
			np.array([1, -1, 0]), 
			np.array([0, 1, -1])
		]

	def get_valid_moves(self, board):
		possible_moves = [self.position + move for move in self.moves]

		# filter for OOB
		possible_moves = filter(OOB_filter, possible_moves)

		# filter for on top of an enemy piece
		# filter for on top of a firendly piece

		return list(possible_moves)

if (__name__ == '__main__'):

	p = Piece()
	print(p.get_valid_moves('board'))