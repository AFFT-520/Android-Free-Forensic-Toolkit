#!/usr/bin/env python

import os, multiprocessing, imaging.step2, time, sys, imaging.getinfo, subprocess


def main(casefolder):
    cwd = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'nt': #Redundant, since running in Windows will no longer run this script
        adb = os.path.join(cwd, '..', 'bin', 'adb.exe')
        print(adb)
    os.system(adb + ' forward tcp:5555 tcp:5555' if os.name == 'nt' else 'adb forward tcp:5555 tcp:5555') # This command sets up a line of data communication between the PC and the device 
    os.system(adb + ' shell cat /proc/partitions' if os.name == 'nt' else 'adb shell \'cat /proc/partitions\'') # This command shows a list of possible drives/partitions to make copies of
    print("Here is a list of partitions on the Android device. You can image individual partitions or you can image the entire drive. To image the entire drive, provide the name of the device that has the largest size.\n\n")
    print("What drive/partition should be imaged?\n")
    device = input("(drive/partition name): ")
    device = device.replace("/dev/","") # We assume that the user does not put the correct path to the device file. If they did, we strip out the path anyway
    imaging.getinfo.makedb(casefolder)
    p1 = multiprocessing.Process(target=sendcommand, args=(device, ))
    p1.start() #While sending the imaging command to the device...
    p2 = multiprocessing.Process(target=runstep2, args=(casefolder, ))
    p2.start() #...Get the PC ready to receive the data
    time.sleep (13) # Waits for this to get ready and for the data to start flowing
    imagepath = os.path.join(casefolder, "image", "image.dd")
    imagesize = int(os.path.getsize(imagepath))
    time.sleep (2)
    while not os.path.getsize(imagepath) == imagesize: # Provides imaging progress information to the user as it copies. 
        imagesize = os.path.getsize(imagepath)
        imagesize_human = imagesize/1073741824
        imagesize_human = "%0.2f" % imagesize_human
        sys.stdout.write("\r" + imagesize_human + "GB transferred. ", )
        sys.stdout.flush()
        time.sleep(3)
    p2.join()

def sendcommand(device): #Sends the command over ADB to send the image data over the wire
    su = subprocess.Popen('adb shell su -c "echo \\"test\\""', shell=True, stdout=subprocess.PIPE).stdout.read() #This tests for the 'su' program on the Android device. It is a common method for using root access 
    su=str(su)
    su=su[2:6]
    if su != 'test':
        print("'su' was not found on the system. Assuming we do not need it") #'su' is not always required for root access
        found_su=False
    else:
        found_su=True
    if found_su == True: #The presence of su changes the command that gets sent to the device.
        os.system('adb shell "su -c \\"busybox nc -l -p 5555 -e dd if=/dev/block/' + device + '\\""')
    else:
        os.system('adb shell busybox nc -l -p 5555 -e dd if=/dev/block/' + device )

def runstep2(casefolder):
    imaging.step2.main(casefolder) #Runs the PC preparation functions

    
    
