#!/usr/bin/env python

import os, ctypes, sethome, sys, legalprompt, imaging.step1, mounter.mount, lockscreen.lockscreen, extractor.extractor

def getuserdatapartition(caselocation): #If we don't know the partition that hosts the 'userdata' partition (not to be confused with the user data area typically found on /sdcard), we'll ask the user.
	userdata = input("Please provide the full path to the root of the mounted user data partition (usually called 'userdata')")
	settingslocation= os.path.join(location, "image", "userdata-name.txt") #We save the answer here for next time
	settfile = open(settingslocation,'w')
	settfile.write(userdata + "\n")
	settfile.truncate()
	settfile.close
	
	
def mac (case): #This notifies the user of the limitations of running the program on Mac OSX, and asks the user if they want to proceeed with data extraction capabilities. Upon their answer, shows the relevant menu.
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
def windows (case): #This notifies the user of the limitations of running the program on Windows, and asks the user if they want to proceeed with data extraction capabilities. Upon their answer, shows the relevant menu.
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

def menulinux (case): #Shows the menu that will be seen on Linux machines
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
	
	if option == "1": #Creates a directory for the disk image (if it doesn't already exist) and proceeds to the imaging scripts
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		imaging.step1.main(case)
		menulinux (case)
	elif option == "2": #Mounts the disk image in a forensically sound manner. The mountpoints for this is [case]/mount/Partition X (Where X is a number)
		mounter.mount.mountfs(case)
		menulinux(case)
	elif option == "3": #Runs the data extraction scripts
		extractor.extractor.main(case)
		menulinux(case)
	elif option == "4": #Unmounts the disk image
		mounter.mount.unmountfs(case)
		menulinux(case)
	elif option == "5": #Mounts the disk image for basic repair then unmounts ASAP. Note: This WILL damage data
		mounter.mount.repair(case)
		menulinux(case)
	elif option == "6": #Runs the script for bypassing lockscreens. Warning: This modifies the Android Settings.
		lockscreen.lockscreen.breakpassword()
		menulinux(case)
	elif option == "7": #Quits
		sys.exit(0)
	else:
		menulinux(case) #If anything odd is entered, simply refresh the menu

def menuotheros (case): #This is the menu seen by non-Linux users if they choose to have data extraction capacity 
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne)")
	print("-----------------------------------------------\n")
	print("The casefiles can be found in " + case + os.path.sep + "\n")
	print("Select an option:")
	print("1) Retrieve or import a whole-system image from device")
	print("2) Obtain communication dumps")
	print("3) Disable lock-screen security on device")
	print("4) Exit")
	option = input()
	
	if option == "1": #Make image directory. If on OSX, run the same imaging scripts as Linux. If on Windows, run the Windows-specific version of the scripts
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		if os.name == 'nt':
			cwd = os.path.dirname(os.path.realpath(__file__))
			script = os.path.join(cwd, "imaging", "step1win.py")
			os.system(script + " -c " + case)
		else:
			imaging.step1.main(case)
		menuotheros (case)
	elif option == "2": #See the comment on line 74
		extractor.extractor.main(case)
		menuotheros(case)
	elif option == "3": #See the comment on line 83
		lockscreen.lockscreen.breakpassword()
		menuotheros(case)
	elif option == "4":
		sys.exit(0)
	else:
		menuotheros(case)

def menuotherosnoextract (case): #This is the menu seen by Non-Linux users if they choose not to utilise data extraction capabilities
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne)")
	print("-----------------------------------------------\n")
	print("The casefiles can be found in " + case + os.path.sep + "\n")
	print("Select an option:")
	print("1) Retrieve or import a whole-system image from device")
	print("2) Disable lock-screen security on device")
	print("3) Exit")
	option = input()
	
	if option == "1": #See the comment on line 103
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		if os.name == 'nt':
			cwd = os.path.dirname(os.path.realpath(__file__))
			script = os.path.join(cwd, "imaging", "step1win.py")
			os.system(script + " -c " + case)
		else:
			imaging.step1.main(case)
		menuotherosnoextract (case)
	elif option == "2": #See the comment on line 83
		lockscreen.lockscreen.breakpassword()
		menuotherosnoextract(case)
	elif option == "3":
		sys.exit(0)
	else:
		menuotherosnoextract(case)
		
def checkroot(): #Checks to see if the user has root/admin access, and displays a fatal error if they do not.
	if sys.platform == 'win32':
		isRoot = ctypes.windll.shell32.IsUserAnAdmin() != 0 #This is the Windows admin check
		if isRoot == False:
			print('ERROR! Insufficient privileges to run this tool. Please run this tools as a Local Administrator')
			input('Press Enter to exit') #Allows the user to read the error message if the program was run from a shortcut
			exit(1)
	else:
		isRoot = os.access('/', os.W_OK)
		if isRoot == False:
			print('ERROR! Insufficient privileges to run this tool. Please run this tool as root or use \'sudo\'')
			input('Press Enter to exit') # See the comment on line 162
			exit(1)


def intro (): #The startup procedure of the program
	checkroot()
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Please provide the directory name for the case items")
	phonecase = input() #This is the name of the case the user is working on. If it is a new case, automatically creates it.
	case = os.path.join(casehome, "afft-cases", phonecase) 
	if not os.path.exists(case):
		os.makedirs(case)
	if sys.platform in ('linux', 'linux2'):
		menulinux(case)
	elif sys.platform == 'win32': # 'win32' = Windows
		windows(case)
	elif sys.plaform == 'darwin': #'darwin' usually means OSX. Usually.
		mac(case)
legalprompt.main() #If the user has not accepted the legal disclaimer, show it and refuse to proceed until it is accepted.
casehome = sethome.main() #Get the address for the case files directory
intro()

