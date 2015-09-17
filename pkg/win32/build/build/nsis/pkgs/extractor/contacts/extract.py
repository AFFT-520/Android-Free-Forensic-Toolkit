#!/usr/bin/env python

import os, shutil, apsw

def extract(case, userdata):
	print("--> Extracting contacts database\n\n")
	if os.path.exists(os.path.join(userdata, "data", "com.android.providers.contacts", "databases", "contacts2.db")):
		extractdir = os.path.join(case, "extracted data")
		if not os.path.exists(extractdir):
			os.makedirs(extractdir)
		extractdir = os.path.join(extractdir, "contacts")
		if not os.path.exists(extractdir):
			os.makedirs(extractdir)
		extract_db_dir = os.path.join(extractdir, "db")
		if not os.path.exists(extract_db_dir):
			os.makedirs(extract_db_dir)
	
	
		sourcedb = os.path.join(userdata, "data", "com.android.providers.contacts", "databases", "contacts2.db")
		destpath = os.path.join (case, "extracted data", "contacts", "db", "contacts2.db")
		outpath = os.path.join (case, "extracted data", "contacts", "contactslist.txt")

		source = shutil.copyfile(sourcedb, destpath)
		output = open(outpath, 'w', encoding='utf8')
		extractSQLconnect = apsw.Connection(destpath)
		SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
		SQLShell.process_command(".header on")
		try:
			SQLShell.process_sql("select * from view_contacts as R join phone_lookup as C on C.raw_contact_id=R.name_raw_contact_id")
		except apsw.SQLError:
			SQLShell.process_sql("select * from view_contacts as R join phone_lookup as C on C.raw_contact_id=R.name_raw_contact_id")		
		output.close()

	else:
		print("!!> Not extracting contacts data. Reason: Not found\n\n")


