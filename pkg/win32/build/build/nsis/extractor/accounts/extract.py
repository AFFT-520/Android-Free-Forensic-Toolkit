#!/usr/bin/env python

import os, distutils.dir_util, apsw, shutil

def extract(case, userdata):
	print("--> Extracting accounts info\n\n")
	
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "accounts")
	
	
	shutil.copytree(os.path.join(userdata, "system", "users"), os.path.join (case, "extracted data", "accounts"))
	for dirname, dirnames, filenames in os.walk(extractdir):
		for subdirname in dirnames:		
			user = os.path.join(extractdir, subdirname)	
			database = os.path.join(user, "accounts.db")
			outputfile = os.path.join(user, "accounts.txt")
			output = open(outputfile, 'w', encoding='utf8')
			extractSQLconnect = apsw.Connection(database)
			SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
			SQLShell.process_command(".header on")
			SQLShell.process_sql("select * from accounts")
			output.close()
				
