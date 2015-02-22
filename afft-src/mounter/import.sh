#!/bin/bash

clear
echo "To import your device image into AFFT, move the file into $1/image/. Make sure it is the ONLY file in that directory. Once done, press enter and AFFT will do the rest.

AFFT only supports raw images. This means images made in proprietary formats or some other compresion algorithm will not work.

Press Enter when you are ready"

read placebo		# We're not actually doing anything with this, it's just to make the script stop until the user is ready

find $1/image/* | while read imagefile; do
file $imagefile | grep 'x86 boot sector'	#Images appear to identify themselves as x86 boot sectors. If anybody has a better way of identifying images, please let me know or edit this
if [ $? == 0 ]; then
echo "test"
	gdisk -l $imagefile > $1/image/partitioninfo # gets partition info from the image. We'll need this for mounting the files later
	cat $1/image/partitioninfo | awk 'f;/Number/{f=1}' > $1/image/tmpdata # strips the header from the data, makes parsing via script much easier.
	cat $1/image/tmpdata | awk '{print $2, $7}' > $1/mount/mountinfo # alters the partition info file to include info only useful to the mounting script
	rm $1/image/tmpdata
fi
done
echo "Done! Is the user data partition called 'userdata'? If not, type in the name"	#gets the name of the userdata partition, incase it isn't the default
read userdata
if [ -z $userdata ]; then
	userdata="$1/mount/userdata"
fi
echo $userdata > $1/image/userdata-name.txt
