#!/bin/bash

adb forward tcp:5555 tcp:5555
adb shell 'cat /proc/partitions' # gives the user a list of drives/partitions on the Android device
echo ""
echo "Here is a list of partitions on the Android device. You can image individual partitions or you can image the entire drive. To image the entire drive, provide the name of the device that has the largest size."
function pickdevice () {
echo "What device should be imaged?"
read device # gets the name of the desired device from the user
device=$(echo $device | sed 's/\/dev//')
}
pickdevice
adb shell "su -c \"/system/xbin/busybox nc -l -p 5555 -e /system/xbin/busybox dd if=/dev/block/$device\"" & /opt/afft/imaging/step2.sh $1 # executes the imaging command on the device, and goes to the next part on the PC
