from .algo_base import *
from random import choice, shuffle


class CPUPlayer:
	def __init__(self, niveau: int, camp: int):
		self.niv = niveau
		self.camp = camp

	def jouer(self, position: Awele) -> int:
		"""Renvoyer le coup CPU va jouer selon son niveau"""
		if position.trait != self.camp:
			return 0
		if self.niv <= 0:
			return CPUPlayer.aleatoire(position)
		elif self.niv == 1:
			return CPUPlayer.alpha_beta(position, 2, CPUPlayer.evalue_naive)[0]
		elif self.niv == 2:
			return CPUPlayer.alpha_beta(position, 4, CPUPlayer.evalue_naive)[0]
		elif self.niv == 3:
			return CPUPlayer.alpha_beta(position, 4, CPUPlayer.evalue_boost)[0]
		elif self.niv == 4:
			return CPUPlayer.alpha_beta(position, 6, CPUPlayer.evalue_boost)[0]
		else:
			return CPUPlayer.alpha_beta(position, 8, CPUPlayer.evalue_boost)[0]

	@staticmethod
	def aleatoire(position: Awele):
		"""AI stupid qui choisit un coup aleatoire"""
		return choice(coups_possibles(position))

	@staticmethod
	def alpha_beta(position:Awele, prof: int, eval_f, alpha=INF_N, beta=INF_P, coup=0) -> tuple:
		"""Bon AI qui choisit le meilleur coup avec minimax et coupage alpha-beta"""
		if prof == 0 or est_terminale(position):
			return coup, eval_f(position)

		best = 0
		possible = coups_possibles(position)
		shuffle(possible)
		comparateur = max if position.trait == JOEUR_SUD else min
		valeur = alpha * (position.trait == JOEUR_SUD) + beta * (position.trait == JOEUR_NORD)
		for coup in possible:
			if alpha >= beta:
				break
			nouvelle_pos = deepcopy(position)
			nouvelle_pos.jouer(coup)
			temp = comparateur(valeur, CPUPlayer.alpha_beta(nouvelle_pos, prof-1, eval_f, alpha, beta, coup)[1])
			if temp != valeur:
				valeur = temp
				best = coup
				if position.trait == JOEUR_SUD:
					alpha = valeur
				elif position.trait == JOEUR_NORD:
					beta = valeur
		return best, valeur

	@staticmethod
	def evalue_naive(position: Awele):

		def f12(trait: int) -> int:
			l = position.getCamp(trait)
			return len([x for x in l if x in (1,2)])

		gagne = 4 * position.dimension + 1
		if position.butin[JOEUR_SUD] >= gagne:
			return INF_P
		elif position.butin[JOEUR_NORD] >= gagne:
			return INF_N
		return 2 * (position.butin[JOEUR_SUD] - position.butin[JOEUR_NORD]) + f12(JOEUR_NORD) - f12(JOEUR_SUD)

	@staticmethod
	def evalue_boost(position: Awele):

		def f12_boost(trait: int) -> int:
			score = 0
			for x in position.getCamp(trait):
				score += x * (x in (1, 2))
			return score
		
		gagne = 4 * position.dimension + 1
		if position.butin[JOEUR_SUD] >= gagne:
			return INF_P
		elif position.butin[JOEUR_NORD] >= gagne:
			return INF_N
		if position.butin[JOEUR_SUD] > position.butin[JOEUR_NORD]:
			return 2 * (position.butin[JOEUR_SUD] - position.butin[JOEUR_NORD]) \
				+ f12_boost(JOEUR_NORD) - 1.5*f12_boost(JOEUR_SUD)
		elif position.butin[JOEUR_SUD] < position.butin[JOEUR_NORD]:
			return 2 * (position.butin[JOEUR_SUD] - position.butin[JOEUR_NORD]) \
				+ 1.5*f12_boost(JOEUR_NORD) - f12_boost(JOEUR_SUD)
		return 2 * (position.butin[JOEUR_SUD] - position.butin[JOEUR_NORD]) \
			+ f12_boost(JOEUR_NORD) - f12_boost(JOEUR_SUD)
	