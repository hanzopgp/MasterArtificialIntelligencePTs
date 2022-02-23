"""
Nombre de variables:
C(ne,2) * 2 * nj
"""

from itertools import combinations


def calcul_k(ne, nj, j, x, y):
	"""Calculer k l'id de la variable"""
	return j * ne**2 + x * ne + y + 1

def calcul_jxy(ne, k):
	"""Calculer j,x,y les attributs individus de la variable k"""
	y = (k - 1) % ne
	x = ((k-1-y) // ne) % ne
	j = (k - 1 - y - x*ne) // (ne**2)
	return j, x, y

def au_moins_1(list_vars):
	"""Renvoie une clause DIMACS correspondant a la contrainte au moins une de ces vars est vraie"""
	return [" ".join(map(str, list_vars + [0]))]

def au_plus_1(list_vars):
	"""Renvoie une liste des clauses DIMACS correspondant a la contrainte au plus une de ces vars est vraie"""
	l = [[-i, -j] for i, j in combinations(list_vars, 2)]
	return [" ".join(map(str, clause + [0])) for clause in l]
