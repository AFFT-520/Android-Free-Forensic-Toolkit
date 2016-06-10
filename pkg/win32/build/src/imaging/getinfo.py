#!/usr/bin/env python

import os, apsw, subprocess, shutil

def makedb(case):
	print(' --> Creating device information database')
	cwd = os.path.dirname(os.path.realpath(__file__))
	dbname = os.path.join(case, "image", "deviceproperties.db")
	if os.path.isfile(dbname):
		os.remove(dbname)
	dbcon = apsw.Connection(dbname)
	dbcur1 = dbcon.cursor()
	dbcur1.execute('CREATE TABLE settings(key PRIMARY KEY, value)')
	if os.name == 'nt':
		adb = os.path.join(cwd, '..', 'bin', 'adb.exe')

	if os.name == 'nt':
		detail_list = subprocess.Popen(adb + ' shell getprop', shell=True, stdout=subprocess.PIPE).stdout.read()
	else:
		detail_list = subprocess.Popen('adb shell getprop', shell=True, stdout=subprocess.PIPE).stdout.read()
	detail_list_str = str(detail_list)
	if os.name == 'nt':
		detail_list_str = detail_list_str.replace('\\r\\n', '\r')
	else:
		detail_list_str = detail_list_str.replace('\\r\\n', '\n')
	detail_list_str = detail_list_str[2:-2]
	detail_list_str = detail_list_str + "\n"
	detail_list_str = detail_list_str.replace('[]', "NULL")
	detail_list_str = detail_list_str.replace('[', '')
	detail_list_str = detail_list_str.replace(']', '')
	detail_list_str = detail_list_str.replace(': ', ':')
	detail_list_lines = detail_list_str.splitlines()
	linemax = len(detail_list_lines)
	linecount = 0
	while linecount < linemax:
		linestr = str(detail_list_lines[linecount])
		linesplit = linestr.split(':')
		key = linesplit[0]
		value = linesplit[1]
		dbcur1.execute("INSERT INTO settings(key, value) VALUES('" + key + "', '" + value + "')")
		linecount = linecount + 1
	

