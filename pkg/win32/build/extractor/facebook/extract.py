#!/usr/bin/env python

import os, shutil, apsw, distutils.dir_util

def extract(case, userdata):
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "facebook")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	dbdir = os.path.join(extractdir, "db")
	if not os.path.exists(dbdir):
		os.makedirs(dbdir)
	copy(case, userdata, dbdir)
	sql(case, dbdir)

def copy(case, userdata, dbdir):
	db_path = os.path.join(userdata, "data", "com.facebook.katana", "databases")	
	try:
		sourcedb = os.path.join(db_path, "analytics_db2")
		destpath = os.path.join (dbdir, "analytics_db2")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy analytics_db2 ! ")

	try:
		sourcedb = os.path.join(db_path, "bookmarks_db2")
		destpath = os.path.join (dbdir, "bookmarks_db2")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy bookmarks_db2 ! ")

	try:
		sourcedb = os.path.join(db_path, "composer_db")
		destpath = os.path.join (dbdir, "composer_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy composer_db ! ")

	try:
		sourcedb = os.path.join(db_path, "composer_shortcuts_db")
		destpath = os.path.join (dbdir, "composer_shortcuts_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy composer_shortcuts_db ! ")

	try:
		sourcedb = os.path.join(db_path, "connections_db")
		destpath = os.path.join (dbdir, "connections_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy connections_db ! ")

	try:
		sourcedb = os.path.join(db_path, "contacts_db2")
		destpath = os.path.join (dbdir, "contacts_db2")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy contacts_db2 ! ")

	try:
		sourcedb = os.path.join(db_path, "dash_ranking_analytics_db")
		destpath = os.path.join (dbdir, "dash_ranking_analytics_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy dash_ranking_analytics_db ! ")

	try:
		sourcedb = os.path.join(db_path, "events_db")
		destpath = os.path.join (dbdir, "events_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy events_db ! ")

	try:
		sourcedb = os.path.join(db_path, "graphql_cache")
		destpath = os.path.join (dbdir, "graphql_cache")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy graphql_cache ! ")

	try:
		sourcedb = os.path.join(db_path, "legacy_key_value_db")
		destpath = os.path.join (dbdir, "legacy_key_value_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy legacy_key_value_db ! ")

	try:
		sourcedb = os.path.join(db_path, "mds_cache_db")
		destpath = os.path.join (dbdir, "mds_cache_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy mds_cache_db ! ")

	try:
		sourcedb = os.path.join(db_path, "minutiae_db")
		destpath = os.path.join (dbdir, "minutiae_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy minutiae_db ! ")

	try:
		sourcedb = os.path.join(db_path, "nearby_tiles_db")
		destpath = os.path.join (dbdir, "nearby_tiles_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy nearby_tiles_db ! ")

	try:
		sourcedb = os.path.join(db_path, "newsfeed_db")
		destpath = os.path.join (dbdir, "newsfeed_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy newsfeed_db ! ")

	try:
		sourcedb = os.path.join(db_path, "notifications_db")
		destpath = os.path.join (dbdir, "notifications_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy notifications_db ! ")

	try:
		sourcedb = os.path.join(db_path, "offline_mode_db")
		destpath = os.path.join (dbdir, "offline_mode_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy offline_mode_db ! ")

	try:
		sourcedb = os.path.join(db_path, "photos_db")
		destpath = os.path.join (dbdir, "photos_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy photos_db ! ")

	try:
		sourcedb = os.path.join(db_path, "prefs_db")
		destpath = os.path.join (dbdir, "prefs_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy prefs_db ! ")

	try:
		sourcedb = os.path.join(db_path, "push_notifications_db")
		destpath = os.path.join (dbdir, "push_notifications_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy push_notifications_db ! ")

	try:
		sourcedb = os.path.join(db_path, "qe_db")
		destpath = os.path.join (dbdir, "qe_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy qe_db ! ")

	try:
		sourcedb = os.path.join(db_path, "search_bootstrap_db")
		destpath = os.path.join (dbdir, "search_bootstrap_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy search_bootstrap_db ! ")

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

	try:
		sourcedb = os.path.join(db_path, "timeline_db")
		destpath = os.path.join (dbdir, "timeline_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy timeline_db ! ")

	try:
		sourcedb = os.path.join(db_path, "timeline_prefetch_db")
		destpath = os.path.join (dbdir, "timeline_prefetch_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy timeline_prefetch_db ! ")

	try:
		sourcedb = os.path.join(db_path, "user_statuses_db")
		destpath = os.path.join (dbdir, "user_statuses_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy user_statuses_db ! ")

	try:
		sourcedb = os.path.join(db_path, "vault_db")
		destpath = os.path.join (dbdir, "vault_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy vault_db ! ")

	try:
		sourcedb = os.path.join(db_path, "videocache_db")
		destpath = os.path.join (dbdir, "videocache_db")
		source = shutil.copyfile(sourcedb, destpath)

	except Exception:
		print("Could not copy videocache_db ! ")


def sql(case, dbdir):

	user = dbdir
	print( "--> Extracting results from Facebook databases\n\n")
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

	database = os.path.join(user, "contacts_db2")
	outputfile = os.path.join(user, "..", "contacts_db2.txt")
	output = open(outputfile, 'w', encoding='utf8')
	extractSQLconnect = apsw.Connection(database)
	SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
	try:
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select * from contacts")
	except Exception:
		print("Could not extract contact info")
	output.close()

	database = os.path.join(user, "notifications_db")
	outputfile = os.path.join(user, "..", "notifications_db.txt")
	output = open(outputfile, 'w', encoding='utf8')
	extractSQLconnect = apsw.Connection(database)
	SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
	try:	
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select * from gql_notifications")
	except Exception:
		print("Could not extract notification log")
	output.close()
