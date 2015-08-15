#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makehtml, report.makecss


def makereport(case):
	csslocation = os.path.join(case, "reports", "system", "report.css")
	reportfilelocation = os.path.join(case, "reports", "system", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "System Info"
	css = open(csslocation, 'w')
	report.makecss.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()
	

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "image", "deviceproperties.db")	
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()

	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>example</b></td><td><b>example</b></td></tr>\n")
	for row1 in reportfile_cursor1.execute("SELECT key FROM settings ORDER BY key DESC"):		##This is your initial SQL statement.
		for entry1 in row1:
			setting = str(entry1)
			reportfile.write("<TR>") ## this initiates a html table row
			reportfile.write("<TD>" + setting + "</TD>") ##this inserts a table cell
			for row2 in reportfile_cursor2.execute("SELECT value FROM settings WHERE key = '" + setting + "'"):
				for entry2 in row2:
					value = str(entry2)
					reportfile.write("<TD>" + value + "</TD>") 
			reportfile.write("</TR>") ##closes the table row

