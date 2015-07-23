#!/bin/bash

umount $1/mount/*
rm -rf $1/mount/*
kpartx -d $1/image/image.dd
echo 0 > "$1/mount/mountstatus"
