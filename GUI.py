import tkinter as tk
import math
from itertools import product
import numpy as np
from time import sleep

# returns a list of six tuples representing the coordinates of the corners of a hexagon centred at (x, y)
def get_hexagon_points(radius, x, y):

	pts = []
	rt = math.sqrt(3)/2

	pts.append((x+radius, y))
	pts.append((x+0.5*radius, y-rt*radius))
	pts.append((x-0.5*radius, y-rt*radius))
	pts.append((x-radius, y))
	pts.append((x-0.5*radius, y+rt*radius))
	pts.append((x+0.5*radius, y+rt*radius))

	return pts

class HexChessCanvas():

	def __init__(self, canvas, height=500, width=500, tile_radius=25, n=5):
		self.canvas = canvas
		self.centrex = height/2
		self.centrey = width/2
		self.centre = np.array([width/2, height/2])
		self.tile_radius = tile_radius
		self.n = n
		self.selected_tile = None

		# here we create a set of 3D coordinates to represent hexagonal space
		axis = list(range(-n, n+1))
		all_pts = product(axis, axis, axis)
		# this list represents the index of every tile on the board in hex coordinates
		self.tile_coords = list(filter(lambda tup : sum(tup)==0, all_pts))

		# the basis vectors for our hexagonal coordinate system
		self.htc_matrix = self.tile_radius*np.array([[1/2, -1, 1/2], [-math.sqrt(3)/2, 0, math.sqrt(3)/2], [1, 1, 1]])
		self.cth_matrix = np.linalg.inv(self.htc_matrix)

		# binds the onclick method to the right mouse button
		canvas.bind("<Button-1>", self.onclick)

		self.draw()

	# flips the y-component of basis vectors so that the screen is draw upside-down
	def flip(self):
		self.htc_matrix = self.htc_matrix*[[1], [-1], [1]]
		self.cth_matrix = np.linalg.inv(self.htc_matrix)

	# translates from hex coordinates on the board to cartesian coordinates on the canvas
	def hex_to_cart(self, hex_v):
		hex_v = np.array(hex_v)
		cart_v = np.matmul(self.htc_matrix, hex_v)[0:2]
		return cart_v + self.centre

	# translates from cartesian coordinates on the canvas to hex coordinates on the board
	def cart_to_hex(self, cart_v):
		cart_v = np.array(cart_v) - self.centre
		cart_v = np.concatenate([cart_v, np.array([0])], 0)
		return np.matmul(self.cth_matrix, cart_v)

	def onclick(self, event):
		# here we represent the click coordinates in hex coords
		x, y = event.x, event.y
		(a, b, c) = self.cart_to_hex([x, y])

		# round the click location to the nearest hexagon tile
		a, b, c = round(a), round(b), round(c)

		self.selected_tile = None

		# does not acknowledge clicks that are out of bounds or that are on the corners of tiles
		if (max([abs(a), abs(b), abs(c)]) < self.n+1) and (sum([a, b, c]) == 0): 
			self.selected_tile = (a, b, c)

		self.draw()

	def draw(self):

		# wipes the screen
		self.canvas.delete('all')

		# iterate over each of the coordinates on the board and draw a hexagon there
		for hex_tile in self.tile_coords:
			# translating the coordinates of the tile from hex coordinates to cartesian coordinates
			x, y = self.hex_to_cart(hex_tile)

			# this ensures the tile colours alternate between red, white and black correctly
			colours = ['red', 'white', 'black']
			s = sum([hex_tile[i]*(i+1) for i in range(len(hex_tile))])%3
			colour = colours[s]

			# draw the tile as a hexagon
			verts = get_hexagon_points(self.tile_radius, x, y)
			self.canvas.create_polygon(*verts, fill=colour, outline='black')

		# draw a yellow hexagon if there's a tile selected
		if (self.selected_tile != None):
			# draw a yellow hexagon on the selected tile
			x, y = self.hex_to_cart(self.selected_tile)
			verts = get_hexagon_points(self.tile_radius, x, y)
			self.canvas.create_polygon(*verts, fill='yellow', outline='black')

def main():
	window = tk.Tk()

	window.geometry('800x500')
	window.title('HexChess')

	buttonframe = tk.Frame(window)
	buttonframe.columnconfigure(0, weight=1)
	buttonframe.columnconfigure(1, weight=1)
	buttonframe.columnconfigure(2, weight=1)

	canvas = tk.Canvas(width=500, height=500, bd=5, bg='white')
	vc = HexChessCanvas(canvas)

	label = tk.Label(buttonframe, text='hello world', font=('Areal', 18))
	label.grid(row=0, column=0, sticky=tk.W+tk.E)
	label = tk.Label(buttonframe, text='hello world', font=('Areal', 18))
	label.grid(row=1, column=0, sticky=tk.W+tk.E)

	def onclick_flip_button():
		vc.flip()
		vc.draw()

	flip_button = tk.Button(buttonframe, text='flip', font=('Areal', 18), command=onclick_flip_button)
	flip_button.grid(row=2, column=0, sticky=tk.W+tk.E)

	buttonframe.pack(padx=30, side='left')
	canvas.pack(padx=30, side='left')

	window.mainloop()

if __name__ == '__main__':
	main()