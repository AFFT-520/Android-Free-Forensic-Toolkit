#!/usr/bin/env python

import os, shutil, apsw, distutils.dir_util, sys, re

def extract(case, userdata):
	print( "--> Extracting GMail data\n\n")
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "gmail")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	dbdir = os.path.join(extractdir, "db")
	if not os.path.exists(dbdir):
		os.makedirs(dbdir)
	maildbdir = os.path.join(dbdir, "mailstore")
	if not os.path.exists(maildbdir):
		os.makedirs(maildbdir)
	settingdbdir = os.path.join(dbdir, "settings")
	if not os.path.exists(settingdbdir):
		os.makedirs(settingdbdir)
	
	importdbdir = os.path.join(userdata, "data", "com.google.android.gm", "databases")
	for row in os.listdir(importdbdir):
		mailstore_search = re.compile("^mailstore")
		mailstore_match = mailstore_search.match(row)
		db_search = re.compile("^.*\.db$")
		db_match = db_search.match(str(row))
		setting_search = re.compile("^internal")
		setting_match = setting_search.match(str(row))
		if mailstore_match and db_match:		
			accname = str(row)
			accname = accname.replace("mailstore.","")
			accname = accname.replace(".db", "")
			accdir = os.path.join(extractdir, accname)
			if not os.path.exists(accdir):
				os.makedirs(accdir)
			
			accmaildb_src = os.path.join(importdbdir, str(row))
			accmaildb_dest = os.path.join(maildbdir, str(row))
			shutil.copyfile(accmaildb_src, accmaildb_dest)
		
		if setting_match and db_match:
			accsettdb_src = os.path.join(importdbdir, str(row))
			accsettdb_dest = os.path.join(settingdbdir, str(row))
			shutil.copyfile(accsettdb_src, accsettdb_dest)

		copy_misc(importdbdir, dbdir, "EmailProvider.db")
		copy_misc(importdbdir, dbdir, "google_analytics_v2.db")
		copy_misc(importdbdir, dbdir, "EmailProviderBody.db")
		copy_misc(importdbdir, dbdir, "suggestions.db")	

	for row in os.listdir(maildbdir):
		accname = str(row)
		accname = accname.replace("mailstore.","")
		accname = accname.replace(".db", "")

		dbselected = os.path.join(maildbdir, str(row))
		dbconnection = apsw.Connection(dbselected)
		accfilepath = os.path.join(extractdir, accname, "Messages.txt")
		accfile = open(accfilepath, "w", encoding='utf8')
		dbshell = apsw.Shell(stdout=accfile, db=dbconnection)
		dbshell.process_command(".header on")
		dbshell.process_sql("select * from messages")
		accfile.close()


def copy_misc(importdbdir, destdbdir, filename):
		other_src = os.path.join(importdbdir, filename )
		other_dest = os.path.join(destdbdir, filename )
		shutil.copyfile(other_src, other_dest)
			
