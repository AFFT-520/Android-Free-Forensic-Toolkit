#!/bin/bash

loopnum=`kpartx -vrag $1/image/image.dd -p afft | grep -o -m 1 "/dev/loop." | sed 's/\/dev\/loop//g'`
echo $loopnum
loopsearch="loop${loopnum}afft*"
echo $loopsearch
find /dev/mapper/ -name "$loopsearch" | while read -r line;
do
echo $line    
foldername=$(echo $line | sed "s/\/dev\/mapper\///" | sed "s/loop${loopnum}afft/Partition\ /")
mkdir $1/mount/"$foldername"
mount $line $1/mount/"$foldername" -o ro,noexec,loop,noload
if [ $? -ne 0 ];
then
	rm -rf $1/mount/"$foldername"
fi
echo $loopnum > $1/mount/loopnum
done
rm -rf $1/mount/loop$loopnum
