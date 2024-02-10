
class Board():

	def __init__(self):
		self.pieces = {}

	def add_piece(self, piece):
		position = piece.position.tobytes()
		self.pieces[position] = piece

	def remove_piece(self, piece):
		position = piece.position.tobytes()

		if not position in self.pieces:
			return

		del self.pieces[position]