#!/usr/bin/env python

import os, apsw, subprocess, shutil


def makedb(case): #This function gets the feedback from 'adb shell getprop' and puts it into a SQLite database for later use. This can help validate certain aspects of the imaging process such as (in some cases) the method of obtaining root for imaging. 
	print(' --> Creating device information database') #Feedback for the user to prevent misconception of crashing
	cwd = os.path.dirname(os.path.realpath(__file__))
	dbname = os.path.join(case, "image", "deviceproperties.db")#Sets up the database
	if os.path.isfile(dbname):
		os.remove(dbname)
	dbcon = apsw.Connection(dbname)
	dbcur1 = dbcon.cursor()
	dbcur1.execute('CREATE TABLE settings(key PRIMARY KEY, value)')
	if os.name == 'nt':
		adb = os.path.join(cwd, '..', 'bin', 'adb.exe') #If running under Windows, we're using a bundled version of ADB instead of assuming it's in $PATH...

	if os.name == 'nt': #...And the command we run changes to reflect that
		detail_list = subprocess.Popen(adb + ' shell getprop', shell=True, stdout=subprocess.PIPE).stdout.read() #This command gets the raw output of 'adb shell getprop'
	else:
		detail_list = subprocess.Popen('adb shell getprop', shell=True, stdout=subprocess.PIPE).stdout.read()
	detail_list_str = str(detail_list) #The raw output of the command
	if os.name == 'nt':
		detail_list_str = detail_list_str.replace('\\r\\n', '\r') #Changes the newline notation in the raw output to the native newline notation of the PC Operating system (\r for Windows, \n for OSX/Linux)
	else:
		detail_list_str = detail_list_str.replace('\\r\\n', '\n')
	detail_list_str = detail_list_str[2:-2] #Gets rid of fluff notation put by Python (the b' at the start and the stray ' at the end)
	detail_list_str = detail_list_str + "\n"#Puts an endline at the end of the output
	detail_list_str = detail_list_str.replace('[]', "NULL") # '[]' in the output means that there is no data. This translates that fact to SQL-friendly language.
	detail_list_str = detail_list_str.replace('[', '') # Data values in the raw output are enclosed in square brackets. This is unneccessary, so we strip them
	detail_list_str = detail_list_str.replace(']', '')
	detail_list_str = detail_list_str.replace(': ', ':') #gets rid of the leading space after the : (which seperates the data names and their values). This is important for later
	detail_list_lines = detail_list_str.splitlines()
	linemax = len(detail_list_lines) #Gets the number of lines from the parsed output.
	linecount = 0
	while linecount < linemax: #Until the amount of lines processed equals the total number of lines, parse each line and put the key and value into the SQLite database.
		linestr = str(detail_list_lines[linecount]) #Selects the next unprocessed line
		linesplit = linestr.split(':')#uses the : in the line to differentiate between the key and it's value
		key = linesplit[0]
		value = linesplit[1]
		dbcur1.execute("INSERT INTO settings(key, value) VALUES('" + key + "', '" + value + "')")# put the key and value into the database
		linecount = linecount + 1 #on to the next one
	

