#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makecss, report.makehtml


def makereport(case):
	csslocation = os.path.join(case, "reports", "google-maps", "report.css")
	reportfilelocation = os.path.join(case, "reports", "google-maps", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "Google Maps Bookmarked Locations"
	css = open(csslocation, 'w')
	report.makecss.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "google-maps", "db", "gmm_myplaces.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()

	
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>Latitude</b></td><td><b>Longitude</b></td><td><b>Time added</b></td><td><b>Google Maps Link</b></td></tr>\n")
	for row1 in reportfile_cursor1.execute("SELECT key_string FROM sync_item ORDER BY timestamp DESC"):
		for entry in row1:						
			for row2 in reportfile_cursor2.execute("SELECT latitude FROM sync_item where key_string = '" + str(entry) + "'"):
				for lat in row2:
					reportfile.write("<TD>" + str(lat) + "</TD>")
			for row2 in reportfile_cursor2.execute("SELECT longitude FROM sync_item where key_string = '" + str(entry) + "'"):
				for lon in row2:
					reportfile.write("<TD>" + str(lon) + "</TD>")
			for row2 in reportfile_cursor2.execute("SELECT datetime(timestamp/1000,'unixepoch','localtime') as timestamp FROM sync_item where key_string = '" + str(entry) + "'"):				
				for time in row2:
					reportfile.write("<TD>" + str(time) + "</TD>")
			reportfile.write("<TD><a href=\"" + str(entry) + "\">" + str(entry) + "</a></TD>")			
			reportfile.write("</TR>")



