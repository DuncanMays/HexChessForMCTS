import tkinter as tk
import math
from itertools import product

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

def draw_hex_board(canvas):

	centrex = 250
	centrey = 250
	tile_radius = 25
	n=5

	hex_dims = list(range(-n, n+1))
	hex_coords = product(hex_dims, hex_dims, hex_dims)
	hex_coords = list(filter(lambda tup : sum(tup)==0, hex_coords))

	cardinal_directions = [(1/2, -math.sqrt(3)/2), (-1, 0), (1/2, math.sqrt(3)/2)]
	cart_coords = []

	for hex_tile in hex_coords:
		cart_tile = [centrex, centrey]

		for d in range(0, 3):
			direction = cardinal_directions[d]
			scalar =tile_radius*hex_tile[d]

			cart_tile[0] += scalar*direction[0]
			cart_tile[1] += scalar*direction[1]

		cart_coords.append(cart_tile)

	for i in range(len(cart_coords)):
		tup = hex_coords[i]
		(x, y) = cart_coords[i]

		colours = ['red', 'white', 'black']
		s = sum([tup[i]*(i+1) for i in range(len(tup))])%3
		colour = colours[s]

		verts = get_hexagon_points(tile_radius, x, y)
		canvas.create_polygon(*verts, fill=colour, outline='black')

def main():
	window = tk.Tk()

	window.geometry('800x500')
	window.title('HexChess')

	buttonframe = tk.Frame(window)
	buttonframe.columnconfigure(0, weight=1)
	buttonframe.columnconfigure(1, weight=1)
	buttonframe.columnconfigure(2, weight=1)

	label = tk.Label(buttonframe, text='hello world', font=('Areal', 18))
	label.grid(row=0, column=0, sticky=tk.W+tk.E)
	label = tk.Label(buttonframe, text='hello world', font=('Areal', 18))
	label.grid(row=1, column=0, sticky=tk.W+tk.E)
	label = tk.Label(buttonframe, text='hello world', font=('Areal', 18))
	label.grid(row=2, column=0, sticky=tk.W+tk.E)

	buttonframe.pack(padx=30, side='left')

	canvas = tk.Canvas(width=500, height=500, bd=5, bg='white')
	canvas.pack(padx=30, side='left')

	draw_hex_board(canvas)
	# draw_hex_board_0(canvas)

	window.mainloop()

if __name__ == '__main__':
	main()