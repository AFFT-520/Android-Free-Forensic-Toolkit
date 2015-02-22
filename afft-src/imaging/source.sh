#!/bin/bash

directory=$1
function menu () {
	clear
	echo "Do you wish to acquire an image directly from an Android device or import an existing one?

A) Acquire an image from a device
I) Import a pre-existing image for use with AFFT
R) Return to the main menu"

	read -n 1 answer
	answer=$(echo $answer | tr '[:upper:]' '[:lower:]')
	case "$answer" in
	a) /opt/afft/imaging/step1.sh $directory/image/;
	;;
	i) /opt/afft/mounter/import.sh $directory;
	;;
	r) return 0;
	;;	
	*) menu;
	;;
	esac
}
menu
