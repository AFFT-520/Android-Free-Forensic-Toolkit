#!/bin/bash

sudo losetup -a | grep -e "$1" -e "/image/image.dd" | awk '{print $1}' | sed 's/://' | while read line; do
sudo umount $line
sudo losetup -d $line
done
sudo umount $1/mount/* #Incase the above didnt work
find $1/mount/* -maxdepth 0 -empty -exec rm -rf {} \;
