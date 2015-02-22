#!/bin/bash
if [ ! -d $1/extracted\ data ]; then			#Makes required folders if they don't exist
mkdir $1/extracted\ data
fi
if [ ! -d $1/extracted\ data/facebook ]; then
mkdir $1/extracted\ data/facebook
fi
if [ ! -d $1/extracted\ data/facebook/messages ]; then
mkdir $1/extracted\ data/facebook/messages
fi
if [ ! -d $1/extracted\ data/facebook-messenger ]; then
mkdir $1/extracted\ data/facebook-messenger
fi
if [ ! -d $1/extracted\ data/facebook-messenger/messages ]; then
mkdir $1/extracted\ data/facebook-messenger/messages
fi

#Grabs data from the various databases
sqlite3 $2/data/com.facebook.katana/databases/threads_db2 < /opt/afft/extractor/facebook/messages.sql > $1/extracted\ data/facebook/messages/message-dump.txt
sqlite3 $2/data/com.facebook.katana/databases/contacts_db2 < /opt/afft/extractor/facebook/contacts.sql > $1/extracted\ data/facebook/contacts-info.txt
sqlite3 $2/data/com.facebook.katana/databases/notifications_db < /opt/afft/extractor/facebook/notifications.sql > $1/extracted\ data/facebook/notification-log.txt
sqlite3 $2/data/com.facebook.orca/databases/threads_db2 < /opt/afft/extractor/facebook/messages.sql > $1/extracted\ data/facebook-messenger/messages/message-dump.txt
sqlite3 $2/data/com.facebook.orca/databases/call_log.sqlite < /opt/afft/extractor/facebook/fb-call-log.sql > $1/extracted\ data/facebook-messenger/call-log.txt

#Copies data from Facebook's cache
cp -rf $2/data/com.facebook.katana/cache $1/extracted\ data/facebook
cp -rf $2/data/com.facebook.katana/files $1/extracted\ data/facebook
cp -rf $2/data/com.facebook.orca/cache $1/extracted\ data/facebook-messenger
cp -rf $2/data/com.facebook.orca/files $1/extracted\ data/facebook-messenger
