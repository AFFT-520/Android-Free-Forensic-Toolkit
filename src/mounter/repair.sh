#!/bin/bash

cat $1/mount/mountinfo | while read line;
do
offset=$(echo $line | awk '{print $1}')
name=$(echo $line | awk '{print $2}')
offset=$(($offset*512))
mkdir $1/mount/$name &> /dev/null
currentCount=$(sudo losetup -a | wc -l)
sudo losetup /dev/loop$currentCount $1/image/image.dd -o $offset &> /dev/null
sudo mount /dev/loop$currentCount $1/mount/$name &> /dev/null
if [ ! $? == 0 ]; then
rm -rf $1/mount/$name &> /dev/null
sudo losetup -d /dev/loop$currentCount &> /dev/null
fi
done

