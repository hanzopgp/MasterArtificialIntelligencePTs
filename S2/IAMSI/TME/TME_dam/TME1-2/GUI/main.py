from interne.GUIStartWindow import StartWindow
from interne.Controller import Controller
from interne.constants import *


if __name__ == '__main__':
	startwin = StartWindow()
	humain, niv = startwin.run()
	if not humain or not niv:
		exit(0)
	Controller(humain, niv).run()