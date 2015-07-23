#!/usr/bin/env python
import sys, os, mounter.mounter

def mountfs(case):
	if sys.platform in ('linux', 'linux2'):
		mounter.mounter.mount(case)
	else:
		print("This is a Linux command that will not work on your system. To mount the image, please use a third-party tool such as FTK imager")
		input("Press Enter to return to the main menu")

def unmountfs(case):
	if sys.platform in ('linux', 'linux2'):
		scriptpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unmount.sh")
		os.system(scriptpath + " " + case)
	else:
		print("AFFT does not handle image mounting on non-Linux systems. To unmount the drive, refer to the tool you used to mount it.")
		input("Press Enter to return to the main menu")
				
def repair(case):
	if sys.platform in ('linux', 'linux2'):
		scriptpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repair.sh")
		scriptpathunmount = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unmount.sh")
		os.system(scriptpath + " " + case)
		os.system(scriptpathunmount + " " + case)
	else:
		print("AFFT cannot repair filesystems on a non-Linux host. ")
		input("Press Enter to return to the main menu")

