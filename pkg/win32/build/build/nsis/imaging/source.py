#!/usr/bin/env python

import os, sys, imaging.step1

def picksource(casefolder):
	cwd = os.path.dirname(os.path.realpath(__file__))
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Do you wish to acquire an image directly from an Android device or import an existing one?\n\n")
	print("A) Acquire an image from a device\n")
	print("I) Import a pre-existing image for use with AFFT\n")
	print("R) Return to the main menu")
	choice = input("[A/I/R]")
	
	if choice in ("a", "A"):
		if os.name == 'nt':
			script = os.path.join(cwd, "step1win.py")
			os.system(script + " -c " + casefolder)
		else:
			imaging.step1.main(casefolder)
	elif choice in ("i", "I"):
		importer = os.path.join(os.getcwd(), "mounter", "import.sh")
		os.system(importer + ' "' + casefolder + '"')
	elif choice in ("r", "R"):
		return (0)
