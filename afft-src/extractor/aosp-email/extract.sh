#!/bin/bash

if [ ! -d $1/extracted\ data/ ]; then		#Makes required folders if they don't exist
mkdir $1/extracted\ data/
fi

if [ ! -d $1/extracted\ data/aosp-email ]; then		
mkdir $1/extracted\ data/aosp-email
fi

if [ ! -d $1/extracted\ data/aosp-email/metadata ]; then		
mkdir $1/extracted\ data/aosp-email/metadata
fi

if [ ! -d $1/extracted\ data/aosp-email/body ]; then		
mkdir $1/extracted\ data/aosp-email/body
fi

sqlite3 $2/data/com.android.email/databases/EmailProvider.db < /opt/afft/extractor/aosp-email/gettables.sql | while read -r line;												#cycle through the tables
do
echo ".header on" >> $1/extracted\ data/aosp-email/metadata/$line.sql
echo "select * from $line;" > $1/extracted\ data/aosp-email/metadata/$line.sql			#make a temporary SQL file for the selected table
sqlite3 $2/data/com.android.email/databases/EmailProvider.db < $1/extracted\ data/aosp-email/metadata/$line.sql > $1/extracted\ data/aosp-email/metadata/$line.txt								#executes the SQL file on the table
rm $1/extracted\ data/aosp-email/metadata/$line.sql						#removes the temporary file
done
echo ".header on" >> $1/extracted\ data/aosp-email/body/body.sql
echo "select * from body;" > $1/extracted\ data/aosp-email/body/body.sql			#makes a temporary SQL file for the 'body' database
sqlite3 $2/data/com.android.email/databases/EmailProviderBody.db < $1/extracted\ data/aosp-email/body/body.sql > $1/extracted\ data/aosp-email/body/body.txt									#executes it
rm $1/extracted\ data/aosp-email/body/body.sql							#removes it
