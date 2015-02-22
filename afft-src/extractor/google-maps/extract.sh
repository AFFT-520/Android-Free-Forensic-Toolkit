#!/bin/bash

if [ ! -d $1/extracted\ data ]; then
mkdir $1/extracted\ data		#Makes required folders if they don't exist
fi
if [ ! -d $1/extracted\ data/google-maps ]; then
mkdir $1/extracted\ data/google-maps		#Makes required folders if they don't exist
fi

sqlite3 $2/data/com.google.android.apps.maps/databases/gmm_myplaces.db < /opt/afft/extractor/google-maps/bookmarked-locations.sql > $1/extracted\ data/google-maps/bookmarked-locations
