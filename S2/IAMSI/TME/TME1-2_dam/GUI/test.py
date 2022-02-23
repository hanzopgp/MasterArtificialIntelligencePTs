from tqdm import tqdm
from interne.constants import *
from interne.Awele import Awele
from interne.CPUPlayer import CPUPlayer
from interne.algo_base import est_terminale
import numpy as np

def cpu_vs_cpu(niv_sud: int, niv_nord: int):
	position = Awele(TAILLE)
	sud = CPUPlayer(niv_sud, JOEUR_SUD)
	nord = CPUPlayer(niv_nord, JOEUR_NORD)

	while not est_terminale(position):
		coup = nord.jouer(position) if position.trait == JOEUR_NORD else sud.jouer(position)
		if not coup:
			break
		position.jouer(coup)

	if position.butin[JOEUR_SUD] > position.butin[JOEUR_NORD]:
		return "SUD", position.butin[JOEUR_SUD] - position.butin[JOEUR_NORD]
	elif position.butin[JOEUR_SUD] < position.butin[JOEUR_NORD]:
		return "NORD", position.butin[JOEUR_NORD] - position.butin[JOEUR_NORD]
	return "DRAW", 0

def results(n_partie, niv_sud, niv_nord):
	winners = []
	ecart = 0

	for _ in tqdm(range(n_partie)):
		try:
			nom, score = cpu_vs_cpu(niv_sud, niv_nord)
			winners.append(nom)
			ecart += score
		except KeyboardInterrupt:
			break

	u, c = np.unique(winners, return_counts=True)
	print("parties gagnees : ", u, c)
	print("ecart moyen pour le gagnant :", ecart/n_partie)

if __name__ == '__main__':
	niv_sud = 2
	niv_nord = 3
	results(30, niv_sud, niv_nord)