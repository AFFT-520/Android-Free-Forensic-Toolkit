#!/usr/bin/env python

import os, subprocess, threading, step2, time, sys, pdb, getopt


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
    os.system(winadb + ' forward tcp:5555 tcp:5555' if os.name == 'nt' else 'adb forward tcp:5555 tcp:5555')
    os.system(winadb + ' shell cat /proc/partitions' if os.name == 'nt' else 'adb shell \'cat /proc/partitions\'')
    print("Here is a list of partitions on the Android device. You can image individual partitions or you can image the entire drive. To image the entire drive, provide the name of the device that has the largest size.\n\n")
    print("What drive/partition should be imaged?\n")
    device = input("(drive/partition name): ")
    device = device.replace("/dev/","")
    imaging.getinfo.makedb(casefolder)
    if __name__ == '__main__':
        subprocess.Popen([winadb, 'shell', 'su -c "/system/xbin/busybox nc -l -p 5555 -e /system/xbin/busybox dd if=/dev/block/' + str(device) + '"'])
        thread = threading.Thread(target=step2.main, args=(casefolder,))
        thread.start()
        imagepath = os.path.join(casefolder, "image", "image.dd")
        imagesize = int(os.path.getsize(imagepath))
        time.sleep (13)
        while not os.path.getsize(imagepath) == imagesize:
            imagesize = os.path.getsize(imagepath)
            imagesize_human = imagesize/1073741824
            imagesize_human = "%0.2f" % imagesize_human
            sys.stdout.write("\r" + imagesize_human + "GB transferred. ", )
            sys.stdout.flush()
            time.sleep(3)


def sendcommand(device):
    su = subprocess.Popen(winadb + ' shell su', shell=True, stdout=subprocess.PIPE).stdout.read()
	print(str(su))
	if re.search(str(su), "not found\\r\\n") != 'None':
		print("'su' was not found on the system. Assuming we are collecting via the TWRP method")
		found_su=False
	else:
		found_su=True
	if found_su == True:
		os.system(winadb + ' shell "su -c \\"nc -l -p 5555 -e dd if=/dev/block/' + device + '\\""')
	else:
		os.system(winadb + ' shell nc -l -p 5555 -e dd if=/dev/block/' + device )

    
def runstep2(casefolder):
    step2.main(str(casefolder))


manualrun()
    
    
