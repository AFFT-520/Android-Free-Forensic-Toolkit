#!/usr/bin/env python

import os, sys, getopt, time, apsw, re, report.makehtml

	

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "facebook", "db", "threads_db2")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("<tr><td><a href=report.html>Messages</a></td></tr>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr><td><b>Profile Picture</b></td><td><b>Name</b></td><td><b>Facebook ID</b></td></tr>\n")

	try:
		for row1 in reportfile_cursor1.execute("select user_key from thread_users order by Name ASC"):
			for entry1 in row1:
				reportfile.write("<TR>\n")
				for row2 in reportfile_cursor2.execute("select user_key from thread_users WHERE user_key = '" + str(entry1) + "'"):
					for entry2 in row2:
						entry2 = entry2.replace("FACEBOOK:","")
						reportfile.write("<TD><a href src='http://www.facebook.com/" + entry2 + "'><img src='http://graph.facebook.com/" + entry2 + "/picture'</TD>\n")
					for row2 in reportfile_cursor2.execute("select name from thread_users WHERE user_key = '" + str(entry1) + "'"):
						for entry2 in row2:
							reportfile.write("<TD>" + str(entry2) + "</TD>\n")
				
					for row2 in reportfile_cursor2.execute("select user_key from thread_users WHERE user_key = '" + str(entry1) + "'"):
						for entry2 in row2:
							entry2 = entry2.replace("FACEBOOK:","")
							reportfile.write("<TD>" + str(entry2) + "</TD>\n")
						
				
						
				reportfile.write("</TR>\n")
		reportfile.write("</table>\n")
		reportfile.write("</div>\n")
	except Exception as error:
		print("Error! contacts", error)
		exit()
	
def makereport(case):
	
	reportfilelocation = os.path.join(case, "reports", "facebook", "reportfile-contacts.html")
	reportname = "Facebook Contacts"	
	reportfile = open(reportfilelocation, 'w')
	
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	
	
	reportfile.close()
	
	


