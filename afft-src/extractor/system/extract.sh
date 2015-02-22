#!/bin/bash


if [ ! -d $1/extracted\ data/ ]; then		#Makes required folders if they don't exist
mkdir $1/extracted\ data/
fi

if [ ! -d $1/extracted\ data/system ]; then		
mkdir $1/extracted\ data/system
fi

if [ ! -d $1/extracted\ data/system/vpn ]; then		
mkdir $1/extracted\ data/system/vpn
fi

cp $2/misc/wifi/wpa_supplicant.conf $1/extracted\ data/system/wifi\ details.txt
cp $2/misc/adb/adb_keys $1/extracted\ data/system/
cp $2/misc/bluedroid/bt_config.xml $1/extracted\ data/system/bluetooth-pairings.txt
cp -rf $2/misc/vpn $1/extracted\ data/system/

