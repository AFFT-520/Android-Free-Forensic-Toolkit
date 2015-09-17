#!/usr/bin/env python

import os, subprocess, threading, step2, time, sys, pdb, getopt, getinfo, re

def manualrun():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "c:", ["case="])
	except getopt.GetoptError as err:
		exit()
	for o, a in opts:
		if o in ("-c", "--case"):
			casefolder = a
			main(casefolder)
			

def main(casefolder):
	cwd = os.path.dirname(os.path.realpath(__file__))
	if os.name == 'nt':
		winadb = os.path.join(cwd, '..', 'bin', 'adb.exe')
		winstep1 = os.path.join(cwd, '..', 'imaging', 'step1win.bat')
		winstep12 = os.path.join(cwd, '..', 'imaging', 'step1-2win.bat')
		winstep2 = os.path.join(cwd, '..', 'imaging', 'step2win.bat')
	subprocess.call('"' + winadb + '" shell cat /proc/partitions' if os.name == 'nt' else 'adb shell \'cat /proc/partitions\'')
	print("Here is a list of partitions on the Android device. You can image individual partitions or you can image the entire drive. To image the entire drive, provide the name of the device that has the largest size.\n\n")
	print("What drive/partition should be imaged?\n")
	device = input("(drive/partition name): ")
	device = device.replace("/dev/","")
	#getinfo.makedb(casefolder)
	if __name__ == '__main__':
		subprocess.Popen([winadb, 'shell', 'su -c "/system/xbin/busybox nc -l -p 5555 -e /system/xbin/busybox dd if=/dev/block/' + str(device) + '"'])
		thread1 = threading.Thread(target=sendcommand, args=(device, winadb, winstep1, cwd, winstep12))
		thread2 = threading.Thread(target=runstep2, args=(casefolder, cwd, winstep2))
		print("Initiating imaging process...\n")
		thread1.start()
		time.sleep(10)
		thread2.start()
		time.sleep (5)
		imagepath = os.path.join(casefolder, "image", "image.dd")
		imagesize = int(os.path.getsize(imagepath))
		while not os.path.getsize(imagepath) == imagesize:
			imagesize = os.path.getsize(imagepath)
			imagesize_human = imagesize/1073741824
			imagesize_human = "%0.2f" % imagesize_human
			sys.stdout.write("\r" + imagesize_human + "GB transferred. ", )
			sys.stdout.flush()
			time.sleep(3)
		

def sendcommand(device, winadb, winstep1, cwd, winstep12):
	if os.name == 'nt':
		cwd = os.path.dirname(os.path.realpath(__file__))
	rootlocations = ["/sbin/su", "/system/bin/su", "/system/xbin/su", "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/xbin/su"]
	rootcheck = False
	for address in rootlocations:
		found = subprocess.Popen([winadb, "shell", "ls", address], stdout=subprocess.PIPE).stdout.read()
		foundstr = str(found)
		badperms = "Permission denied"
		notexist = "No such file or directory"
		if not (re.search(badperms, foundstr) or re.search(notexist, foundstr)):
			rootcheck = True
	if not rootcheck:
		print("'su' was not found on the system. Assuming we are collecting via the TWRP method")
	if rootcheck == True:
		subprocess.Popen([winstep1, device, cwd], stdout=subprocess.PIPE)
	else:
		subprocess.Popen([winstep12, device, cwd], stdout=subprocess.PIPE)

	
def runstep2(casefolder, cwd, winstep2):
	subprocess.Popen([winstep2, casefolder, cwd], stdout=subprocess.PIPE)


manualrun()
	
	
