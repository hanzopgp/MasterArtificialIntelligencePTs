from .constants import *
from .Awele import Awele
from copy import deepcopy


def est_correct(position: Awele, coup: int) -> bool:
	if coup < 1 or coup > position.dimension:
		return False
	camp = position.getCamp(position.trait)
	return camp[coup - 1] > 0

def est_legale(position: Awele) -> bool:
	return any(position.getCamp(position.trait))

def effectue_si_valide(position: Awele, coup: int) -> Awele:
	if est_correct(position, coup):
		nouvelle_pos = deepcopy(position)
		nouvelle_pos.jouer(coup)
		if est_legale(nouvelle_pos):
			return nouvelle_pos
	return None

def est_terminale(position: Awele) -> bool:
	gagne = 4 * position.dimension + 1
	for coup in range(1, position.dimension + 1):
		pos = effectue_si_valide(position, coup)
		if pos and position.butin[JOEUR_NORD] < gagne and position.butin[JOEUR_SUD] < gagne:
			return False
	return True

def coups_possibles(position: Awele) -> list:
	return [coup for coup in range(1, position.dimension + 1) if effectue_si_valide(position, coup)]
