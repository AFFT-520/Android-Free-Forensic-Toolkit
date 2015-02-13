#!/bin/bash

cat $1/mount/mountinfo | while read line;
do
offset=$(echo $line | awk '{print $1}')
name=$(echo $line | awk '{print $2}')
offset=$(($offset*512))
mkdir $1/mount/$name
currentCount=$(sudo losetup -a | wc -l)
sudo losetup /dev/loop$currentCount $1/image/image.dd -r -o $offset
sudo mount /dev/loop$currentCount $1/mount/$name
if [ ! $? == 0 ]; then
rm -rf $1/mount/$name
sudo losetup -d /dev/loop$currentCount
fi
done
