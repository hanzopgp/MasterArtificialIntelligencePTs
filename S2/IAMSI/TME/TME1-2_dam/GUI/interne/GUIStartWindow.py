import tkinter as tk
from tkinter import ttk
from .constants import *


class StartWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title(TITLE)
		self.resizable(False, False)
		self.camp, self.cpu_lv = None, None	# valeurs de retour a passer au jeu

		# config style par default
		style = ttk.Style(self)
		style.configure("TLabel", font=("Courier", 14, "bold"))
		style.configure("TRadiobutton", font=("Courier", 12))
		style.configure("TButton", font=("Courier", 12))
		
		self.camp_temp, self.lv_temp = tk.StringVar(), tk.StringVar()
		self.camp_temp.set(NOM_CAMPS[JOEUR_SUD])
		self.lv_temp.set(str(3))

		label = ttk.Label(text="Choisir camp humain (SUD joue en premier)")
		label.grid(column=0, row=0, columnspan=2, sticky='ew')

		radio_s = ttk.Radiobutton(self, text=NOM_CAMPS[JOEUR_SUD], value=NOM_CAMPS[JOEUR_SUD], \
			variable=self.camp_temp)
		radio_s.grid(column=0, row=1, sticky='ew')
		radio_n = ttk.Radiobutton(self, text=NOM_CAMPS[JOEUR_NORD], value=NOM_CAMPS[JOEUR_NORD], \
			variable=self.camp_temp)
		radio_n.grid(column=1, row=1, sticky='ew')

		label = ttk.Label(text="Choisir le niveau du CPU")
		label.grid(column=0, row=2, columnspan=2, sticky='ew')

		cpu_lv = ["Bebe", "Debutant", "Facile", "Moyen", "Dur", "Cauchemar"]
		for lv, text in enumerate(cpu_lv):
			r = ttk.Radiobutton(
				self, text=text, value=str(lv),
				variable=self.lv_temp
			)
			r.grid(column=0, row=3+lv, columnspan=2, sticky='ew')

		button = ttk.Button(self, text="Start Game", command=self.start_game)
		button.grid(column=0, row=9, columnspan=2, sticky='ew')

	def start_game(self):
		self.camp = self.camp_temp.get()
		self.cpu_lv = int(self.lv_temp.get())
		self.destroy()

	def run(self):
		self.mainloop()
		return self.camp, self.cpu_lv
