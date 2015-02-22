#!/bin/bash

if [ ! -d $1/extracted\ data/ ]; then			# Make directories if they don't already exist
mkdir $1/extracted\ data/
fi
if [ ! -d $1/extracted\ data/calendar ]; then			# Make directories if they don't already exist
mkdir $1/extracted\ data/calendar
fi
sqlite3 $2/data/com.android.providers.calendar/databases/calendar.db 'select distinct account_name from calendars;' | while read account; do
	if [ ! -d $1/extracted\ data/calendar/$account ]; then			# Make directories if they don't already exist
	mkdir $1/extracted\ data/calendar/$account
	fi
	if [ ! -d $1/extracted\ data/calendar/$account/sql ]; then			# Make directories if they don't already exist
	mkdir $1/extracted\ data/calendar/$account/sql
	fi
	echo ".header on" > $1/extracted\ data/calendar/$account/sql/calendarlist.sql
	echo "select * from calendars where account_name = '$account';" >> $1/extracted\ data/calendar/$account/sql/calendarlist.sql
	sqlite3 $2/data/com.android.providers.calendar/databases/calendar.db < $1/extracted\ data/calendar/$account/sql/calendarlist.sql > $1/extracted\ data/calendar/$account/calendarlist.txt
	sqlite3 $2/data/com.android.providers.calendar/databases/calendar.db "select name from calendars where account_name = '$account'" | while read calendar; 
			do			
			mkdir $1/extracted\ data/calendar/$account/"$calendar";
			sqlite3 $2/data/com.android.providers.calendar/databases/calendar.db "select _id from calendars where name = '$calendar' AND account_name = '$account';" | while read calID; do
				echo ".header on" > $1/extracted\ data/calendar/$account/sql/$calID.sql
				echo "select * from events where calendar_id = '$calID';" > $1/extracted\ data/calendar/$account/sql/$calID.sql
				sqlite3 $2/data/com.android.providers.calendar/databases/calendar.db < $1/extracted\ data/calendar/$account/sql/$calID.sql > $1/extracted\ data/calendar/$account/"$calendar"/calID.$calID.events.txt
				done
			done
	done

