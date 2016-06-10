#!/usr/bin/env python

import apsw, getopt, os, io, sys, shutil, re, time, report.makehtml, report.makecss, zlib


def makereport(case, timeline):
	csslocation = os.path.join(case, "reports", "gmail", "report.css")
	reportfilelocation = os.path.join(case, "reports", "gmail", "report.html")
	reportfile = open(reportfilelocation, 'w')
	reportname = "GMail"
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
		dbfolder = os.path.join(case, "extracted data", "gmail", "db", "mailstore")
		for file in os.listdir(dbfolder):
			if file.endswith(".db"):
				account = file.replace("mailstore.", "")
				account = account.replace(".db","")
				reportfiledb = os.path.join(dbfolder, file)
				reportfile_connection=apsw.Connection(reportfiledb)
				reportfile_cursor1=reportfile_connection.cursor()
				reportfile_cursor2=reportfile_connection.cursor()
				reportfile_cursor3=reportfile_connection.cursor()
				
				reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
				reportfile.write("</table>\n")
				reportfile.write("<div class=\"ResultsTable\">\n")
				reportfile.write("<table>\n")
				reportfile.write("<tr class=\"title\"><td><b>From</b></td><td><b>To</b></td><td><b>Subject</b></td><td><b>Body</td></b><td><b>Sent</td></b><td><b>Received</td></b></tr>\n")
				reportfile.write("<tr><b>" + account + "</b></tr>")

				for row1 in reportfile_cursor1.execute("SELECT _id FROM messages ORDER BY dateSentMs DESC"):		##This is your initial SQL statement execution.
					for entry1 in row1:
						reportfile.write("<TR>")
						for row2 in reportfile_cursor2.execute("SELECT fromAddress FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								fromadd=str(entry2)
								fromadd=fromadd.replace("<","&#60;")
								fromadd=fromadd.replace(">","&#62;")
								reportfile.write("<TD>" + fromadd + "</TD>")
										
						for row2 in reportfile_cursor2.execute("SELECT toAddresses FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								toadd=str(entry2)
								toadd=toadd.replace("<","&#60;")
								toadd=toadd.replace(">","&#62;")
								reportfile.write("<TD>" + toadd + "</TD>")
						for row2 in reportfile_cursor2.execute("SELECT subject FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								toadd=str(entry2)
								toadd=toadd.replace("<","&#60;")
								toadd=toadd.replace(">","&#62;")
								reportfile.write("<TD>" + toadd + "</TD>")
						for row2 in reportfile_cursor2.execute("SELECT body FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								if entry2 == None:
									for row3 in reportfile_cursor3.execute("SELECT bodyCompressed FROM messages WHERE _id = " + str(entry1)):
										for entry3 in row3:
											body = zlib.decompress(entry3)
											body = str(body)
											body = body.replace("<","&#60;")
											body = body.replace(">","&#62;")
											body = body[2:-1]
											reportfile.write("<TD>" + body + "</TD>")
								else:
									body = str(body)
									body = body.replace("<","&#60;")
									body = body.replace(">","&#62;")
									reportfile.write("<TD>" + body + "</TD>")
						for row2 in reportfile_cursor2.execute("SELECT datetime(dateSentMs/1000,'unixepoch','localtime') as dateSentMs FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								reportfile.write("<TD>" + str(entry2) + "</TD>")
						for row2 in reportfile_cursor2.execute("SELECT datetime(dateReceivedMs/1000,'unixepoch','localtime') as dateRecievedMs FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								reportfile.write("<TD>" + str(entry2) + "</TD>")
						reportfile.write("</TR>") ##closes the table row

def tlmake(case):
		dbfolder = os.path.join(case, "extracted data", "gmail", "db", "mailstore")
		for file in os.listdir(dbfolder):
			if file.endswith(".db"):
				account = file.replace("mailstore.", "")
				account = account.replace(".db","")
				reportfiledb = os.path.join(dbfolder, file)
				reportfile_connection=apsw.Connection(reportfiledb)
				reportfile_cursor1=reportfile_connection.cursor()
				reportfile_cursor2=reportfile_connection.cursor()
				reportfile_cursor3=reportfile_connection.cursor()
				
				tldb = os.path.join(case, "reports", "timeline.db")
				tl_connection = apsw.Connection(tldb)
				tl_cursor= tl_connection.cursor()
				
				for row1 in reportfile_cursor1.execute("SELECT _id FROM messages ORDER BY dateSentMs DESC"):		##This is your initial SQL statement execution.
					for entry1 in row1:
						for row2 in reportfile_cursor2.execute("SELECT fromAddress FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								fromadd=str(entry2)
								fromadd=fromadd.replace("<","")
								fromadd=fromadd.replace(">","")
								fromadd=fromadd + " ==> "
										
						for row2 in reportfile_cursor2.execute("SELECT toAddresses FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								toadd=str(entry2)
								toadd=toadd.replace("<","")
								toadd=toadd.replace(">","")
								toadd = toadd + ", "
						for row2 in reportfile_cursor2.execute("SELECT subject FROM messages WHERE _id = " + str(entry1)):
							for entry2 in row2:
								sub=str(entry2)
								sub=sub.replace("<","")
								sub=sub.replace(">","")
								sub = "Subject: " + sub
						for row2 in reportfile_cursor2.execute("SELECT dateReceivedMs FROM messages WHERE _id = " + str(entry1)):
							for date in row2:
								datestr = str(date)
						message = fromadd + toadd + sub
						message = message.replace('"', '""')
						message = message.replace("'", "''")
						command = "INSERT INTO timeline VALUES(NULL, 'Gmail', '" + message + "', " + datestr + ")"
						tl_cursor.execute(command)