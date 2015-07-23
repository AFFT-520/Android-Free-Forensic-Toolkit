#!/usr/bin/env python

import os, shutil, apsw, distutils.dir_util

def extract(case, userdata):
	print("--> Extracting system information\n\n")
	extractdir = os.path.join(case, "extracted data")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extractdir = os.path.join(extractdir, "system")
	if not os.path.exists(extractdir):
		os.makedirs(extractdir)
	extract_db_dir = os.path.join(extractdir, "vpn")
	if not os.path.exists(extract_db_dir):
		os.makedirs(extract_db_dir)
	
	try:
		sourcedb = os.path.join(userdata, "misc", "wifi", "wpa_supplicant.conf")
		destpath = os.path.join (case, "extracted data", "system", "wpa_supplicant.conf")
		source = shutil.copyfile(sourcedb, destpath)

		sourcedb = os.path.join(userdata, "misc", "adb", "adb_keys")
		destpath = os.path.join (case, "extracted data", "system", "adb_keys")
		source = shutil.copyfile(sourcedb, destpath)

		sourcedb = os.path.join(userdata, "misc", "bluedroid", "bt_config.xml")
		destpath = os.path.join (case, "extracted data", "system", "bt_config.xml")
		source = shutil.copyfile(sourcedb, destpath)

		distutils.dir_util.copy_tree(os.path.join(userdata, "misc", "vpn"), os.path.join (case, "extracted data", "system", "vpn"))
		

	except Exception:
		print("--> Not extracting system data. Reason: Not found\n\n")


