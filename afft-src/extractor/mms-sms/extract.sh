#!/bin/bash
if [ ! -d $1/extracted\ data ]; then
mkdir $1/extracted\ data		#Makes required folders if they don't exist
fi
if [ ! -d $1/extracted\ data/sms/ ]; then
mkdir $1/extracted\ data/sms/		
fi
sudo sqlite3 $2/data/com.android.providers.telephony/databases/mmssms.db < /opt/afft/extractor/mms-sms/extract.sql > $1/extracted\ data/sms/dump.txt		#Extracts the data from the database
