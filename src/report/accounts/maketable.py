#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makecss, report.makehtml

def makereport(case):
	csslocation = os.path.join(case, "reports", "accounts", "report.css")
	reportfilelocation = os.path.join(case, "reports", "accounts", "report.html")
	reportname = "System Accounts"
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
	datadir = os.path.join(case, "extracted data", "accounts")
	for dirname, subdirlist, filelist in os.walk(datadir):
		for entry in subdirlist:
			reportfiledb = os.path.join(datadir, entry, "accounts.db")
			reportfile_connection=apsw.Connection(reportfiledb)
			reportfile_cursor1=reportfile_connection.cursor()
			reportfile_cursor2=reportfile_connection.cursor()
			reportfile_cursor3=reportfile_connection.cursor()
	
			reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
			reportfile.write("</table>\n")
			reportfile.write("<div class=\"ResultsTable\">\n")

			accname = entry
			accinfo = os.path.join(case, "extracted data", "accounts", accname + ".xml")


			with open(accinfo, 'r') as accfile:
				for entry in accfile.readlines():
					namecriteria = re.compile(".*\<name\>")
					namematch = namecriteria.match(str(entry))
					if namematch:
						name = entry
						name = name.replace("</name>","")
						name = name.replace("<name>","")
						name = name.replace("	","")

			reportfile.write("<b>" + name + "</b>")
			reportfile.write("<table>\n")
			reportfile.write("<tr><td><b>Name</b></td><td><b>Account Type</b></td><td><b>Password Hash</b></td></tr>\n")
			for row2 in reportfile_cursor2.execute("SELECT _id FROM accounts"):
				for rowid in row2:
					reportfile.write("<TR>")
					for row3 in reportfile_cursor3.execute("SELECT name FROM accounts WHERE _id = " + str(rowid)):
						for accname in row3:
							reportfile.write("<TD>" + accname + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT type FROM accounts WHERE _id = " + str(rowid)):
						for acctype in row3:
							reportfile.write("<TD>" + acctype + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT password FROM accounts WHERE _id = " + str(rowid)):
						for accpass in row3:
							reportfile.write("<TD>" + str(accpass) + "</TD>")
					reportfile.write("</TR>")

