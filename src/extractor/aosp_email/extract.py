#!/usr/bin/env python

import os, distutils.dir_util, apsw, shutil

def extract(case, userdata):

	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "aosp-email")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	metadata = os.path.join(extractdir, "metadata")
	if not os.path.exists(metadata):
		os.makedirs(metadata)
	body = os.path.join(extractdir, "body")
	if not os.path.exists(body):
		os.makedirs(body)
	dbpath = os.path.join(extractdir, "db")
	if not os.path.exists(dbpath):
		os.makedirs(dbpath)

	sourcedb = os.path.join(userdata, "data", "com.android.email", "databases", "EmailProvider.db")
	destpath = os.path.join (dbpath, "EmailProvider.db" )
	source = shutil.copyfile(sourcedb, destpath)
	metadatadb = destpath

	sourcedb = os.path.join(userdata, "data", "com.android.email", "databases", "EmailProviderBody.db")
	destpath = os.path.join (dbpath, "EmailProviderBody.db" )
	source = shutil.copyfile(sourcedb, destpath)
	bodydb = destpath

	sqlbody(bodydb, body)
	sqlmetadata(metadatadb, metadata, "account")
	sqlmetadata(metadatadb, metadata, "attachment")
	sqlmetadata(metadatadb, metadata, "hostauth")
	sqlmetadata(metadatadb, metadata, "mailbox")
	sqlmetadata(metadatadb, metadata, "message")
	sqlmetadata(metadatadb, metadata, "message_deletes")
	sqlmetadata(metadatadb, metadata, "message_updates")
	sqlmetadata(metadatadb, metadata, "messagemove")
	sqlmetadata(metadatadb, metadata, "messagestatechange")
	sqlmetadata(metadatadb, metadata, "policy")
	sqlmetadata(metadatadb, metadata, "quickresponse")

def sqlmetadata(metadatadb, metadata, table):
	
	outputfile = os.path.join(metadata, table + ".txt")
	output = open(outputfile, 'w', encoding='utf8')
	extractSQLconnect = apsw.Connection(metadatadb)
	SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
	try:
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select * from " + table)
	except:
		print("Could not extract email " + table +" info")
	output.close()

def sqlbody(bodydb, body):
	print( "--> Extracting data from Email (AOSP)\n\n")
	outputfile = os.path.join(body, "body.txt")
	output = open(outputfile, 'w', encoding='utf8')
	extractSQLconnect = apsw.Connection(bodydb)
	SQLShell = apsw.Shell(stdout=output, db=extractSQLconnect)
	try:
		SQLShell.process_command(".header on")
		SQLShell.process_sql("select * from body")
	except:
		print("Could not extract message body")
	output.close()



	

	
