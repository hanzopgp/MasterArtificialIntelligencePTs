#! /usr/bin/python3

import sys
import os
from subprocess import run

FICHIER_TEMP = 'glucose_sol.tmp'


if __name__ == '__main__':
	if len(sys.argv) not in (3, 4):
		print("Usage: ./program.py <num_teams> <num_days> [teamnames_file]", file=sys.stderr)
		exit(1)
	ne, nj = sys.argv[1], sys.argv[2]
	fnoms = None if len(sys.argv) == 3 else sys.argv[3]

	encodage = run(['./interne/encoder.py', ne, nj], capture_output=True)
	gluc = run(['./glucose_static', '-model'], input=encodage.stdout, capture_output=True)
	with open(FICHIER_TEMP, mode='w') as fsol:
		fsol.write(gluc.stdout.decode())
	
	decoder_args = ['./interne/decoder.py', ne, nj, FICHIER_TEMP]
	if fnoms is not None:
		decoder_args.append(fnoms)
	run(decoder_args)
	os.remove(FICHIER_TEMP)
