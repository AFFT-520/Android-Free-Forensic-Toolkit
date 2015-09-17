#!/usr/bin/env python

import os, ctypes, sethome, sys, legalprompt, imaging.source, mounter.mount, lockscreen.lockscreen, extractor.extractor


def getuserdatapartition(caselocation): # Prompts the user for the location of the mounted disk. Saves this for future reference in [case]/image/username.txt
	userdata = input("Please provide the full path to the root of the mounted user data partition (usually called 'userdata')")
	settingslocation= os.path.join(caselocation, "image", "userdata-name.txt")
	settfile = open(settingslocation,'w')
	settfile.write(userdata + "\n")
	settfile.truncate()
	settfile.close
	
	
def mac (case):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("NOTICE FOR MAC OSX USERS\n")
	print("-------------------------\n\n")
	print("AFFT has detected that you are running this tool under Mac OSX. OSX does not have native support for Ext3/4 to extract user data using the toolkit alone. As such, the option to mount the Android image partitions are not available from this toolkit.\n\n")
	print("You may, however, use a third party mounting tool to compensate. If you do not have one already, we recommend downloading FTK Imager for Mac for this task, but you may use whichever tool you prefer. If you choose to do this, please provide the path to the root of the user data partition (usually named 'userdata')\n\n")
	print("How would you like to proceed?\n")
	print("1) Enable user data extraction. I will provide the path to the userdata partition\n")
	print("2) Disable user data extraction options")
	option = input()
	
	if option == "1":
		menuotheros(case)
	elif option == "2":
		menuotherosnoextract(case)
	else:
		mac(case)
def windows (case):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("NOTICE FOR WINDOWS USERS\n")
	print("-------------------------\n\n")
	print("AFFT has detected that you are running this tool under Windows. Windows does not have either the necessary loopback interfaces or native support for Ext3/4 to extract user data using the toolkit alone. As such, the option to mount the Android image partitions are not available from this toolkit.\n\n")
	print("You may, however, use a third party mounting tool to compensate. If you do not have one already, we recommend downloading FTK Imager for this task, but you may use whichever tool you prefer. If you choose to do this, please provide the path to the root of the user data partition (usually named 'userdata')\n\n")
	print("How would you like to proceed?\n\n")
	print("1) Enable user data extraction. I will provide the path to the userdata partition\n")
	print("2) Disable user data extraction options")
	option = input()
	
	if option == "1":
		menuotheros(case)
	elif option == "2":
		menuotherosnoextract(case)
	else:
		windows(case)

def menulinux (case):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne)")
	print("-----------------------------------------------\n")
	print("The casefiles can be found in " + case + os.path.sep + "\n")
	print("Select an option:")
	print("1) Retrieve or import a whole-system image from device")
	print("2) Mount Android images (where possible)")
	print("3) Obtain communication dumps")
	print("4) Unmount Android images and perform cleanup")
	print("5) Repair Android images (WARNING: Alters image)")
	print("6) Disable lock-screen security on device")
	print("7) Exit")
	option = input()
	
	if option == "1":
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		imaging.step1.main(case)
		menulinux (case)
	elif option == "2":
		mounter.mount.mountfs(case)
		menulinux(case)
	elif option == "3":
		extractor.extractor.main(case)
		menulinux(case)
	elif option == "4":
		mounter.mount.unmountfs(case)
		menulinux(case)
	elif option == "5":
		mounter.mount.repair(case)
		menulinux(case)
	elif option == "6":
		lockscreen.lockscreen.breakpassword()
		menulinux(case)
	elif option == "7":
		sys.exit(0)
	else:
		menulinux(case)

def menuotheros (case):
	#os.system('cls' if os.name == 'nt' else 'clear')
	print("Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne)")
	print("-----------------------------------------------\n")
	print("The casefiles can be found in " + case + os.path.sep + "\n")
	print("Select an option:")
	print("1) Retrieve or import a whole-system image from device")
	print("2) Obtain communication dumps")
	print("3) Disable lock-screen security on device")
	print("4) Exit")
	option = input()
	
	if option == "1":
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		if os.name == 'nt':
			imaging.step1win.main(case)
		else:
			imaging.step1.main(case)
		menuotheros (case)
	elif option == "2":
		extractor.extractor.main(case)
		menuotheros(case)
	elif option == "3":
		lockscreen.lockscreen.breakpassword()
		menuotheros(case)
	elif option == "4":
		sys.exit(0)
	else:
		menuotheros(case)

def menuotherosnoextract (case):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne)")
	print("-----------------------------------------------\n")
	print("The casefiles can be found in " + case + os.path.sep + "\n")
	print("Select an option:")
	print("1) Retrieve or import a whole-system image from device")
	print("2) Disable lock-screen security on device")
	print("3) Exit")
	option = input()
	
	if option == "1":
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		if os.name == 'nt':
			imaging.step1win.main(case)
		else:
			imaging.step1.main(case)
		menuotherosnoextract (case)
	elif option == "2":
		lockscreen.lockscreen.breakpassword()
		menuotherosnoextract(case)
	elif option == "3":
		sys.exit(0)
	else:
		menuotherosnoextract(case)
		
def checkroot():
	if sys.platform == 'win32':
		isRoot = ctypes.windll.shell32.IsUserAnAdmin() != 0
		if isRoot == False:
			print('ERROR! Insufficient privileges to run this tool. Please run this tools as a Local Administrator (Right click the program and click \'Run as Administrator\')')
			input('Press Enter to exit')
			exit(1)
	else:
		isRoot = os.access('/', os.W_OK)
		if isRoot == False:
			print('ERROR! Insufficient privileges to run this tool. Please run this tool as root or use \'sudo\'')
			input('Press Enter to exit')
			exit(1)


def intro ():
	checkroot()
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Please provide the directory name for the case items")
	phonecase = input()
	case = os.path.join(casehome, "afft-cases", phonecase) 
	if not os.path.exists(case):
		os.makedirs(case)
	if sys.platform in ('linux', 'linux2'):
		menulinux(case)
	elif sys.platform == 'win32':
		windows(case)
	elif sys.platform == 'darwin':
		mac(case)
legalprompt.main()
casehome = sethome.main()
intro()

