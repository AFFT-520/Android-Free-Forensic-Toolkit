#!/usr/bin/env python

import os, distutils.dir_util, apsw, shutil


def extract(case, userdata):

	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "skype")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	
	path = os.path.join(userdata, "data", "com.skype.raider", "files")
	print("--> Extracting Skype information\n\n")
	for dirname in next(os.walk(path))[1]:
		if os.path.isfile(os.path.join(path, dirname, "main.db")):
			accdir = os.path.join(extractdir, dirname)
			if not os.path.exists(accdir):
				os.makedirs(accdir)

			dbdir = os.path.join(accdir, "db")
			if not os.path.exists(dbdir):
				os.makedirs(dbdir)	

			outputdir = os.path.join(accdir, "output")		
			if not os.path.exists(outputdir):
				os.makedirs(outputdir)	
			
			source = os.path.join(path, dirname, "main.db")
			dest = os.path.join(dbdir, "main.db")
			shutil.copyfile(source, dest)

			sql(dest, outputdir)

def sql(database, extractdir):
	
	dbconnection=apsw.Connection(database)
	dbcursor1=dbconnection.cursor()
	errors = 0

	for row in dbcursor1.execute("SELECT name FROM sqlite_master WHERE type='table';"):
		for entry1 in row:
			outfilepath = os.path.join(extractdir, str(entry1) + ".txt")
			outfile = open(outfilepath, "w", encoding='utf8')
			SQLShell = apsw.Shell(stdout=outfile, db=dbconnection)
			SQLShell.process_command(".header on")
			SQLShell.process_sql("select * from " + str(entry1))
			outfile.close()

			
