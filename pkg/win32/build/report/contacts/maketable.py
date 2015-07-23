#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makecss, report.makehtml

def makereport(case):
	csslocation = os.path.join(case, "reports", "contacts", "report.css")
	reportfilelocation = os.path.join(case, "reports", "contacts", "report.html")
	reportname = "Phone Contacts"
	reportfile = open(reportfilelocation, 'w')
	css = open(csslocation, 'w')
	report.makecss.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "contacts", "db", "contacts2.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile_cursor3=reportfile_connection.cursor()
	
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>Name</b></td><td><b>Number</b></td><td><b>Type</b></td><td><b>Account Registered To</b></td></tr>\n")
	try:
		for row1 in reportfile_cursor1.execute("SELECT _id FROM view_raw_contacts"):
			for entry in row1:	
				reportfile.write("<TR>")					
				for row2 in reportfile_cursor2.execute("SELECT display_name FROM view_raw_contacts where _id = " + str(entry)):
					for name in row2:
						reportfile.write("<TD>" + str(name) + "</TD>")
					
				reportfile.write("<TD>" + reportfile_cursor2.execute("SELECT normalized_number FROM phone_lookup where raw_contact_id = " + str(entry)) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT normalized_number FROM phone_lookup where raw_contact_id = " + str(entry)):								
					for number in row2:
						reportfile.write("<TD>" + str(number) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT account_type FROM view_raw_contacts where _id = " + str(entry)):				
					for acctype in row2:
						reportfile.write("<TD>" + str(acctype) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT account_name FROM view_raw_contacts where _id = " + str(entry)):				
					for accname in row2:
						reportfile.write("<TD>" + str(accname) + "</TD>")
			
				reportfile.write("</TR>")
	except apsw.SQLError:
		for row1 in reportfile_cursor1.execute("SELECT _id FROM view_raw_contacts"):
			for entry in row1:	
				reportfile.write("<TR>")					
				for row2 in reportfile_cursor2.execute("SELECT display_name FROM view_raw_contacts where _id = " + str(entry)):
					for name in row2:
						reportfile.write("<TD>" + str(name) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT COUNT (normalized_number) FROM phone_lookup where raw_contact_id = " + str(entry)):								
					for count in row2:
						if count == 0:
							reportfile.write("<TD>None</TD>")					
						elif count == 1:
							for row2 in reportfile_cursor2.execute("SELECT normalized_number FROM phone_lookup where raw_contact_id = " + str(entry)):								
								for number in row2:
									reportfile.write("<TD>" + str(number) + "</TD>")
						elif count > 1:
							written = 1
							reportfile.write("<TD>")
							for row2 in reportfile_cursor3.execute("SELECT normalized_number FROM phone_lookup where raw_contact_id = " + str(entry)):								
								for number in row2:
									if written != count:
										reportfile.write(str(number) + ", ")
									else:
										reportfile.write(str(number))
									written = written + 1
							reportfile.write("</TD>")
				for row2 in reportfile_cursor2.execute("SELECT account_type FROM view_raw_contacts where _id = " + str(entry)):				
					for acctype in row2:
						reportfile.write("<TD>" + str(acctype) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT account_name FROM view_raw_contacts where _id = " + str(entry)):				
					for accname in row2:
						reportfile.write("<TD>" + str(accname) + "</TD>")
			
				reportfile.write("</TR>")



