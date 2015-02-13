#!/bin/bash
clear
/opt/afft/legal-prompt.sh
echo "Please provide the directory name for the case items"
read phonecase
if [ ! -d $HOME/afft-cases ]; then
	mkdir $HOME/afft-cases ];		# If the case directories don't exist, create them
fi
if [ ! -d $HOME/afft-cases/$phonecase ]; then
	mkdir $HOME/afft-cases/$phonecase
fi
casefolder="$HOME/afft-cases/$phonecase"	# This is the operating directory of the functions. It gets passed as an argument to each one 							where needed
function menu () {
echo "Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne"			# Displays the operation menu
echo "-----------------------------------------------"
echo ""
echo "The case files can be found in $casefolder"
echo ""
echo "Select an option:"
echo "1) Retrieve a whole-system image from device"
echo "2) Mount Android images (where possible)"
echo "3) Obtain communication dumps"
echo "4) Unmount Android images and perform cleanup"
echo "5) Repair Android images (WARNING: Alters image)"
echo "6) Exit"
read option
case "$option" in				# This part onwards manages selection

1) echo "Proceed to image dump"
imagingfolder="$casefolder/image"
mkdir $imagingfolder
/opt/afft/imaging/step1.sh $imagingfolder
clear
menu
;;
2) echo "Mounting Android partitions"
mountingfolder="$casefolder/mount"
if [ ! -d $mountingfolder ]; then
mkdir $mountingfolder
fi
/opt/afft/mounter/mount.sh $casefolder
clear
menu
;;
3) echo "Proceed to communication data extraction"
/opt/afft/extractor/extractor.sh $casefolder
clear
menu
;;
4) echo "Proceeding to unmount image"
/opt/afft/mounter/unmount.sh $casefolder
clear
menu
;;
5) 
echo "Mounting images for filesystem repair"
/opt/afft/mounter/repair.sh $casefolder
clear
menu
;;
6)
clear
exit
;;
esac
}

menu
