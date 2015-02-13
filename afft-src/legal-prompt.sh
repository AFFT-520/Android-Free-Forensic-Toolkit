#!/bin/bash

function disclaimer {
	echo "LEGAL DISCLAIMER"
	echo ""
	echo "This program is provided under the understanding that it is to be used on devices only for purposes where lawful authorisation is in place (including but not limited to: your own device, a device for which you have express and fully-informed permission from the owner, a device for which you have a valid subpoena regarding it's data, etc). By using this program, you hereby state that you understand this and accept any consequences that arise from the use of this tool, and that neither the program's authour or contributors are responsible for your use of the tool."
	echo ""
	echo "Do you agree to these conditions?[Y/N]"
	read -n 1 answer
	answer=$(echo $answer | tr '[:upper:]' '[:lower:]')
	if [ $answer == "y" ]; then
		clear
		echo "read-disclaimer == 1" > $HOME/.afft
	elif [ $answer == "n" ]; then
		clear		
		exit
	else
		clear
		disclaimer
	fi
}


if [ -f $HOME/.afft ]; then
grep "read-disclaimer == 1" $HOME/.afft > /dev/zero
if [ $? -ne 0 ]; then
disclaimer
fi
else
disclaimer
fi
