#!/usr/bin/env python

import os, sys, getopt, time, apsw, re, report.makehtml, report.makecss


	

def maketable(reportfile, case):
	reportfiledb = os.path.join(case, "extracted data", "facebook-messenger", "db", "threads_db2")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile_cursor3=reportfile_connection.cursor()
	
	reportfile.write("<table CELLPADDING=8 CELLSPACING=0 VALIGN=TOP>\n")
	reportfile.write("<tr><td><a href=reportfile-contacts.html>Contacts</a></td></tr>\n")
	reportfile.write("</table>\n")
	reportfile.write("<div class=\"ResultsTable\">\n")
	reportfile.write("<table>\n")
	reportfile.write("<tr><td><b>Conversation</b></td><td><b>Message</b></td><td><b>Sent By</b></td><td><b>Attachments</b></td><td><b>Coordinates</b></td><td><b>Time</b></td></tr>\n")

	for row1 in reportfile_cursor1.execute("select msg_id from messages order by timestamp_ms DESC"):
		for entry1 in row1:
			reportfile.write("<TR>\n")
			for row2 in reportfile_cursor2.execute("select thread_key from messages WHERE msg_id = '" + str(entry1) + "'"):
				for entry2 in row2:
						for row3 in reportfile_cursor3.execute("select participants from threads where thread_key = '" + str(entry2) + "'"):
							for entry3 in row3:							
								entrylist = str(entry3)
								entrylist = entrylist.replace("{", "")
								entrylist = entrylist.replace('"', '')
								entrylist = entrylist.replace('}', '')
								entrylist = entrylist.replace('[', '')
								entrylist = entrylist.replace(']', '')
								entrylist = entrylist.split(",")
								lenlist = len(entrylist)
								countlist = 0
								name = re.compile('name:')
								writelist = ""
								while countlist != lenlist:
									if name.match(entrylist[countlist]):
										writelist = writelist + " " + entrylist[countlist] + ","
									countlist = countlist + 1
								threadkey = str(entry2)
								threadkey = threadkey.split(":")
								if threadkey[0] == "ONE_TO_ONE":
									writelist = "&#40;Private Message&#41;" + writelist
								elif threadkey[0] == "GROUP":
									writelist = "&#40;Group Conversation&#41;" + writelist
								writelist = writelist.replace("name:","")
								reportfile.write("<TD>" + writelist[:-1] + "</TD>\n")
				for row2 in reportfile_cursor2.execute("select text from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						text = str(entry2)
						text = text.replace("<", "\<")
						text = text.replace(">", "\>")
						reportfile.write("<TD>" + text + "</TD>\n")
			
				for row2 in reportfile_cursor2.execute("select sender from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						senderdetails = str(entry2)
						senderdetails = senderdetails.replace("{", "")
						senderdetails = senderdetails.replace('"', '')
						senderdetails = senderdetails.replace('}', '')
						senderdetails = senderdetails.replace('email:', '')
						senderdetails = senderdetails.replace('user_key:', '')
						senderdetails = senderdetails.replace('name:', '')
						senderlist = senderdetails.split(',')
						if len(senderlist) == 3:
							reportfile.write("<TD>" + senderlist[2] + "</TD>\n")
						else:
							reportfile.write("<TD>N/A</TD>")
					
				for row2 in reportfile_cursor2.execute("select attachments from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						if str(entry2) == '[]':
							entry_str2 = 'None'
						else:
							attachmentre = re.compile(r"(filename\":\".*?\")")
							attachresults = attachmentre.findall(entry2)
							attresults_tmp1 = str(attachresults)
							attresults_tmp2 = attresults_tmp1.replace('[\'filename":"',"")
							entry_str2 = attresults_tmp2.replace('"\']','')
						reportfile.write("<TD>" + entry_str2 + "</TD>\n")
					
				for row2 in reportfile_cursor2.execute("select coordinates from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						coord_list = str(entry2)
						coord_list = coord_list.replace("{", "")
						coord_list = coord_list.replace('"latitude":', "")
						coord_list = coord_list.replace('"longitude":', "")
						coord_list = coord_list.replace('"accuracy":', "")
						coord_list = coord_list.replace("}", "")
						coord_list = coord_list.replace(",", " ")
						coord = coord_list.split()
						if len(coord) == 1:
							reportfile.write("<TD>N/A</TD>")
						else:
							lat = float(coord[0])
							lat = "%0.4f" % lat
							
							lon = float(coord[1])
							lon = "%0.4f" % lon
							if len(coord) == 2:
								reportfile.write("<TD><a href='https://www.google.com/maps/preview/@" + str(coord[0]) + "," + str(coord[1]) + ",15z'>Latitude of " + str(lat) + ", Longitude of " + str(lon) + "</a></TD>")
							else:
								accuracy = float(coord[2])
								zoom = int(accuracy)
								reportfile.write("<TD><a href='https://www.google.com/maps/preview/@" + str(coord[0]) + "," + str(coord[1]) + "," + str(zoom) + "z'> Latitude of " + str(lat) + ", Longitude of " + str(lon) + " to the accuracy of " + str(accuracy) + "meters</a></TD>")
				for row2 in reportfile_cursor2.execute("select datetime(timestamp_ms/1000,'unixepoch','localtime') as timestamp_ms from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						reportfile.write("<TD>" + str(entry2) + "</TD>\n")
					
			reportfile.write("</TR>\n")
	reportfile.write("</table>\n")
	reportfile.write("</div>\n")


def tlmake(case):
	reportfiledb = os.path.join(case, "extracted data", "facebook-messenger", "db", "threads_db2")
	reportfile_connection=apsw.Connection(reportfiledb)
	reportfile_cursor1=reportfile_connection.cursor()
	reportfile_cursor2=reportfile_connection.cursor()
	reportfile_cursor3=reportfile_connection.cursor()

	tldb = os.path.join(case, "reports", "timeline.db")
	tl_connection = apsw.Connection(tldb)
	tl_cursor = tl_connection.cursor()
	
	for row1 in reportfile_cursor1.execute("select msg_id from messages order by timestamp_ms DESC"):
		for entry1 in row1:
			for row2 in reportfile_cursor2.execute("select thread_key from messages WHERE msg_id = '" + str(entry1) + "'"):
				for entry2 in row2:
						for row3 in reportfile_cursor3.execute("select participants from threads where thread_key = '" + str(entry2) + "'"):
							for entry3 in row3:							
								entrylist = str(entry3)
								entrylist = entrylist.replace("{", "")
								entrylist = entrylist.replace('"', '')
								entrylist = entrylist.replace('}', '')
								entrylist = entrylist.replace('[', '')
								entrylist = entrylist.replace(']', '')
								entrylist = entrylist.split(",")
								lenlist = len(entrylist)
								countlist = 0
								name = re.compile('name:')
								writelist = ""
								while countlist != lenlist:
									if name.match(entrylist[countlist]):
										writelist = writelist + " " + entrylist[countlist] + ","
									countlist = countlist + 1
								threadkey = str(entry2)
								threadkey = threadkey.split(":")
								private = False
								if threadkey[0] == "ONE_TO_ONE":
									writelist = "in a private conversation involving" + writelist
									private = True
								elif threadkey[0] == "GROUP":
									writelist = "to a group conversation involving:" + writelist
								writelist = writelist.replace("name:","")
								writelist = writelist[:-1]
								writelist = writelist.replace('"', '""')
								writelist = writelist.replace("'", "''")
								if private == 1:
									
									writelist = writelist.replace(",", " and")
				for row2 in reportfile_cursor2.execute("select text from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						text = str(entry2)
						text = text.replace("<", "&#60;")
						text = text.replace(">", "&#62;")
						text = text.replace('"', '""')
						text = text.replace("'", "''")
						text = '""' + text + '""'
			
				for row2 in reportfile_cursor2.execute("select sender from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						senderdetails = str(entry2)
						senderdetails = senderdetails.replace("{", "")
						senderdetails = senderdetails.replace('"', '')
						senderdetails = senderdetails.replace('}', '')
						senderdetails = senderdetails.replace('email:', '')
						senderdetails = senderdetails.replace('user_key:', '')
						senderdetails = senderdetails.replace('name:', '')
						senderlist = senderdetails.split(',')
						if len(senderlist) == 3:
							sender = senderlist[2]
							sender = sender.replace("'","''")
							sender = sender.replace('"', '""')
						else:
							sender = "Someone"
						sender = sender + " sent "
					
				for row2 in reportfile_cursor2.execute("select coordinates from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						coord_list = str(entry2)
						coord_list = coord_list.replace("{", "")
						coord_list = coord_list.replace('"latitude":', "")
						coord_list = coord_list.replace('"longitude":', "")
						coord_list = coord_list.replace('"accuracy":', "")
						coord_list = coord_list.replace("}", "")
						coord_list = coord_list.replace(",", " ")
						coord = coord_list.split()
						if len(coord) == 1:
							coordstatement = "."
						else:
							lat = float(coord[0])
							lat = "%0.4f" % lat
							
							lon = float(coord[1])
							lon = "%0.4f" % lon
							if len(coord) == 2:
								coordstatement = ". They were located at " + str(lat) + "," + str(lon)
							else:
								accuracy = float(coord[2])
								zoom = int(accuracy)
								coordstatement = ". They were located at " + str(lat) + "," + str(lon) + " (Accurate to " + str(accuracy) + " meters)"
				for row2 in reportfile_cursor2.execute("select timestamp_ms from messages WHERE msg_id = '" + str(entry1) + "'"):
					for entry2 in row2:
						date = str(entry2)
				statement = sender + text + writelist + coordstatement
				command = "INSERT INTO timeline VALUES(NULL, 'Facebook Messenger', '" + statement + "', " + date + ")"

				tl_cursor.execute(command)
	

def makereport(case, timeline):
	
	reportlocation = os.path.join(case, "reports", "facebook-messenger", "report.html")
	reportfile = open(reportlocation, 'w')
	reportname = "Facebook Messenger Messages"
	
	report.makehtml.makehead(reportfile, reportname)
	report.makehtml.importnavbar(reportfile, case)
	report.makehtml.makemid(reportfile)
	cssfile = os.path.join (case, "reports", "facebook-messenger", "report.css")
	css = open(cssfile, 'w')
	report.makecss.makecss(css)
	css.close()
	maketable(reportfile, case)
	if timeline:
		tlmake(case)
	
	
	reportfile.close()
	
	


