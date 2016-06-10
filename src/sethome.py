#!/usr/bin/env python

import os
import fileinput

def sethome (): #Guides the user through setting up the directory for holding their case files. Default is the user's home directory, but this is changeable.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("AFFT has not been configured with a root directory yet, and must be set up with one before continuing. The root directory will hold all your AFFT case files under a sub-directory called " + os.path.sep + "afft-cases" + os.path.sep + "\n")
    homepath = os.path.expanduser("~")
    print("You can set a custom one or you can leave it as default (the home directory. In this case it is " + homepath + ").\n")
    print("Type in the location where you'd like to store case files, or press Enter to leave as default")
    answer = input()
    if answer == "": #If the answer is blank, just go with the default
        answer = homepath

    settingsfile = os.path.join(homepath, ".afft-py")
    if not os.path.isfile(settingsfile): #If the settings file doesn't exist, make one.
        opensetts = open(settingsfile, 'w+')
        opensetts.write("AFFTRootDir=" + answer + "\n")
        opensetts.close()
    else: #If it does, find the line that has the case file root directory and update it.
        afftline = "AFFTRootDir="
        if afftline in open(settingsfile).read():
                for line in fileinput.input(settingsfile, inplace=True):
                    print(afftline.replace("AFFTRootDir=","AFFTRootDir=" + answer + "\n"), end='')
        else: #If the line doesnt exist, create it 
            opensetts = open(settingsfile, 'a')
            opensetts.write("AFFTRootDir=" + answer + "\n")
            opensetts.close()

def main (): #Checks the settings file for the root directory. If the file doesn't exist or the line doesn't, guide the user through creating it.
    homepath = os.path.expanduser("~")
    settingsfile = os.path.join(homepath, ".afft-py")
    if os.path.isfile(settingsfile):
        afftline = "AFFTRootDir="
        settfile = open(settingsfile)
        for line in settfile:
            if afftline in line: #Finds the line that has the info, and parses it for the programs use. If the field is empty, send the user through the guide to make a proper one.
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
