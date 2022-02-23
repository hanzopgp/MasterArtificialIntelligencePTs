from TMEcore import *


def encoderC1(ne, nj):
	"""Encoder chaque equipe ne peut jouer plus d'un match par jour"""
	clauses = []
	for j in range(nj):
		for x in range(ne):
			list_vars = [calcul_k(ne, nj, j, x, y) for y in range(ne) if x != y] \
				+ [calcul_k(ne, nj, j, y, x) for y in range(ne) if x != y]
			clauses += au_plus_1(list_vars)
	return clauses


def encoderC2(ne, nj):
	"""Encoder sur la duree du championnat chaque equipe doit rencontrer l'ensemble des autres
	equipes une fois a domicile et une fois a l'ext soit exactement 2 matchs par equipe adverse"""
	clauses = []
	for x, y in combinations(range(ne), 2):
		clauses += au_plus_1([calcul_k(ne, nj, j, x, y) for j in range(nj)])
		clauses += au_moins_1([calcul_k(ne, nj, j, x, y) for j in range(nj)])
		clauses += au_plus_1([calcul_k(ne, nj, j, y, x) for j in range(nj)])
		clauses += au_moins_1([calcul_k(ne, nj, j, y, x) for j in range(nj)])
	return clauses
	
def encoder(ne, nj):
	"""Programme principal"""
	return encoderC1(ne, nj) + encoderC2(ne, nj)


if __name__ == '__main__':
	pass