from .constants import *
from .algo_base import est_terminale
from .Awele import Awele
from .CPUPlayer import CPUPlayer
from .GUIGameWindow import GameWindow
import threading


class Controller:
	def __init__(self, humain: str, nivCPU: int):
		cpu = JOEUR_NORD if humain == NOM_CAMPS[JOEUR_SUD] else JOEUR_SUD
		self.humain = JOEUR_SUD if cpu == JOEUR_NORD else JOEUR_NORD
		self.cpu = CPUPlayer(nivCPU, cpu)
		self.jeu = Awele(TAILLE)
		self.gui = GameWindow(self.jeu.plateau, self.jeu.butin, self.humain, self)
		if cpu == JOEUR_SUD:
			self.jouer_cpu()

	def run(self):
		self.gui.mainloop()

	def trait_actuel(self) -> int:
		return self.jeu.trait

	def jeu_termine(self) -> bool:
		return est_terminale(self.jeu)

	def vainqueur(self) -> str:
		if self.jeu.butin[JOEUR_NORD] > self.jeu.butin[JOEUR_SUD]:
			return JOEUR_NORD
		elif self.jeu.butin[JOEUR_NORD] < self.jeu.butin[JOEUR_SUD]:
			return JOEUR_SUD
		return None

	def jouer_humain(self, coup: int):
		self.jeu.jouer(coup)

	def jouer_cpu(self):
		def run_cpu_thread():
			coup = self.cpu.jouer(self.jeu)
			if not coup:
				return
			self.jeu.jouer(coup)
			self.gui.last_move = coup
			self.gui.update_state()
		cpu_thread = threading.Thread(target=run_cpu_thread)
		cpu_thread.run()
