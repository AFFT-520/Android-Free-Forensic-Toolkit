#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makehtml, report.makecss


def makereport(case):
	csslocation = os.path.join(case, "reports", "mms-sms", "report.css")
	reportfilelocation = os.path.join(case, "reports", "mms-sms", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "Example"
	css = open(csslocation, 'w')
	report.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()
	

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "example", "db", "example.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()

	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>example</b></td><td><b>example</b></td></tr>\n")
	for row1 in reportfile_cursor1.execute("SELECT _id FROM example ORDER BY example DESC"):		##This is your initial SQL statement execution.
		for entry1 in row1:
			reportfile.write("<TR>") ## this initiates a html table row
			reportfile.write("<TD>Example</TD>") ##this inserts a table cell
			reportfile.write("</TR>") ##closes the table row

