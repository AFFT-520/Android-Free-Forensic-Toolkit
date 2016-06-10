#!/usr/bin/env python

import os, shutil, apsw, distutils.dir_util

def extract(case, userdata):
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "facebook-messenger")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	dbdir = os.path.join(extractdir, "db")
	if not os.path.exists(dbdir):
		os.makedirs(dbdir)
	copy(case, userdata, dbdir)
	sql(case, dbdir)

def copy(case, userdata, dbdir):
	db_path = os.path.join(userdata, "data", "com.facebook.orca", "databases")	
	
	try:
		sourcedb = os.path.join(db_path, "analytics_db2")
		destpath = os.path.join (dbdir, "analytics_db2")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy analytics_db2 ! ")

	try:
		sourcedb = os.path.join(db_path, "call_log.sqlite")
		destpath = os.path.join (dbdir, "call_log.sqlite")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy call_log.sqlite ! ")

	try:
		sourcedb = os.path.join(db_path, "composer_shortcuts_db")
		destpath = os.path.join (dbdir, "composer_shortcuts_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy composer_shortcuts_db ! ")

	try:
		sourcedb = os.path.join(db_path, "contacts_db2")
		destpath = os.path.join (dbdir, "contacts_db2")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy contacts_db2 ! ")

	try:
		sourcedb = os.path.join(db_path, "graphql_cache")
		destpath = os.path.join (dbdir, "graphql_cache")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy graphql_cache ! ")

	try:
		sourcedb = os.path.join(db_path, "offline_mode_db")
		destpath = os.path.join (dbdir, "offline_mode_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy offline_mode_db ! ")

	try:
		sourcedb = os.path.join(db_path, "prefs_db")
		destpath = os.path.join (dbdir, "prefs_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy prefs_db ! ")

	try:
		sourcedb = os.path.join(db_path, "qe_db")
		destpath = os.path.join (dbdir, "qe_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy qe_db ! ")

	try:
		sourcedb = os.path.join(db_path, "stickers_db")
		destpath = os.path.join (dbdir, "stickers_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy stickers_db ! ")

	try:
		sourcedb = os.path.join(db_path, "threads_db2")
		destpath = os.path.join (dbdir, "threads_db2")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy threads_db2 ! ")

def sql(case, dbdir):

	user = dbdir
	print( "--> Extracting results from Facebook Messenger databases\n\n")
	database = os.path.join(user, "threads_db2")
	outputfile = os.path.join(user, "..", "threads_db2.txt")
	output = open(outputfile, 'w', encoding='utf8')
	extractSQLconnect = apsw.Connection(database)
	SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
	try:
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select * from messages")
	except:
		print("Could not extract messages")
	output.close()

	database = os.path.join(user, "call_log.sqlite")
	outputfile = os.path.join(user, "..", "call_log.sqlite.txt")
	output = open(outputfile, 'w', encoding='utf8')
	extractSQLconnect = apsw.Connection(database)
	SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
	try:
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select * from person_summary")
	except Exception:
		print("Could not extract call log")
	output.close()

