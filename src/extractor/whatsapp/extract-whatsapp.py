#!/usr/bin/env python
import sys, os, shutil, binascii, apsw, zlib
from Crypto.Cipher import AES

def extract (case, userdata):
	if os.path.exists(os.path.join(userdata, "data", "com.whatsapp")):
		extractdir = os.path.join(case, "extracted data")
		if not os.path.exists(extractdir):
			os.makedirs(extractdir)
		extractdir = os.path.join(extractdir, "whatsapp")
		if not os.path.exists(extractdir):
			os.makedirs(extractdir)

		keysource = os.path.join(userdata, "data", "com.whatsapp", "files", "key")
		keydest = os.path.join(case, "extracted data", "whatsapp", "key")
		dbsource = os.path.join(userdata, "media", "0", "WhatsApp", "Databases", "msgstore.db.crypt8")
		dbdest = os.path.join(case, "extracted data", "whatsapp", "msgstore.db.crypt8")
		dbnohead = os.path.join(case, "extracted data", "whatsapp", "msgstore.db.nohead")
		dbtmp = os.path.join(case, "extracted data", "whatsapp", "msgstore.db.tmp")
		dbdecrypt = os.path.join(case, "extracted data", "whatsapp", "msgstore.db.decrypted")

		shutil.copyfile(keysource, keydest)
		shutil.copyfile(dbsource, dbdest)

	
		#os.system('bin\\dd.exe if="' + dbdest + '" of="' + dbnohead + '" ibs=67 skip=1 ' if os.name == 'nt' else 'dd if="' + dbdest + '" of="' + dbnohead + '" ibs=67 skip=1 >/dev/null 2>&1')
		sourcefile = open(dbdest, "rb")
		sourcefileread = sourcefile.read()
		dbdestfile = open(dbnohead, "wb")
		dbdestfile.write(sourcefileread[67:])
		dbdestfile.close()

		
		gziphead = "1f8b080000000000"
		gzipheadbytes = binascii.unhexlify(gziphead)
		keyfile = open(keydest, "rb")
		tmpfile = open(dbtmp, "wb")
		dbdestfile = open(dbnohead, "rb")
		#tmpfile.write(gzipheadbytes)
		with keyfile as f:
			for chunk in iter(lambda: f.read(160), b''):
				keystring = str(binascii.hexlify(chunk))
				keystring = keystring.replace('\'', '')
				key = binascii.unhexlify(keystring[253:317])
				iv = binascii.unhexlify(keystring[221:253])
				cipher = AES.new(key, AES.MODE_CBC, iv)
				chunk = cipher.decrypt(dbdestfile.read())
				tmpfile.write(chunk)	
		keyfile.close()
		tmpfile.close()
		dbdestfile.close()			
		
		tmpfile = open(dbtmp, "rb")
		tmptogzip = tmpfile.read()
		finaldb = open(dbdecrypt, "wb")
		d = zlib.decompressobj(16+zlib.MAX_WBITS)
		decompressdata=d.decompress(tmptogzip)
		finaldb.write(decompressdata)
		tmpfile.close()
		finaldb.close()
		
		#os.system('bin\\gzip.exe -d < "' + dbtmp + '" > "' + dbdecrypt + '"' if os.name == 'nt' else 'gzip -d < "' + dbtmp + '" > "' + dbdecrypt + '" 2>&1' )
		print("--> Extracting WhatsApp data\n\n")
		txtoutput = os.path.join(case, "extracted data", "whatsapp", "messages.txt")
		txtoutfile = open(txtoutput, 'w', encoding='utf8')
		sqlconnection = apsw.Connection(dbdecrypt)
		sqlshell = apsw.Shell(stdout=txtoutfile, db=sqlconnection)
		sqlshell.process_command('.header on')
		sqlshell.process_sql('select * from messages')
		txtoutfile.close()
		
		os.remove(dbtmp)
		os.remove(dbnohead)

	else:
		print("--> Not extracting WhatsApp data. Reason: Not found\n\n")
	

