#!/usr/bin/env python

import os, shutil, apsw

def extract(case, userdata):
	print("--> Extracting Google Maps bookmarks\n\n")
	if os.path.exists(os.path.join(userdata, "data", "com.google.android.apps.maps")):
		extractdir = os.path.join(case, "extracted data")
		if not os.path.exists(extractdir):
			os.makedirs(extractdir)
		extractdir = os.path.join(extractdir, "google-maps")
		if not os.path.exists(extractdir):
			os.makedirs(extractdir)
		extract_db_dir = os.path.join(extractdir, "db")
		if not os.path.exists(extract_db_dir):
			os.makedirs(extract_db_dir)
	
	
		sourcedb = os.path.join(userdata, "data", "com.google.android.apps.maps", "databases", "gmm_myplaces.db")
		destpath = os.path.join (case, "extracted data", "google-maps", "db", "gmm_myplaces.db")
		outpath = os.path.join (case, "extracted data", "google-maps", "gmm_myplaces.txt")

		source = shutil.copyfile(sourcedb, destpath)
		output = open(outpath, 'w', encoding='utf8')
		extractSQLconnect = apsw.Connection(destpath)
		SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select key_string, timestamp, latitude, longitude from sync_item")	
		output.close()
	else:
		print("--> Not extracting Google Maps data. Reason: Not found\n\n")


