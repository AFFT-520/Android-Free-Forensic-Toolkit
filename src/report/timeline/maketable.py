#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makehtml, report.makecss


def makereport(case):
	csslocation = os.path.join(case, "reports", "timeline", "report.css")
	reportfilelocation = os.path.join(case, "reports", "timeline", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "Timeline"
	css = open(csslocation, 'w')
	report.makecss.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()
	

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "reports", "timeline.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()

	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>Service</b></td><td><b>Event</b></td><td><b>Time</b></td></tr>\n")
	for row1 in reportfile_cursor1.execute("SELECT _id FROM timeline ORDER BY datetime(timestamp/1000,'unixepoch','localtime') DESC"):		##This is your initial SQL statement execution.
		for entry1 in row1:
			reportfile.write("<TR>") ## this initiates a html table row
			for row2 in reportfile_cursor2.execute("SELECT service FROM timeline WHERE _id = " + str(entry1)):
				for service in row2:
					servicestr = str(service)
					reportfile.write("<TD>" + servicestr + "</TD>") ##this inserts a table cell
			for row2 in reportfile_cursor2.execute("SELECT message FROM timeline WHERE _id = " + str(entry1)):
				for event in row2:
					eventstr = str(event)
					reportfile.write("<TD>" + eventstr + "</TD>") ##this inserts a table cell
			for row2 in reportfile_cursor2.execute("SELECT datetime(timestamp/1000,'unixepoch','localtime') as timestamp FROM timeline WHERE _id = " + str(entry1)):
				for time in row2:
					timestr = str(time)
					reportfile.write("<TD>" + timestr + "</TD>") ##this inserts a table cell
			reportfile.write("</TR>") ##closes the table row

