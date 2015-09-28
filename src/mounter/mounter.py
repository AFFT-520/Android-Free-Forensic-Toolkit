#!/usr/bin/env python
import sys, os, subprocess, re, pdb, time

def mount(case):
	if not os.path.isfile(case + '/image/image.dd'):
		print("Error! Could not find image.dd")
		input("Press Enter to continue")
		return
	program = subprocess.Popen('kpartx -vra ' + case + '/image/image.dd -p afft', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	loop = program.stdout.read()
	if str(loop) == "b''":
		program = subprocess.Popen('kpartx -vrag ' + case + '/image/image.dd -p afft', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		loop = program.stdout.read()
	looperr = program.stderr.read()
	looperrstr = str(looperr)
	if re.search("read error", looperrstr):
		print("Mount Failure! Is the image damaged?")
		scriptpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mountfallback.sh")
		os.system(scriptpath + " " + case)		
		input("Press Enter to continue")
		return
	else:
		loop = str(loop)
		print(loop)
		time.sleep(2)
		loopsearchstring = "/dev/loop[0-99]"
		match=re.search(loopsearchstring, loop)
		loopadd=match.group(0)
		loopid=loopadd.replace("/dev/","")
		loopnum=loopid.replace("loop","")
		for file in os.listdir("/dev/mapper"):
			if file.startswith(loopid):
				partnum = file.replace("loop" + loopnum + "afft","")
				partdir = os.path.join(case, "mount", "Partition " + partnum)
				if not os.path.exists(partdir):
					os.makedirs(partdir)
					loopdir = os.path.join("/","dev","mapper", file)
					mountoutput=subprocess.Popen('mount ' + loopdir + ' "' + partdir + '" -o ro,noexec,loop,noload', shell=True, stderr=subprocess.PIPE).stderr.read()
					print ('mount ' + loopdir + ' "' + partdir + '" -o ro,noexec,loop,noload')
					mountoutput=str(mountoutput)
					if re.search("wrong fs type", mountoutput):
						os.rmdir(partdir)
	mountedstatus = os.path.join(case, "mount", "mountstatus")
	mstatusfile = open(mountedstatus, "w")
	mstatusfile.write("1")
	mstatusfile.close()
	loopnumfile = os.path.join(case, "mount", "loopnumber")
	lnumfile = open(loopnumfile, "w")
	lnumfile.write(loopnum)
	lnumfile.close()