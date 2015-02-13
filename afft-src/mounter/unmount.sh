#!/bin/bash

sudo losetup -a | grep -e "$1" -e "/image/image.dd" | awk '{print $1}' | sed 's/://' | while read line; do
sudo umount $line
sudo losetup -d $line
done
cat $1/mount/mountinfo | awk '{print $2}' | while read line; do
rm -rf $1/mount/$line
done
