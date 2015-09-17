#!/usr/bin/env python

from dateutil import tz

import apsw, getopt, os, io, sys, shutil, re, time, report.makecss, report.makehtml, datetime


def makereport(case, timeline):
	csslocation = os.path.join(case, "reports", "calendar", "report.css")
	reportfilelocation = os.path.join(case, "reports", "calendar", "report.html")
	reportname = "Calendar"
	reportfile = open(reportfilelocation, 'w')
	css = open(csslocation, 'w')
	report.makecss.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()
	if timeline == True:
		tlmake(case)
def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "calendar", "db", "calendar.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile_cursor3=reportfile_connection.cursor()
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")

	for row1 in reportfile_cursor1.execute("SELECT DISTINCT account_name from calendars"):
		for account in row1:
			reportfile.write("<div class=\"ResultsTable\">\n")
			reportfile.write("<b>" + account + "</b>")
			reportfile.write("<table>\n")
			reportfile.write("<tr><td><b>Event</b></td><td><b>Details</b></td><td><b>Calendar</b></td><td><b>Location</b></td><td><b>Start</b></td><td><b>End</b></td><td><b>Organiser</b></td></tr>\n")
			for row2 in reportfile_cursor2.execute("SELECT _id FROM view_events WHERE account_name = \"" + account + "\" ORDER BY calendar_displayName DESC"):
				for rowid in row2:
					reportfile.write("<TR>")
					for row3 in reportfile_cursor3.execute("SELECT title FROM view_events WHERE _id = " + str(rowid)):
						for evtname in row3:
							reportfile.write("<TD>" + evtname + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT description FROM view_events WHERE _id = " + str(rowid)):
						for details in row3:
							details = details.replace("<", "&lt;")
							details = details.replace(">", "&gt;")
							reportfile.write("<TD>" + str(details) + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT calendar_displayName FROM view_events WHERE _id = " + str(rowid)):
						for calname in row3:
							reportfile.write("<TD>" + calname + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT eventLocation FROM view_events WHERE _id = " + str(rowid)):
						for locname in row3:
							reportfile.write("<TD>" + locname + "</TD>")					
					for row3 in reportfile_cursor3.execute("SELECT datetime(dtstart/1000,'unixepoch','localtime') as dtstart FROM view_events WHERE _id = " + str(rowid)):
						for start in row3:
							reportfile.write("<TD>" + str(start) + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT datetime(dtstart/1000,'unixepoch','localtime') as dtend FROM view_events WHERE _id = " + str(rowid)):
						for end in row3:
							reportfile.write("<TD>" + str(end) + "</TD>")
					for row3 in reportfile_cursor3.execute("SELECT organizer FROM view_events WHERE _id = " + str(rowid)):
						for organiser in row3:
							reportfile.write("<TD><a href=\"https://www.google.com/calendar/embed?src=" + str(organiser) + "\">" + str(organiser) + "</a></TD>")
					reportfile.write("</TR>")
			reportfile.write("</table>")
			reportfile.write("</div>")
			reportfile.write("<br />")
			reportfile.write("<br />")

def tlmake(case):
	reportfiledb = os.path.join(case, "extracted data", "calendar", "db", "calendar.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile_cursor3=reportfile_connection.cursor()
	
	tldb = os.path.join(case, "reports", "timeline.db")
	tl_connection=apsw.Connection(tldb)
	tl_cursor=tl_connection.cursor()
	for row1 in reportfile_cursor1.execute("SELECT DISTINCT account_name from calendars"):
		for account in row1:
			for row2 in reportfile_cursor2.execute("SELECT _id FROM view_events WHERE account_name = \"" + account + "\" ORDER BY calendar_displayName DESC"):
				for rowid in row2:
					for row3 in reportfile_cursor3.execute("SELECT title FROM view_events WHERE _id = " + str(rowid)):
						for evtname in row3:
							name = str(evtname)
							name = name.replace("'", "''")
							name = name.replace('"', '""')
							name = name.replace("--", "")
							tlname = 'The event "' + name + '"'
					for row3 in reportfile_cursor3.execute("SELECT calendar_displayName FROM view_events WHERE _id = " + str(rowid)):
						for calname in row3:
							tlcalname = '(registered to ' + str(calname) + ')'
					for row3 in reportfile_cursor3.execute("SELECT eventLocation FROM view_events WHERE _id = " + str(rowid)):
						for locname in row3:
							loc = str(locname)
							loc = loc.replace('"', '""')
							loc = loc.replace("'", "''")
							loc = loc.replace("--", "")
							if str(loc) != '':
								tllocname =  ", located at " + loc + ","
							else:
								tllocname = " "
					for row3 in reportfile_cursor3.execute("SELECT dtstart FROM view_events WHERE _id = " + str(rowid)):
						for start in row3:
							timestamp = start
					for row3 in reportfile_cursor3.execute("SELECT dtend FROM view_events WHERE _id = " + str(rowid)):
						for end in row3:
							endtimestamp = end
					for row3 in reportfile_cursor3.execute("SELECT datetime(dtstart/1000,'unixepoch','localtime') as dtstart FROM view_events WHERE _id = " + str(rowid)):
						for readablestart in row3:
							readstart = readablestart
							now = int(time.time())
							if start > now:
								tlstart = " started at " + readstart
							else:
								tlstart = " starts at " + readstart
					for row3 in reportfile_cursor3.execute("SELECT datetime(dtend/1000,'unixepoch','localtime')as dtend FROM view_events WHERE _id = " + str(rowid)):
						for readableend in row3:
							if end > now:
								tlend = " and ended at " + str(readableend)
							else:
								tlend = " and ends at " + str(readableend)
					message = tlname + tllocname + tlstart + tlend + tlcalname
					command = "INSERT INTO timeline VALUES(NULL, 'Calendar','" + message + "', '" + str(timestamp) + "')"
					tl_cursor.execute(command)
