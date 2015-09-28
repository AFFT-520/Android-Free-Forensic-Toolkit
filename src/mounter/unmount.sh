#!/bin/bash

umount $1/mount/*
sleep 2
loopnum=$(cat $1/mount/loopnumber)
rm -rf $1/mount/*
kpartx -d $1/image/image.dd
ls /dev/mapper/loop[$loopnum]afft* | while read -r line;
do
  device=$(echo $line | sed 's/\/dev\/mapper\///g')
  sudo dmsetup remove $device
done
echo 0 > "$1/mount/mountstatus"
