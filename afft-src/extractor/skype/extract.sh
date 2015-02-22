#!/bin/bash

skypeDir=$2/data/com.skype.raider/
ourDir=$(pwd)
find $skypeDir -name "main.db" | while read db; do	#Finds every instance of 'main.db' in the Skype folder; these have the data we need
goto=$(echo $db | sed 's/main.db//')
cd $goto
username=$(printf '%s\n' "${PWD##*/}")			#Gets the Skype username pertaining to the currently-selected database
cd $ourDir
if [ ! -d $1/:extracted\ data/ ]; then
mkdir $1/extracted\ data/
fi
if [ ! -d $1/extracted\ data/skype ]; then		#Makes required folders if they don't exist, including those pertaining to individual usernames
mkdir $1/extracted\ data/skype
fi
if [ ! -d $1/extracted\ data/skype/$username ]; then
mkdir $1/extracted\ data/skype/$username
fi
mkdir $1/extracted\ data/skype/$username/sqlcommands/
sqlite3 $skypeDir/files/$username/main.db < /opt/afft/extractor/skype/gettables.sql | while read tname; do #Gets list of tables in the database...
echo ".header on" > $1/extracted\ data/skype/$username/sqlcommands/$tname.sql	#...and crafts SQL scripts for each one, basically to dump everything, headers included
echo "select * from $tname;" >> $1/extracted\ data/skype/$username/sqlcommands/$tname.sql
sqlite3 $skypeDir/files/$username/main.db < $1/extracted\ data/skype/$username/sqlcommands/$tname.sql > $1/extracted\ data/skype/$username/$tname										#...and executes that script
done
rm -rf $1/extracted\ data/skype/$username/sqlcommands/				#Cleans up generated SQL scripts 
done

