#!/usr/bin/env python

import os
import fileinput

def sethome ():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("AFFT has not been configured with a root directory yet, and must be set up with one before continuing. The root directory will hold all your AFFT case files under a sub-directory called " + os.path.sep + "afft-cases" + os.path.sep + "\n")
    homepath = os.path.expanduser("~")
    print("You can set a custom one or you can leave it as default (the home directory. In this case it is " + homepath + ").\n")
    print("Type in the location where you'd like to store case files, or press Enter to leave as default")
    answer = input()
    if answer == "":
        answer = homepath

    settingsfile = os.path.join(homepath, ".afft-py")
    if not os.path.isfile(settingsfile):
        opensetts = open(settingsfile, 'w+')
        opensetts.write("AFFTRootDir=" + answer + "\n")
        opensetts.close()
    else:
        afftline = "AFFTRootDir="
        if afftline in open(settingsfile).read():
                for line in fileinput.input(settingsfile, inplace=True):
                    print(afftline.replace("AFFTRootDir=","AFFTRootDir=" + answer + "\n"), end='')
        else:
            opensetts = open(settingsfile, 'a')
            opensetts.write("AFFTRootDir=" + answer + "\n")
            opensetts.close()

def main ():
    homepath = os.path.expanduser("~")
    settingsfile = os.path.join(homepath, ".afft-py")
    if os.path.isfile(settingsfile):
        afftline = "AFFTRootDir="
        settfile = open(settingsfile)
        for line in settfile:
            if afftline in line:
                address = line.replace("AFFTRootDir=", "")
                address = address.replace("\n", "")
                if address == "":
                    sethome()
                return address
        else:
            sethome()
    else:
        sethome()
main()
