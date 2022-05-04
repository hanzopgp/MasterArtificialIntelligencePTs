from subprocess import run
import platform

COLOR = dict(
	blanc="\033[0m",
	bleu="\033[94m",
	vert="\033[92m",
	rouge="\033[91m",
	jaune="\033[93m"
)

EXE = ".\clingo.exe" if platform.system() == 'Windows' else "./clingo"	# executable
LP = "ex5.lp"	# LP file for exo 5
N = 1

def parse_rule(rule:str):
	i = rule.index('(')
	name = rule[:i]
	num = int(rule[i+1])
	val = rule[i+3:-1]
	return name, num, val

def print_answer(line):
	answer = dict(
		house_color=[None] * 5,
		house_origin=[None] * 5,
		house_drink=[None] * 5,
		house_pet=[None] * 5,
		house_smoke=[None] * 5,
	)
	for rule in line.split():
		name, num, value = parse_rule(rule)
		answer[name][num-1] = value
	print(f"Answer #{N}")
	
	print("  Couleur : ", end='')
	for color in answer["house_color"]:
		print(COLOR[color] + ("%-12s" % color) + COLOR["blanc"], end='')
	print()

	print("  Origine : ", end='')
	for i, origin in enumerate(answer["house_origin"]):
		color = answer["house_color"][i]
		print(COLOR[color] + ("%-12s" % origin) + COLOR["blanc"], end='')
	print()
	
	print("  Animal  : ", end='')
	for i, pet in enumerate(answer["house_pet"]):
		color = answer["house_color"][i]
		if pet == 'poisson':
			print('\033[4m', end='')
		print(COLOR[color] + ("%-12s" % pet) + COLOR["blanc"], end='')
	print()

	print("  Boisson : ", end='')
	for i, drink in enumerate(answer["house_drink"]):
		color = answer["house_color"][i]
		print(COLOR[color] + ("%-12s" % drink) + COLOR["blanc"], end='')
	print()

	print("  Fume    : ", end='')
	for i, smoke in enumerate(answer["house_smoke"]):
		color = answer["house_color"][i]
		print(COLOR[color] + ("%-12s" % smoke) + COLOR["blanc"], end='')
	print()

if __name__ == "__main__":
	solution = run([EXE, '0', LP], capture_output=True).stdout.decode()
	endl = '\r\n' if '\r\n' in solution else '\n'
	lines = solution.split(endl)
	for i, l in enumerate(lines):
		if l.startswith("Answer:"):
			print_answer(lines[i + 1])
			N += 1
