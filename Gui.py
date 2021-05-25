import tkinter as tk
import math
from Board import Board
from AI import AI

# Reference: the main idea of this gui is from github:TongTongX/Gomoku
class Gui_helper(tk.Canvas):
	def __init__(self, size = 15, master=None, height=0, width=0):
		self.size = size
		tk.Canvas.__init__(self, master, height=height, width=width)
		self.create_board()
		self.Board = Board(size)
		self.AI = AI(size)
		self.AI.board = self.Board.get_board()
		self.player = 2
		self.undo = False
		self.depth = 2
		self.prev_exist = False
		self.prev_row = 0
		self.prev_col = 0


	def create_board(self):
		"""
        create the Board on the canvas with [size]
        """
		#print(self.size)
		for i in range(self.size):
			start_pixel_x = (i + 1) * 30
			end_pixel_x = (i + 1) * 30
			start_pixel_y = (0 + 1) * 30
			end_pixel_y = self.size * 30
			self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)
			start_pixel_x = (0 + 1) * 30
			start_pixel_y = (i + 1) * 30
			end_pixel_x = self.size * 30
			end_pixel_y = (i + 1) * 30
			self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

		# stars 
		loc1 = self.size//2//2
		loc2 = self.size//2
		loc3 = loc2 + loc1 + 1
		self.star(loc1,loc1)
		self.star(loc3,loc1)
		self.star(loc2,loc2)
		self.star(loc1,loc3)
		self.star(loc3,loc3)


	def star(self, row, col):
		"""
		Place a star at [row, col] for reference
		"""
		start_pixel_x = (row + 1) * 30 - 2
		end_pixel_x = (row + 1) * 30 + 2
		start_pixel_y = (col + 1) * 30 - 2
		end_pixel_y = (col + 1) * 30 + 2
		self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill = 'black')


	def stone(self, row, col):
		"""
		Place a double circle from the last move on the board at [row, col]
		"""
		loc4 = self.size//2//2+1
		loc5 = self.size//2 - 1
		loc6 = loc4 + loc5
		inner_start_x = (row + 1) * 30 - loc4
		inner_start_y = (col + 1) * 30 - loc4
		inner_end_x = (row + 1) * 30 + loc4
		inner_end_y = (col + 1) * 30 + loc4

		outer_start_x = (row + 1) * 30 - loc5
		outer_start_y = (col + 1) * 30 - loc5
		outer_end_x = (row + 1) * 30 + loc5
		outer_end_y = (col + 1) * 30 + loc5

		start_pixel_x = (row + 1) * 30 - loc6
		start_pixel_y = (col + 1) * 30 - loc6
		end_pixel_x = (row + 1) * 30 + loc6
		end_pixel_y = (col + 1) * 30 + loc6
		
		if self.player == 1:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
			self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='white')
			self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='black')
		elif self.player == 2:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
			self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='black')
			self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='white')


	def prev_stone(self, row, col):
		"""
		update the stone style to a single circle from previous move at [row, col]
		"""
		loc4 = self.size//2//2+1
		loc5 = self.size//2 - 1
		loc6 = loc4 + loc5
		start_pixel_x = (row + 1) * 30 - loc6
		start_pixel_y = (col + 1) * 30 - loc6
		end_pixel_x = (row + 1) * 30 + loc6
		end_pixel_y = (col + 1) * 30 + loc6
		
		if self.player == 1:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
		elif self.player == 2:
			self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')


	def main_game(self, event):
		"""
		display the game on gui as well as on terminal
		"""
		while True:
			print('Your turn!!\n')
			self.player = 1
			invalid = True
			# check for the nearest position where the user click
			for i in range(self.size):
				for j in range(self.size):
					pixel_x = (i + 1) * 30
					pixel_y = (j + 1) * 30
					square_x = math.pow((event.x - pixel_x), 2)
					square_y = math.pow((event.y - pixel_y), 2)
					distance =  math.sqrt(square_x + square_y)
					# calculate the distance
					if (distance < self.size) and (self.Board.get_board()[i][j] == 0):
						self.stone(i, j)
						invalid = False
						if self.prev_exist == False:
							self.prev_exist = True
						else:
							self.prev_stone(self.prev_row, self.prev_col)
						self.prev_row =  i
						self.prev_col = j
						row, col = i, j
						# waiting for the AI's move
						self.unbind('<Button-1>')
						break
				else:
					continue
				break		
			
			# invalid position
			if invalid:
				print('Invalid! Please choose another position!\n')
				break
			else:
				break

		# Place a black stone after determining the position
		self.Board.get_board()[row][col] = 1

		# the player wins
		if self.Board.check_winner() == 'Black':
			print('BLACK WINS !!')
			self.create_text(240, 500, text = 'OMG! You beat the AI!')
			self.unbind('<Button-1>')
			return 0
		
		# AI's turn
		self.player = 2
		print('AI needs some time...')
		row, col = self.AI.minimax(self.player, self.depth)
		coord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))
		print('AI moves to {}\n'.format(coord))
		self.Board.get_board()[row][col] = 2
		self.stone(row,col)
		if self.prev_exist == False:
			self.prev_exist = True
		else:
			self.prev_stone(self.prev_row, self.prev_col)
		self.prev_row = row
		self.prev_col = col
		self.print_board()
		print('\n')
		self.bind('<Button-1>', self.main_game)

		# the AI wins
		if self.Board.check_winner() == 'White':
			print('The AI wins!!!')
			self.create_text(240, 500, text = 'The AI wins!!!')
			self.unbind('<Button-1>')
			return 0
	
	def print_board(self):
		print('  A B C D E F G H I J K L M N O')
		self.Board.check_winner()
		for col in range(15):
			print(chr(ord('A') + col), end=" ")
			for row in range(15):
				ch = self.Board.get_board()[row][col]
				if ch == 0:
					print('.', end=" ")
				elif ch == 1:
					print('X', end=" ")
				elif ch == 2:
					print('O', end=" ")
			print()
			

class Gui(tk.Frame):
	def __init__(self, size = 15, master = None):
		tk.Frame.__init__(self, master)
		self.size = size
		self.create_widgets()


	def create_widgets(self):
		self.boardCanvas = Gui_helper(height = 600, width = 500)
		self.boardCanvas.bind('<Button-1>', self.boardCanvas.main_game)
		self.boardCanvas.pack()

def main():
	window = tk.Tk()
	window.wm_title("GOMOKU GAME WITH AI")
	gui_board = Gui(window)
	gui_board.pack()
	window.mainloop()


if __name__ == "__main__":
	main()