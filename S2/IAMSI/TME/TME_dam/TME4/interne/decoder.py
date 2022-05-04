#! /usr/bin/python3

import sys
from TMEcore import *


GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'


def essayer_lire_fichiers(glucose_out, noms_equipes):
	"""Essayer d'ouvrir les 2 fichiers glucose_out (la sortie de glucose) et nom_equipes
	(les noms d'equipes ligne par ligne). Renvoie True si tout est bon"""
	try:
		f1 = open(glucose_out, mode='r')
		f1.close()
	except:
		print("Impossible d'ouvrir", glucose_out, file=sys.stderr)
		exit(1)
	if noms_equipes is not None:
		try:
			f2 = open(noms_equipes, mode='r')
			f2.close()
		except:
			print("Impossible d'ouvrir", noms_equipes, file=sys.stderr)
			print("Utiliser les noms d'equipes par default (Equipe <n>)", file=sys.stderr)
			return False
	return True

def lire_sortie_glucose(glucose_out):
	"""Lire le contenu du fichier sorti par glucose et renvoyer la liste de bonne solution
	si cela existe, sinon renvoyer None"""
	with open(glucose_out, mode='r') as fgluc:
		for ligne in fgluc:
			if ligne.startswith('s UNSATISFIABLE'):
				return None
			if ligne.startswith('v '):
				sol = [int(k) for k in ligne.split()[1:] if k[0] != '-']
				if len(sol) <= 1:	# renvoyer None si la reponse est negative partout
					return None
				return sol[:-1]		# supprimer le 0 a la fin

def lire_noms_equipes(noms_equipes, ne):
	"""Lire le contenu du fichier ayant les noms d'equipes et renvoyer la liste des noms
	lus par ordre. Si le nombre d'equipes lu est inferieur que ne, ajouter automatiquement
	les noms manquants"""
	if not noms_equipes:
		return [f"Equipe {e}" for e in range(ne)]
	noms = []
	compteur = 0
	with open(noms_equipes, mode='r') as fnoms:
		for ligne in fnoms:
			if compteur >= ne:
				break
			if not len(ligne.split()):	# lignes vides sont ignorees
				continue
			noms.append(ligne.lstrip().rstrip())	# supprimer les espaces devant et a l'arriere de la ligne
			compteur += 1
	while compteur < ne:	# Ajouter les noms manquants
		noms.append(f"Equipe {compteur}")
		compteur += 1
	return noms

def affiche_solution(list_sol, noms):
	ne = len(noms)
	planning = dict()
	for k in list_sol:
		j, x, y = calcul_jxy(ne, k)
		if j  not in planning:
			planning[j] = []
		planning[j].append((x, y))
	for j in sorted(planning.keys()):
		print(f"=== Jour {j} ===")
		for e1, e2 in planning[j]:
			print(f" - {GREEN}{noms[e1]}{ENDC} VS {RED}{noms[e2]}{ENDC}")
		print()


if __name__ == '__main__':
	if len(sys.argv) not in (4, 5):
		print("Usage: ./decoder.py <num_teams> <num_days> <glucose_outfile> [teamnames_file]", file=sys.stderr)
		exit(1)
	ne, nj, fgluc = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
	fnoms = None if len(sys.argv) == 4 else sys.argv[4]

	if not essayer_lire_fichiers(fgluc, fnoms):
		fnoms = None

	solution = lire_sortie_glucose(fgluc)
	if not solution:
		print(f"{fgluc} n'est pas bien formatte ou glucose n'a pas de solution")
		exit(0)

	equipes = lire_noms_equipes(fnoms, ne)
	affiche_solution(solution, equipes)
