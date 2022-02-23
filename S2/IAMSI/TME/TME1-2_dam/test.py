from random import choice

JOEUR_SUD  = 0
JOEUR_NORD = 1
NOM_CAMPS = {JOEUR_SUD: "SUD", JOEUR_NORD: "NORD"}

class AwelePosition:
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
		buffer = "* * * * * * * * * * * * * * * * * * * *\n"
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

	def estChezEnnemi(self, i):
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
		while self.estChezEnnemi(indice_courant) and self.plateau[indice_courant] in (2,3):
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

from copy import deepcopy

def est_correct(position: AwelePosition, nombre: int) -> bool:
	if nombre < 1 or nombre > position.dimension:
		return False
	camp = position.getCamp(position.trait)
	return camp[nombre - 1] > 0

def est_legale(position: AwelePosition) -> bool:
	return any(position.getCamp(position.trait))

def effectue_si_valide(position: AwelePosition, coup: int):
	if est_correct(position, coup):
		nouvelle_pos = deepcopy(position)
		nouvelle_pos.jouer(coup)
		if est_legale(nouvelle_pos):
			return nouvelle_pos
	return False

def est_terminale(position: AwelePosition) -> bool:
	gagne = 4 * position.dimension + 1
	for coup in range(1, position.dimension):
		pos = effectue_si_valide(position, coup)
		if pos and position.butin[JOEUR_NORD] < gagne and position.butin[JOEUR_SUD] < gagne:
			return False
	return True

def partie_humains(n):
	position = AwelePosition(n)
	while not est_terminale(position):
		print(position)
		while True:
			coup = int(input(f"Jouer {NOM_CAMPS[position.trait]}: "))
			nouvelle_pos = effectue_si_valide(position, coup)
			if nouvelle_pos:
				position = nouvelle_pos
				break

def genere_un_coup(position: AwelePosition) -> int:
	possible = [coup for coup in range(1, position.dimension + 1) if effectue_si_valide(position,coup)]
	return choice(possible) if len(possible) else 0

def partie_aleatoire(taille: int, campCPU: int):
	position = AwelePosition(taille)
	while not est_terminale(position):
		print(position)
		if position.trait == campCPU:	# CPU joue
			coup = genere_un_coup(position)
			if not coup:
				break
			position.jouer(coup)
			print(f"CPU ({NOM_CAMPS[campCPU]}) a joue {coup}")
		else:		# humain joue
			while True:
				coup = int(input(f"{NOM_CAMPS[position.trait]} va jouer: "))
				nouvelle_pos = effectue_si_valide(position, coup)
				if nouvelle_pos:
					break
			position = nouvelle_pos
	if position.butin[JOEUR_SUD] > position.butin[JOEUR_NORD]:
		print("SUD gagne")
	elif position.butin[JOEUR_SUD] < position.butin[JOEUR_NORD]:
		print("NORD gagne")
	else:
		print("DRAW")

def f12(position:AwelePosition, trait: int) -> int:
	l = position.getCamp(trait)
	return len([x for x in l if x in (1,2)])

def evalue(position: AwelePosition):
	gagne = 4 * position.dimension + 1
	if position.butin[JOEUR_SUD] >= gagne:
		return 99
	elif position.butin[JOEUR_NORD] >= gagne:
		return -99
	return 2 * (position.butin[JOEUR_SUD] - position.butin[JOEUR_NORD]) + f12(position, JOEUR_NORD) - f12(position, JOEUR_SUD)

def coups_possibles(position: AwelePosition) -> list:
	return [coup for coup in range(1, position.dimension + 1) if effectue_si_valide(position, coup)]

def minimax(position: AwelePosition, prof: int, coup: int = 0) -> tuple:
	if prof == 0:
		return coup, evalue(position)
	if position.trait == JOEUR_SUD:	# maximiser
		value = -100
		best = 0
		for coup in coups_possibles(position):
			nouvelle_pos = deepcopy(position)
			nouvelle_pos.jouer(coup)
			x = max(value, minimax(nouvelle_pos, prof - 1, coup)[1])
			if x > value:
				value = x
				best = coup
	else:
		value = 100
		best = 0
		for coup in coups_possibles(position):
			nouvelle_pos = deepcopy(position)
			nouvelle_pos.jouer(coup)
			x = min(value, minimax(nouvelle_pos, prof - 1, coup)[1])
			if x < value:
				value = x
				best = coup
	return best, value
		
def alpha_beta(position:AwelePosition, prof: int, alpha:int, beta:int, coup=0) -> tuple:
	if prof == 0 or est_terminale(position):
		return coup, evalue(position)
	if position.trait == JOEUR_SUD:	# maximiser
		best = 0
		for coup in coups_possibles(position):
			nouvelle_pos = deepcopy(position)
			nouvelle_pos.jouer(coup)
			x = max(alpha, alpha_beta(nouvelle_pos, prof - 1, alpha, beta, coup)[1])
			if x > alpha:
				alpha = x
				best = coup
			if alpha >= beta:
				break
		return best, alpha
	else:
		best = 0
		for coup in coups_possibles(position):
			nouvelle_pos = deepcopy(position)
			nouvelle_pos.jouer(coup)
			x = min(beta, alpha_beta(nouvelle_pos, prof - 1, alpha, beta, coup)[1])
			if x < beta:
				beta = x
				best = coup
			if alpha >= beta:
				break
		return best, beta

pos = AwelePosition(6)
pos.plateau = [1,0,0,6,0,1,1,1,1,1,2,0]
pos.butin[JOEUR_SUD] = pos.butin[JOEUR_NORD] = 17
alpha_beta(pos, 2, -1000, 1000)
# coups_possibles(pos)