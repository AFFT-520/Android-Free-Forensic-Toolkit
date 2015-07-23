#!/usr/bin/env python

import os, shutil, apsw, distutils.dir_util

def extract(case, userdata):
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "calendar")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	dbdir = os.path.join(extractdir, "db")
	if not os.path.exists(dbdir):
		os.makedirs(dbdir)
	
	print("--> Extracting Google Calendar databases\n\n")
	try:
		sourcedb = os.path.join(userdata, "data", "com.android.providers.calendar", "databases", "calendar.db")
		destpath = os.path.join (dbdir, "calendar.db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy calendar database ! ")

	sql(destpath, extractdir)

def sql(database, extractdir):
	
	dbconnection=apsw.Connection(database)
	dbcursor1=dbconnection.cursor()
	dbcursor2=dbconnection.cursor()
	dbcursor3=dbconnection.cursor()
	errors = 0

	for row in dbcursor1.execute("select distinct account_name from calendars"):
		for entry1 in row:
			accountdir = os.path.join(extractdir, str(entry1))		
			if not os.path.exists(accountdir):
				os.makedirs(accountdir)	

			for row2 in dbcursor2.execute("select name from calendars where account_name = '" + str(entry1) + "'"):
				for entry2 in row2:	
					caldir = os.path.join(accountdir, str(entry2))		
					if not os.path.exists(caldir):
						os.makedirs(caldir)	
					for row3 in dbcursor3.execute("select _id from calendars where name = '" + str(entry1) + "' AND account_name = '" + str(entry2) + "'"):
						for entry3 in row3:
							filepath = os.path.join(caldir, "Events.txt")
							eventfile = open(filepath, "w", encoding='utf8')
							SQLShell = apsw.Shell(stdout=eventfile, db=dbconnection)
							try:
								SQLShell.process_command(".header on")
								SQLShell.process_sql("select * from events where calendar_id = " + str(entry3))
							except Exception:
								print("Error: Could not process " + str(entry1) + " in " + str(entry2) + ".")
								errors = errors + 1
							eventfile.close()
	if not errors == 0:
		print(errors +" error(s) occured in the extraction process!")


