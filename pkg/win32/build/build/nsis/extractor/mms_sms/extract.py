#!/usr/bin/env python

import os, shutil, apsw, distutils.dir_util

def extract(case, userdata):
	print("--> Extracting SMS/MMS messages\n\n")
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "mms-sms")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	dbdir = os.path.join(extractdir, "db")
	if not os.path.exists(dbdir):
		os.makedirs(dbdir)
	db_src = os.path.join(userdata, "data", "com.android.providers.telephony", "databases", "mmssms.db" )
	db_dest = os.path.join(dbdir, "mmssms.db" )
	shutil.copyfile(db_src, db_dest)

	dbconnection = apsw.Connection(db_dest)
	filepath = os.path.join(extractdir, "Messages.txt")
	fileopen = open(filepath, "w", encoding='utf8')
	dbshell = apsw.Shell(stdout=fileopen, db=dbconnection)
	dbshell.process_command(".header on")
	dbshell.process_sql("select * from sms")
	fileopen.close()


