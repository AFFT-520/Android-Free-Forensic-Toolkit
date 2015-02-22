#!/bin/bash

function getuserdatapartition () {
echo "Please provide the full path to the root of the mounted user data partition (usually called 'userdata')"
read userdata
echo $userdata > $1/image/userdata-name.txt
} 


function mac () {		#prints notice for OSX users, informing of limitations
	clear
	echo "NOTICE FOR MAC OSX USERS"
	echo "-------------------------"
	echo ""
	echo "AFFT has detected that you are running this tool under Mac OSX. OSX does not have native support for Ext3/4 to extract user data using the toolkit alone. As such, the option to mount the Android image partitions are not available from this toolkit."
	echo ""
	echo "You may, however, use a third party mounting tool to compensate. If you do not have one already, we recommend downloading FTK Imager for Mac for this task, but you may use whichever tool you prefer. If you choose to do this, please provide the path to the root of the user data partition (usually named 'userdata')"
	echo ""
	echo "How would you like to proceed?"
	echo ""
	echo "1) Enable user data extraction. I will provide the path to the userdata partition "
	echo "2) Disable user data extraction options"
 	read option
	case $option in 
	1) 
	noextract=0;
	;;
	2) 
	noextract=1;
	;;
	*) mac;
	;;
	esac
}

function windows () {			#prints notice for Windows users, informing of limitations
	clear
	echo "NOTICE FOR WINDOWS USERS"
	echo "-------------------------"
	echo ""
	echo "AFFT has detected that you are running this tool under Windows. Windows does not have either the necessary loopback interfaces or native support for Ext3/4 to extract user data using the toolkit alone. As such, the option to mount the Android image partitions are not available from this toolkit."
	echo ""
	echo "You may, however, use a third party mounting tool to compensate. If you do not have one already, we recommend downloading FTK Imager for this task, but you may use whichever tool you prefer. If you choose to do this, please provide the path to the root of the user data partition (usually named 'userdata')"
	echo ""
	echo "How would you like to proceed?"
	echo ""
	echo "1) Enable user data extraction. I will provide the path to the userdata partition "
	echo "2) Disable user data extraction options"
 	read option
	case $option in 
	1) 
	noextract="0";
	;;
	2) 
	noextract="1";
	;;
	*) windows;
	;;
	esac
}

function menulinux () {
echo "Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne"			# Displays the operation menu
echo "-----------------------------------------------"
echo ""
echo "The case files can be found in $casefolder"
echo ""
echo "Select an option:"
echo "1) Retrieve or import a whole-system image from device"
echo "2) Mount Android images (where possible)"
echo "3) Obtain communication dumps"
echo "4) Unmount Android images and perform cleanup"
echo "5) Repair Android images (WARNING: Alters image)"
echo "6) Disable lock-screen security on device"
echo "7) Exit"
read -n 1 option
echo ""
case "$option" in				# This part onwards manages selection

1) echo "Proceed to image dump"
mkdir $casefolder/image
/opt/afft/imaging/source.sh $casefolder
clear
menulinux
;;
2) echo "Mounting Android partitions"
mountingfolder="$casefolder/mount"
if [ ! -d $mountingfolder ]; then
mkdir $mountingfolder
fi
/opt/afft/mounter/mount.sh $casefolder
clear
menulinux
;;
3) echo "Proceed to communication data extraction"
/opt/afft/extractor/extractor.sh $casefolder
clear
menulinux
;;
4) echo "Proceeding to unmount image"
/opt/afft/mounter/unmount.sh $casefolder
clear
menulinux
;;
5) 
echo "Mounting images for filesystem repair"
/opt/afft/mounter/repair.sh $casefolder
clear
menulinux
;;
6)
/opt/afft/lockscreen/lockscreen.sh
clear
menulinux
;;
7)
clear
exit
;;
*)
menulinux
;;
esac
}

function menuotheros () {
echo "Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne"			# Displays the operation menu
echo "-----------------------------------------------"
echo ""
echo "The case files can be found in $casefolder"
echo ""
echo "Select an option:"
echo "1) Retrieve a whole-system image from device"
echo "2) Obtain communication dumps"
echo "3) Disable lock-screen security on device"
echo "4) Exit"
read -n 1 option
echo ""
case "$option" in				# This part onwards manages selection

1) echo "Proceed to image dump"
imagingfolder="$casefolder/image"
mkdir $imagingfolder
/opt/afft/imaging/step1.sh $imagingfolder
clear
menuotheros
;;
2) echo "Proceed to communication data extraction"
/opt/afft/extractor/extractor.sh $casefolder
clear
menuotheros
;;
3)
/opt/afft/lockscreen/lockscreen.sh
clear
menuotheros
;;
4)
clear
exit
;;
*)
menuotheros
;;
esac
}

function menuotheros_noextract () {
echo "Android Free Forensic Toolkit - Alpha Build - (C) Conor Rynne"			# Displays the operation menu
echo "-----------------------------------------------"
echo ""
echo "The case files can be found in $casefolder"
echo ""
echo "Select an option:"
echo "1) Retrieve a whole-system image from device"
echo "2) Disable lock-screen security on device"
echo "3) Exit"
read -n 1 option
echo ""
case "$option" in				# This part onwards manages selection

1) echo "Proceed to image dump"
imagingfolder="$casefolder/image"
mkdir $imagingfolder
/opt/afft/imaging/step1.sh $imagingfolder 
clear
menuotheros_noextract
;;
2)
/opt/afft/lockscreen/lockscreen.sh
clear
menuotheros_noextract
;;
3)
clear
exit
;;
*)
menuotheros_noextract
;;
esac
}





clear
/opt/afft/legal-prompt.sh
source /opt/afft/sethome.sh
sudo /opt/afft/extractor/update-extractor.sh
echo "Please provide the directory name for the case items"
read phonecase
if [ ! -d $AFFTRootDir/afft-cases ]; then
	mkdir $AFFTRootDir/afft-cases ];		# If the case directories don't exist, create them
fi
if [ ! -d $AFFTRootDir/afft-cases/$phonecase ]; then
	mkdir $AFFTRootDir/afft-cases/$phonecase
fi
casefolder="$AFFTRootDir/afft-cases/$phonecase"	# This is the operating directory of the functions. It gets passed as an argument to each one 							where needed

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
	windows
	if [ $noextract == "0" ]; then
		clear
		getuserdatapartition
		menuotheros 
	elif [ $noextract == "1" ]; then
		clear
		menuotheros_noextract
	fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
	mac
	if [ $noextract == "0" ]; then
		clear
		getuserdatapartition
		menuotheros
	elif [ $noextract == "1" ]; then
		clear
		menuotheros_noextract
	fi
else
	menulinux
fi
