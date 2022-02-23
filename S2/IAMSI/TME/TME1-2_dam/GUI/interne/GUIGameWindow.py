import tkinter as tk
from tkinter import ttk
from .constants import *
import tkinter.font as tkFont
from functools import partial


class GameWindow(tk.Tk):
	def __init__(self, ref_table: list, ref_score: dict, human: int, controller):
		super().__init__()
		print(human)
		self.table = ref_table
		self.score = ref_score
		self.human = human
		self.controller = controller
		self.last_move = 0

		self.btn_font = tkFont.Font(self, family="Courier", size=12)
		self.title(TITLE)
		self.resizable(False, False)
		self.create_widgets()

	def button_press(self, idx: int):
		self.last_move = 1 + (idx % TAILLE)
		self.controller.jouer_humain(self.last_move)
		self.update_state()
		self.after(1000, self.controller.jouer_cpu)

	def create_widgets(self):
		style = ttk.Style(self)
		style.configure("TLabel", font=("Courier", 14, "bold"))

		self.label_n = ttk.Label()
		self.label_n.grid(column=0, row=0, columnspan=TAILLE, sticky='ew')

		b = []
		for i in range(TAILLE * 2):
			button = tk.Button(self, text=str(i), command=partial(self.button_press, i))
			button.configure(font=self.btn_font, width=7)
			button.grid(column=i%TAILLE, row=(2 + (i//TAILLE)), sticky='ew')
			b.append(button)
		self.buttons_n = b[:TAILLE]
		self.buttons_s = b[TAILLE:]

		for i in range(TAILLE):
			label = ttk.Label(text=str(1+i), anchor=tk.CENTER)
			label.grid(column=i, row=1, sticky='ew')
			label = ttk.Label(text=str(1+i), anchor=tk.CENTER)
			label.grid(column=i, row=4, sticky='ew')

		self.label_s = ttk.Label()
		self.label_s.grid(column=0, row=5, columnspan=TAILLE, sticky='ew')

		self.label_msg = ttk.Label(anchor=tk.CENTER)
		self.label_msg.grid(column=0, row=6, columnspan=TAILLE, sticky='ew')

		self.update_state()

	def update_state(self):
		if self.controller.jeu_termine():
			v = self.controller.vainqueur()
			status = "Match nul" if v is None else f"{NOM_CAMPS[v]} a gagne"
			self.label_msg.configure(text=f"JEU TERMINE ! {status}", background="red", foreground="white")
			for button in (self.buttons_n + self.buttons_s):
				button.configure(state=tk.DISABLED)

		turn = self.controller.trait_actuel()
		last_turn = JOEUR_NORD if turn == JOEUR_SUD else JOEUR_SUD
		arrow_n = " <---" if turn == JOEUR_NORD else ""
		arrow_s = " <---" if turn == JOEUR_SUD else ""
		self.label_n.configure(text=f"{NOM_CAMPS[JOEUR_NORD]}: {self.score[JOEUR_NORD]}{arrow_n}")
		self.label_s.configure(text=f"{NOM_CAMPS[JOEUR_SUD]}: {self.score[JOEUR_SUD]}{arrow_s}")
		
		for button, x in zip(self.buttons_n, reversed(self.table[TAILLE:])):
			state = tk.DISABLED if (self.human == JOEUR_SUD or turn == JOEUR_SUD or not x) else tk.ACTIVE
			button.configure(text=str(x), state=state)
		for button, x in zip(self.buttons_s, self.table[:TAILLE]):
			state = tk.DISABLED if (self.human == JOEUR_NORD or turn == JOEUR_NORD or not x) else tk.ACTIVE
			button.configure(text=str(x), state=state)

		if self.controller.jeu_termine():
			v = self.controller.vainqueur()
			status = "Match nul" if v is None else f"{NOM_CAMPS[v]} a gagne"
			self.label_msg.configure(text=f"JEU TERMINE ! {status}", background="red", foreground="white")
			for button in (self.buttons_n + self.buttons_s):
				button.configure(state=tk.DISABLED)
		elif self.last_move:
			self.label_msg.configure(text=f"{NOM_CAMPS[last_turn]} joue {self.last_move}")
