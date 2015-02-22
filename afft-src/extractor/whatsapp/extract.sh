#!/bin/bash

if [ ! -d $1/extracted\ data ]; then		#Makes required folders if they don't exist
mkdir $1/extracted\ data
fi
if [ ! -d $1/extracted\ data/whatsapp ]; then
mkdir $1/extracted\ data/whatsapp
fi
#Copies over encrypted data and encryption key
sudo cp $2/data/com.whatsapp/files/key $1/extracted\ data/whatsapp/encryption-key		
sudo cp $2/media/0/WhatsApp/Databases/msgstore.db.crypt8 $1/extracted\ data/whatsapp/
#Extracts vital encryption info 
k=$(hexdump -e '2/1 "%02x"' $1/extracted\ data/whatsapp/encryption-key | cut -b 253-316)
iv=$(hexdump -e '2/1 "%02x"' $1/extracted\ data/whatsapp/encryption-key | cut -b 221-252)
#Removes the header of the encrypted database
dd if=$1/extracted\ data/whatsapp/msgstore.db.crypt8 of=$1/extracted\ data/whatsapp/msgstore.db.crypt8.nohdr ibs=67 skip=1
#Decrypts header-removed database using the key and $k , $iv variables
openssl enc -aes-256-cbc -d -nosalt -bufsize 16384 -in $1/extracted\ data/whatsapp/msgstore.db.crypt8.nohdr -K $k -iv $iv | gunzip > $1/extracted\ data/whatsapp/msgstore.db
#Grabs data from decrypted database
sqlite3 $1/extracted\ data/whatsapp/msgstore.db < /opt/afft/extractor/whatsapp/extract.sql > $1/extracted\ data/whatsapp/messages.txt
#Copies over cache data
cp -rf $2/media/0/WhatsApp/Media/ $1/extracted\ data/whatsapp/
cp -rf $2/media/0/WhatsApp/Profile\ Pictures/ $1/extracted\ data/whatsapp/
