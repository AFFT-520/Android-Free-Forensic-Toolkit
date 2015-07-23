#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makehtml, report.makecss


def makereport(case, timeline):
	csslocation = os.path.join(case, "reports", "whatsapp", "report.css")
	reportfilelocation = os.path.join(case, "reports", "whatsapp", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "Example"
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
	reportfiledb = os.path.join(case, "extracted data", "whatsapp", "msgstore.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr class=\"title\"><td><b>Conversation ID</b></td><td><b>Status</b></td><td><b>Text</b></td><td><b>Timestamp</b></td><td><b>Attached File</b></td><td><b>Relative Filepath</b></td></tr>\n")
	try:
		for row1 in reportfile_cursor1.execute("SELECT _id FROM messages ORDER BY timestamp DESC"):		##This is your initial SQL statement execution.
			for entry1 in row1:
				reportfile.write("<TR>") ## this initiates a html table row
				for row2 in reportfile_cursor2.execute("SELECT key_remote_jid FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						reportfile.write("<TD>" + str(entry2) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT key_from_me FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						if str(entry2) == '1':
							reportfile.write("<TD>Sent</TD>")
						elif str(entry2) == '0':
							reportfile.write("<TD>Recieved</TD>")
				for row2 in reportfile_cursor2.execute("SELECT data FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						body = str(entry2)
						body = body.replace("\\", "\\\\")
						body = body.replace("<", "\<")
						body = body.replace(">", "\>")
						reportfile.write("<TD>" + body + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT datetime(timestamp/1000,'unixepoch','localtime') as timestamp FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						reportfile.write("<TD>" + str(entry2) + "</TD>")
				for row2 in reportfile_cursor2.execute("SELECT media_name FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						if str(entry2) == 'None':
							reportfile.write('<TD>None</TD>')
							reportfile.write('<TD>None</TD>')
						else:
							name = str(entry2)
							if os.path.isfile(os.path.join(case, "extracted data", "whatsapp", "Media", "WhatsApp Images", name)):
								file = os.path.join(case, "extracted data", "whatsapp", "Media", "WhatsApp Images", name)
								reportfile.write("<TD><img src = '" + file + "' width=\"200\" height=\"200\" /></TD>")
								reportfile.write("<TD>/Media/WhatsApp Images/" + name + "</TD>")
							elif os.path.isfile(os.path.join(case, "extracted data", "whatsapp", "Media", "WhatsApp Images", "Sent", name)):
								file = os.path.join(case, "extracted data", "whatsapp", "Media", "WhatsApp Images", "Sent", name)
								reportfile.write("<TD><img src = '" + file + "' width=\"200\" height=\"200\" /></TD>")
								reportfile.write("<TD>/Media/WhatsApp Images/Sent/" + name + "</TD>")
							else:
								reportfile.write("<TD>[Not Found] " + name + "</TD>")
								reportfile.write("<TD>" + name + "</TD>")							
				reportfile.write("</TR>") ##closes the table row
	except apsw.SQLError:
		print("Error! could not make report!")
		
def tlmake(case):
	reportfiledb = os.path.join(case, "extracted data", "whatsapp", "msgstore.db")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()

	tldb = os.path.join(case, "reports", "timeline.db")
	tl_connection = apsw.Connection(tldb)
	tl_cursor = tl_connection.cursor()
	try:
		for row1 in reportfile_cursor1.execute("SELECT _id FROM messages ORDER BY timestamp DESC"):		##This is your initial SQL statement execution.
			for entry1 in row1:
				for row2 in reportfile_cursor2.execute("SELECT key_remote_jid FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						convoid = str(entry2)
				for row2 in reportfile_cursor2.execute("SELECT key_from_me FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						if str(entry2) == '1':
							status = "Sent a message to conversation ID "
						elif str(entry2) == '0':
							status = "Received a message from conversation ID "
				for row2 in reportfile_cursor2.execute("SELECT data FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						body = str(entry2)
						body = body.replace("'", "''")
						body = body.replace('"', '""')
						body = ': ""' + body + '""'
				for row2 in reportfile_cursor2.execute("SELECT timestamp FROM messages WHERE _id = '" + str(entry1) + "'"):
					for entry2 in row2:
						date = str(entry2)
				statement= status + convoid + body
				command = "INSERT INTO 'timeline' VALUES(NULL, 'WhatsApp', '" + statement + "', " + date + ")"
				tl_cursor.execute(command)
	except apsw.SQLError:
		print("Could not extract info for timeline!")