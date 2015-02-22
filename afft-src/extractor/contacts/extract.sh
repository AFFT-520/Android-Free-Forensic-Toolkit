#!/bin/bash
if [ ! -d $1/extracted\ data ]; then		#Makes required folders if they don't exist
mkdir $1/extracted\ data/
fi
if [ ! -d $1/extracted\ data/contacts/ ]; then
mkdir $1/extracted\ data/contacts/
fi
sudo sqlite3 $2/data/com.android.providers.contacts/databases/contacts2.db < /opt/afft/extractor/contacts/extract.sql > $1/extracted\ data/contacts/contactslist.txt	#Grabs data from the database
