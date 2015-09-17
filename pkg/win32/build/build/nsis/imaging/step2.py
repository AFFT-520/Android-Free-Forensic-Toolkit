#!/usr/bin/env python

import os, time, sys


def main(casefolder):
	print("\n --> Imaging command sent\n")
	print(" --> Giving device 10 seconds to process command\n")
	time.sleep(10) # There is a variable delay between the sending of the imaging command, and the command being executed by the device. We wait 10 seconds just to be safe
	imagedir = os.path.join(casefolder, "image")
	image = os.path.join(imagedir, "image.dd")
	cwd = os.path.dirname(os.path.realpath(__file__))
	winadb = os.path.join(cwd, '..', 'bin', 'adb.exe') #Gives the location of the ADB and Netcat executables for Windows 
	winnc = os.path.join(cwd, '..', 'bin', 'nc.exe')
	os.system(winadb + ' forward tcp:5555 tcp:5555' if os.name == 'nt' else 'adb forward tcp:5555 tcp:5555')
	winnc_exec = winnc + ' 127.0.0.1 5555 > ' + image
	linnc_exec = 'nc 127.0.0.1 5555 > ' + image 
	print(" --> Writing image to host PC\n")
	os.system(winnc_exec if os.name == 'nt' else linnc_exec)# On both Windows and UNIX-like OSes, runs the netcat command to listen for the image data and dump it to the file [case]/image/image.dd
	if sys.platform in ('linux', 'linux2'): #If on Linux, prepare the mount location
		mountdir = os.path.join(casefolder, "mount")
		if not os.path.exists(mountdir):
			os.makedirs(mountdir)
		
	
	
	
	
