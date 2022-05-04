#! /usr/bin/python3

import sys
from TMEcore import *


def encoderC1(ne, nj):
	"""Encoder chaque equipe ne peut jouer plus d'un match par jour"""
	clauses = []
	for j in range(nj):
		for e1 in range(ne):
			list_vars = [calcul_k(ne, nj, j, e1, e2) for e2 in range(ne) if e1 != e2] \
				+ [calcul_k(ne, nj, j, e2, e1) for e2 in range(ne) if e1 != e2]
			clauses += au_plus_1(list_vars)
	return clauses


def encoderC2(ne, nj):
	"""Encoder sur la duree du championnat chaque equipe doit rencontrer l'ensemble des autres
	equipes une fois a domicile et une fois a l'ext soit exactement 2 matchs par equipe adverse"""
	clauses = []
	for e1, e2 in combinations(range(ne), 2):
		clauses += au_plus_1([calcul_k(ne, nj, j, e1, e2) for j in range(nj)])
		clauses += au_moins_1([calcul_k(ne, nj, j, e1, e2) for j in range(nj)])
		clauses += au_plus_1([calcul_k(ne, nj, j, e2, e1) for j in range(nj)])
		clauses += au_moins_1([calcul_k(ne, nj, j, e2, e1) for j in range(nj)])
	return clauses
	
def encoder(ne, nj):
	"""Programme principal"""
	return encoderC1(ne, nj) + encoderC2(ne, nj)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: ./encoder.py <num_teams> <num_days>", file=sys.stderr)
		exit(1)
	ne, nj = int(sys.argv[1]), int(sys.argv[2])
	clauses = encoder(ne, nj)
	print("p cnf", calcul_nbvar(ne, nj), len(clauses))
	for c in clauses:
		print(c)