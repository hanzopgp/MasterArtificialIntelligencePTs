from .constants import *


class Awele:
	def __init__(self, n):
		self.dimension = n							# le nombre de colonnes du plateau
		self.plateau = [4 for _ in range(0, 2*n)]	# on met 4 graines dans chaque case
		self.trait = JOEUR_SUD						# le joueur qui doit jouer: 'SUD' ou 'NORD'
		self.butin = {JOEUR_SUD: 0, JOEUR_NORD: 0}	# graines prises par chaque joueur

	def __str__(self):
		"""Afficher la position avec la fonction print()"""
		n = self.dimension
		buffercol = "colonnes:"
		for i in range(1, n + 1):
			buffercol += f"\t {i} "
		buffer = "\n* * * * * * * * * * * * * * * * * * * *\n"
		buffer += f"\t\tNORD (prises:{self.butin[JOEUR_NORD]})\n"
		buffer += "< - - - - - - - - - - - - - - -\n"
		buffer += buffercol + "\n        "
		for x in self.getCamp(JOEUR_NORD):
			buffer += f"\t[{x}]"
		buffer += "\n        "
		for x in self.getCamp(JOEUR_SUD):
			buffer += f"\t[{x}]"
		buffer += '\n' + buffercol
		buffer += "\n- - - - - - - - - - - - - - - >\n"
		buffer += f"\t\tSUD (prises:{self.butin[JOEUR_SUD]})\n"
		buffer += '-> camp au trait: ' + NOM_CAMPS[self.trait]
		buffer += "\n* * * * * * * * * * * * * * * * * * * *\n"
		return buffer

	def chez_ennemi(self, i):
		return (self.trait == JOEUR_NORD and i < self.dimension) \
				or (self.trait == JOEUR_SUD and i >= self.dimension)

	def jouer(self, coup):
		"""Joeur le coup, avec l'hypothese que coup est legal"""
		n = self.dimension
		indice_depart = (coup - 1) * (self.trait == JOEUR_SUD) + (2*n - coup) * (self.trait == JOEUR_NORD)
		nbGraines = self.plateau[indice_depart]
		self.plateau[indice_depart] = 0
		indice_courant = indice_depart
		while nbGraines:
			indice_courant = (indice_courant + 1) % (2*n)
			if indice_courant != indice_depart:
				self.plateau[indice_courant] += 1
				nbGraines -= 1
		while self.chez_ennemi(indice_courant) and self.plateau[indice_courant] in (2,3):
			self.butin[self.trait] += self.plateau[indice_courant]
			self.plateau[indice_courant] = 0
			indice_courant = (indice_courant - 1) % (2*n)
		self.trait = JOEUR_NORD if self.trait == JOEUR_SUD else JOEUR_SUD

	def getCamp(self, joeur):
		"""Renvoyer la liste representant le camp du joeur passer en parametre"""
		if joeur == JOEUR_NORD:
			return list(reversed(self.plateau[self.dimension:]))
		elif joeur == JOEUR_SUD:
			return self.plateau[:self.dimension]
		return None
