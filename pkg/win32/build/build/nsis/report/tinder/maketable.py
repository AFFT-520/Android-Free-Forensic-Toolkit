#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makehtml, report.makecss, datetime


def makereport(case, timeline):
	csslocation = os.path.join(case, "reports", "tinder", "report.css")
	reportfilelocation = os.path.join(case, "reports", "tinder", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "Tinder"
	css = open(csslocation, 'w')
	report.makecss.makecss(css)
	css.close()
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	maketable(reportfile, case)
	reportfile.close()
	if timeline:
		tlmake(case)

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "tinder", "db", "tinder.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>From</b></td><td><b>ConversationID</b></td><td><b>Message</b></td><td><b>Sent</b></td></tr>\n")
	for row1 in reportfile_cursor1.execute("SELECT created FROM messages ORDER BY created DESC"):		##This is your initial SQL statement execution.
		for entry1 in row1:
			reportfile.write("<TR>") ## this initiates a html table row
			for row2 in reportfile_cursor2.execute("SELECT user_id FROM messages WHERE created = '" + str(entry1) + "'"):
				for entry2 in row2:
					reportfile.write("<TD>" + str(entry2) + "</TD>")
			for row2 in reportfile_cursor2.execute("SELECT match_id FROM messages WHERE created = '" + str(entry1) + "'"):
				for entry2 in row2:
					reportfile.write("<TD>" + str(entry2) + "</TD>")
			for row2 in reportfile_cursor2.execute("SELECT text FROM messages WHERE created = '" + str(entry1) + "'"):
				for entry2 in row2:
					reportfile.write("<TD>" + str(entry2) + "</TD>")
			reportfile.write("<TD>" + str(entry1) + "</TD>") ##this inserts a table cell
			reportfile.write("</TR>") ##closes the table row
			
def tlmake(case):
	reportfiledb = os.path.join(case, "extracted data", "tinder", "db", "tinder.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile_cursor3=reportfile_connection.cursor()

	tldb = os.path.join(case, "reports", "timeline.db")
	tl_connection=apsw.Connection(tldb)
	tl_cursor = tl_connection.cursor()
	for row1 in reportfile_cursor1.execute("SELECT created FROM messages ORDER BY created DESC"):		##This is your initial SQL statement execution.
		for entry1 in row1:
			timestr = str(entry1)
			timestr = timestr[:-5]
			timestamp=datetime.datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S").timestamp()
			timestamp = str(timestamp)
			timestamp = timestamp[:-2]
			for row2 in reportfile_cursor2.execute("SELECT user_id FROM messages WHERE created = '" + str(entry1) + "'"):
				for entry2 in row2:
					user = 0
					for row3 in reportfile_cursor3.execute("SELECT COUNT(id) FROM users WHERE id = '" + str(entry2) + "'"):
						for entry3 in row3:
							user = str(entry3)
					if user == '1':
						sender = "Message sent to Conversation ID "
					else:
						tindmatch = 'Unknown'
						for row3 in reportfile_cursor3.execute("SELECT user_name FROM matches WHERE user_id = '" + str(entry2) + "'"):
							for entry3 in row3:
								tindmatch = str(entry3)
						sender = "Received from " + tindmatch + ", from Conversation ID "
			for row2 in reportfile_cursor2.execute("SELECT match_id FROM messages WHERE created = '" + str(entry1) + "'"):
				for entry2 in row2:
					convoid = str(entry2) + ": "
			for row2 in reportfile_cursor2.execute("SELECT text FROM messages WHERE created = '" + str(entry1) + "'"):
				for entry2 in row2:
					text = str(entry2)
					text = text.replace("'", "''")
					text = text.replace('"', '""')
			message = sender + convoid + text
			command = "INSERT INTO timeline VALUES(NULL, 'Tinder', '" + message + "', " + timestamp + ")"
			tl_cursor.execute(command)
			
