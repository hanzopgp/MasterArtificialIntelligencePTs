from subprocess import run


def iterer_glucose(ne):
	"""Iterer nj pour trouver la valeur mininmale satisfaisante"""
	nj = 0
	while True:
		nj += 2		# on itere seulement les nombres pairs car nj ne peut etre impair
		encodage = run(['./interne/encoder.py', str(ne), str(nj)], capture_output=True)
		try:
			gluc = run(['./glucose_static', '-model'], input=encodage.stdout, timeout=10, capture_output=True)
		except:
			# Timeout, on continue avec la valeur suivante de nj
			continue
		if b"UNSATISFIABLE" in gluc.stdout:
			continue
		if b"SATISFIABLE" in gluc.stdout:
			return nj


if __name__ == '__main__':
	for ne in range(3, 11):
		nj_optim = iterer_glucose(ne)
		print(f"ne = {ne}, nj optimal = {nj_optim}")
	
	# Les valeurs optimales sont suivantes:
	# ne = 3, nj optimal = 6
	# ne = 4, nj optimal = 6
	# ne = 5, nj optimal = 10
	# ne = 6, nj optimal = 10
	# ne = 7, nj optimal = 14
	# ne = 8, nj optimal = 14
	# ne = 9, nj optimal = 18
	# ne = 10, nj optimal = 18
	# Formule : nj_optim = 2 * (ne - bool(ne est pair)) ????