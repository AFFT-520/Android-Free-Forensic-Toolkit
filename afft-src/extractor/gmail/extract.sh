#!/bin/bash

if [ ! -d $1/extracted\ data/ ]; then		#Makes required folders if they don't exist
mkdir $1/extracted\ data/
fi
if [ ! -d $1/extracted\ data/gmail ]; then
mkdir $1/extracted\ data/gmail/
fi
ourPath=$(pwd)
ls -1 $2/data/com.google.android.gm/databases | grep -e "mailstore" | grep -v "db-wal" | grep -v "db.shm" | while read -r accountdb;					#Finds the required databases
do
account=$(echo $accountdb | sed 's/mailstore.//' | sed 's/.db//')	#Obtains the registered account name from the database name...
mkdir $1/extracted\ data/gmail/$account					#...and creates a folder structure for that account
mkdir $1/extracted\ data/gmail/$account/db
cp $2/data/com.google.android.gm/databases/$accountdb $1/extracted\ data/gmail/$account/db/mailstore.db #Copies over the mailstore database for that account
chmod 755 $1/extracted\ data/gmail/$account/db/mailstore.db 		#Gives us full read permissions to the database
sqlite3 $1/extracted\ data/gmail/$account/db/mailstore.db < /opt/afft/extractor/gmail/messages.sql > $1/extracted\ data/gmail/$account/messages 								#Extracts the data from that database
done
