#!/bin/bash

function sethome () {
	echo "AFFT has not been configured with a root directory yet, and must be set up with one before continuing. The root directory will hold all your AFFT case files under a sub-directory called \"afft-cases\""
	echo ""
	echo "You can set a custom one or you can leave it as default (the home directory, in this case it is $HOME)."
	echo ""
	echo "Type in the location where you'd like to store case files, or press Enter to leave as default"
	read answer
	if [ -z $answer ]; then
		answer=$HOME
	fi
	grep -q "AFFTRootDir" $HOME/.afft 
	if [ $? -ne 0 ]; then
		echo "AFFTRootDir=$answer" >> $HOME/.afft
	else	
		sed -n -i "s/AFFTRootDir=.*/AFFTRootDir=$answer/" $HOME/.afft
		
	fi
	
	cat $HOME/.afft
}


if [ -f $HOME/.afft ]; then
grep -q "AFFTRootDir=" $HOME/.afft
if [ $? -ne 0 ]; then
sethome
fi
else
sethome
fi
value=$(grep "AFFTRootDir=.*" $HOME/.afft)
export $value
