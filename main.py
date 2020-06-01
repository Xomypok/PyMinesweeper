#SETTINGS--------------------------


Y_SIZE = 10 #Клеток по горизонтали

X_SIZE = 20 #Клеток по вертикали

count = 40 # Кол-во мин

#this is good
#and lol
#END_SETTINGS----------------------

from datetime import datetime
from tkinter import *
#from tkinter.ttk import *
from random import choice
from tkinter import messagebox as mb


id_counter = 0

M = X_SIZE #кол-во клеток по горизонтали
N = Y_SIZE # вертикали
bombs_count = count
mines = []
opened = []
checked = []
blocks = []
firstclick = True
play=False
start = None


def check_win():
	if not play:
		return
	if len(opened)+len(mines)==M*N:
		win()

def lose():
	global play
	play=False
	mb.showerror("lose", "this is bomb")

def win():
	global play
	play = False
	mb.showinfo(time.get(), "Perfect!")

def generate_bombs(arounds, self_id):
	global firstclick, play, start
	firstclick = False
	for i in range(bombs_count):
		while 1:
			item = choice(choice(blocks))
			if (item not in mines) and (item not in arounds) and (item != self_id):
				mines.append(item)
				break
	play=True
	start = datetime.now()
	field.timer()
		


class Block(Button):
	def __init__(self, master):
		global id_counter
		self.arounds = []
		Button.__init__(self, master, width=1, command=self.open, bg="cyan")
		self.id = id_counter
		id_counter+=1
		self.bind("<3>", self.check_as_bomb)

	def __str__(self):
		return self.id

	def open(self, rec=False):
		global firstclick
		if firstclick:
			generate_bombs(self.arounds, self)
		if not play:
			return
		if self in checked:
			return
		if self in mines:
			lose()
			return
		checked_c = 0
		for i in self.arounds:
			if i in checked:
				checked_c+=1
		if self in opened and self.count_mines_around()==checked_c:
			temp = self.arounds
			for i in temp[::]:
				if i in checked or i in opened:
					temp.remove(i)
			for i in temp:
				i.open(rec=True)
		if self in opened:
			return
		else:
			opened.append(self)
			self["bg"]="white"
			c = self.count_mines_around()
			
			if c==0:
				for i in self.arounds:
					if i not in opened:
						i.open(rec=True)
					pass
			if c==0:
				c=""
			self["text"] = "{}".format(c)
		check_win()

	def count_mines_around(self):
		c = 0
		for i in self.arounds:
			if i in mines:
				c+=1
		return c

	def check_as_bomb(self, e):
		if not play:
			return
		if self in opened:
			return
		if self in checked:
			checked.remove(self)
			self["text"] = ""
		else:
			checked.append(self)
			self["text"] = "*"
		mines_remaining.set(len(mines)-len(checked))
		check_win()

class Field(Frame):
	"""
	Это объект игры.
	поле.
	размер MxN
	bombs_count - кол-во мин
	"""
	
	def __init__(self):
		global mines_remaining, time
		mines_remaining = IntVar()
		mines_remaining.set(bombs_count)
		time = IntVar()
		time.set(0)
		display = Frame()
		display.pack(fill=X)
		Label(display, text="Мин: ").pack(side=LEFT)
		Label(display, textvariable=mines_remaining).pack(side=LEFT)
		Label(display, textvariable=time).pack(side=RIGHT)
		Label(display, text="Время:").pack(side=RIGHT)
		Button(display, text=":-)", command=self.new_game).pack(side=TOP)
		Frame.__init__(self)
		self.pack(fill=BOTH, expand=1)
		self.draw_blocks()
		self.set_arounds()

	def timer(self):
		now = datetime.now()
		delta = now-start
		time.set(delta.seconds)
		if play:
			root.after(1000, self.timer)

	def new_game(self):
		global mines, opened, checked, blocks, firstclick
		mines = []
		opened = []
		checked = []
		mines_remaining.set(bombs_count)
		for i in blocks:
			for j in i:
				j.grid_forget()
				del j
		blocks = []
		firstclick = True
		self.draw_blocks()
		self.set_arounds()


	def draw_blocks(self):
		for y in range(M):
			blocks.append([])
			for x in range(N):
				el = Block(self)
				el.grid(row=y, column=x)
				blocks[y].append(el)

	def set_arounds(self):
		for y in range(M):
			for x in range(N):
				block = blocks[y][x]
				if x>0:
					block.arounds.append(blocks[y][x-1])
					if y>0:
						block.arounds.append(blocks[y-1][x-1])
						block.arounds.append(blocks[y-1][x])
						if x<N-1:
							block.arounds.append(blocks[y-1][x+1])
				else:
					if y>0:
						block.arounds.append(blocks[y-1][x])
						if x<N-1:
							block.arounds.append(blocks[y-1][x+1])
				if x<N-1:
					block.arounds.append(blocks[y][x+1])
					if y<M-1:
						block.arounds.append(blocks[y+1][x+1])
						block.arounds.append(blocks[y+1][x])
						if x>0:
							block.arounds.append(blocks[y+1][x-1])
				else:
					if y<M-1:
						block.arounds.append(blocks[y+1][x])
						if x>0:
							block.arounds.append(blocks[y+1][x-1])
				#block["text"]=len(block.arounds)





class App(Tk):
	caption = "Minesweeper"
	#size = (400, 300)
	#offset = (400,250)
	def __init__(self):
		Tk.__init__(self)
		self.title(self.caption)
		#self.geometry("{}x{}+{}+{}".format(*self.size, *self.offset))

	def construct(self):
		global field
		#Your code here
		#Generate field of buttons
		self.field = field = Field()


def main():
	global root
	root = App()
	root.construct()
	root.mainloop()

if __name__ == '__main__':
	main()