#!/usr/bin/env python

import os, ctypes, sethome, sys, legalprompt, imaging.source, mounter.mount, lockscreen.lockscreen, extractor.extractor


def getuserdatapartition(caselocation): # Prompts the user for the location of the mounted disk. Saves this for future reference in [case]/image/username.txt
	userdata = input("Please provide the full path to the root of the mounted user data partition (usually called 'userdata')")
	settingslocation= os.path.join(caselocation, "image", "userdata-name.txt")
	settfile = open(settingslocation,'w')
	settfile.write(userdata + "\n")
	settfile.truncate()
	settfile.close
	
	
def mac (case): # Notifies an OSX user of the limitations of this program when running under Mac OSX and asks how they would like to proceed. Gives a specialised menu with these limitations and choice in mind. Called only when the program is running under OSX.
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
def windows (case): # Notifies a Windows user of the programs limitations when not running under Linux, similar to the 'mac' function above. Called only when the program is running under Windows.
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

def menulinux (case): #Brings up the main menu under Linux
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
		imaging.step1.main(case)#Runs the imaging scripts.
		menulinux (case)
	elif option == "2":
		mounter.mount.mountfs(case)
		menulinux(case) #Mounts the device image found in [case]/image/image.dd to [case]/mount/Partition X (where X represents the number of individual partitions on the image)
	elif option == "3":
		extractor.extractor.main(case)
		menulinux(case) #Runs the extractor tool on mounted images
	elif option == "4":
		mounter.mount.unmountfs(case)
		menulinux(case) #Unmounts the device image and delete's the mountpoints
	elif option == "5":
		mounter.mount.repair(case) #Mounts an image in a forensically unsafe way to allow filesystem fixes, then quickly unmounts. USE AS A LAST RESORT
		menulinux(case)
	elif option == "6":
		lockscreen.lockscreen.breakpassword() #Bypasses the lockscreen of an Android device. WARNING: This alters the settings of the Android device, therefore it may possibly damage evidence.
		menulinux(case)
	elif option == "7":
		sys.exit(0)
	else:
		menulinux(case)

def menuotheros (case): # Brings up the main menu seen when run from other Operating Systems other than Linux-based ones. Seen only when the user is not running the tool under Linux and decides to use a third party tool to handle image mounting.
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
	
	if option == "1":
		imagedir = os.path.join(case, "image")
		if not os.path.exists(imagedir):
			os.makedirs(imagedir)
		os.system('cls' if os.name == 'nt' else 'clear')
		if os.name == 'nt':  #If in Windows, loads the Windows version of the imaging script (which is drastically different in code, if not in function). If in OSX, use the same imaging scripts as Linux
			imaging.step1win.main(case) 
		else:
			imaging.step1.main(case)
		menuotheros (case)
	elif option == "2":
		extractor.extractor.main(case)
		menuotheros(case)
	elif option == "3":
		lockscreen.lockscreen.breakpassword() #Loads the lockscreen bypass tool
		menuotheros(case)
	elif option == "4":
		sys.exit(0)
	else:
		menuotheros(case)

def menuotherosnoextract (case): #Brings up the main menu seen when run from other Operating Systems other than Linux-based ones. Seen when the user decides against using a third party tool to handle image mounting (which means file system examinations cannot be done)
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
			imaging.step1.main(case) #If in Windows, loads the Windows version of the imaging script. If in OSX, use the same imaging scripts as Linux
		menuotherosnoextract (case)
	elif option == "2":
		lockscreen.lockscreen.breakpassword()
		menuotherosnoextract(case) 
	elif option == "3":
		sys.exit(0)
	else:
		menuotherosnoextract(case)
		
def checkroot(): #Checks for root/admin access on Windows or UNIX-Like machines. If root/admin access is not found, it will display an error message saying that said privileges are required for the program to function effectively (May not be as true on Windows, considering altering this function to reflect that) and then exits. Waits for user's input to ensure the message is read.
	if sys.platform == 'win32':
		isRoot = ctypes.windll.shell32.IsUserAnAdmin() != 0 #This is the Windows admin check condition 
		if isRoot == False:
			print('ERROR! Insufficient privileges to run this tool. Please run this tools as a Local Administrator (Right click the program and click \'Run as Administrator\')') # This is the error message non-admin Windows users see upon running the program
			input('Press Enter to exit') # This waits for the user to press enter before closing, allowing time to read the file and preventing the program from closing immediately
			exit(1)
	else:
		isRoot = os.access('/', os.W_OK) # This is the UNIX-like root check. This works by testing the access to the root filesystem.
		if isRoot == False:
			print('ERROR! Insufficient privileges to run this tool. Please run this tool as root or use \'sudo\'') # # This is the error message non-root users of UNIX-like OSes see upon running the program (without running 'sudo')
			input('Press Enter to exit') # Waits for the user to press enter before quitting, ensuring instances not initiated via terminal still give the user ample time to read the error.
			exit(1)


def intro ():
	checkroot()
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Please provide the directory name for the case items")
	phonecase = input() #Gets the name for the active case
	case = os.path.join(casehome, "afft-cases", phonecase) #The directory of the active case
	if not os.path.exists(case):
		os.makedirs(case)# If the case directory doesnt exist, make it.
	if sys.platform in ('linux', 'linux2'): # If run in Linux, load the main menu.
		menulinux(case)
	elif sys.platform == 'win32': # If running on Windows, inform user of limitations vs Linux version and load appropriate menu
		windows(case)
	elif sys.platform == 'darwin': # If running on Mac OSX, inform user of limitations vs Linux version and load appropriate menu
		mac(case)
legalprompt.main() #Displays legal waivers if it detects that it has not been agreed to yet
casehome = sethome.main() # Gets the location of the case directory from the settings file
intro()

