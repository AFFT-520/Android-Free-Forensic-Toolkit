#!/usr/bin/env python

import os, sys, shutil, apsw

def extract(case, userdata):
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "tinder")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	cachedest = os.path.join(extractdir, "cache")
	if os.path.exists(cachedest):
		shutil.rmtree(cachedest)
	filesdest = os.path.join(extractdir, "files")
	if os.path.exists(filesdest):
		shutil.rmtree(filesdest)
	dbpath = os.path.join(extractdir, "db")
	if not os.path.exists(dbpath):
		os.makedirs(dbpath)
	copy(case, userdata, cachedest, filesdest, dbpath)
	sql(case, dbpath)
def copy(case, userdata, cachedest, filesdest, dbpath):
	sourcedb = os.path.join(userdata, "data", "com.tinder", "databases", "tinder.db")
	destpath = os.path.join (dbpath, "tinder.db" )
	source = shutil.copyfile(sourcedb, destpath)

	datapath = os.path.join(userdata, "data", "com.tinder")
	cachesource=os.path.join(datapath, "cache")
	filessource=os.path.join(datapath, "files")
	cache=shutil.copytree(cachesource, cachedest)
	files=shutil.copytree(filessource, filesdest)

def sql(case, dbpath):
	print("--> Extracting Tinder information")
	db = os.path.join (dbpath, "tinder.db" )
	output = os.path.join(dbpath, '..', 'output.txt')
	openoutput = open(output, 'w')
	dbconn = apsw.Connection(db)
	dbshell = apsw.Shell(stdout=openoutput, db=dbconn)
	try:
		dbshell.process_command(".header on")
		dbshell.process_sql("select * from messages")
		openoutput.close()
	except Exception:
		print("Extract Failed")
	
