#!/usr/bin/env python

import os, fileinput, sys

def legalprompt ():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("LEGAL DISCLAIMER\n\n")
    print("This program is provided under the understanding that it is to be used on devices only for purposes where lawful authorisation is in place (including but not limited to: your own device, a device for which you have express and fully-informed permission from the owner, a device for which you have a valid subpoena regarding it's data, etc). By using this program, you hereby state that you understand this and accept any consequences that arise from the use of this tool, and that neither the program's authour or contributors are responsible for your use of the tool.\n\n")
    answer = input("Do you agree to these conditions?[Y/N]")
    
    if answer in ('y', 'Y'):
        settingsfile = os.path.join(os.path.expanduser("~"), ".afft-py")
        if not os.path.isfile(settingsfile):
            opensetts = open(settingsfile, 'w+')
            opensetts.write("ReadDisclaimer=1\n")
            opensetts.close()
        else:
            afftline = "ReadDisclaimer=1"
            if afftline in open(settingsfile).read():
                for line in fileinput.input(settingsfile, inplace=True):
                    print(afftline + "\n", end='')
            else:
                opensetts = open(settingsfile, 'a')
                opensetts.write("ReadDisclaimer=1" + "\n")
                opensetts.close()
    elif answer in ('n', 'N'):
        sys.exit()
    else:
        legalprompt ()
        
def main ():
    homepath = os.path.expanduser("~")
    settingsfile = os.path.join(homepath, ".afft-py")
    if os.path.isfile(settingsfile):
        afftline = "ReadDisclaimer=1"
        settfile = open(settingsfile)
        for line in settfile:
            if afftline in line:
                return (0)
        else:
            legalprompt()
    else:
        legalprompt()
main()