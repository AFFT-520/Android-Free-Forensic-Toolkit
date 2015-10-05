# Android-Free-Forensic-Toolkit
AFFT is a toolkit to automatically acquire and extract data from Android image dumps.

CURRENTLY SUPPORTED APPS

- Facebook (including Messenger)
- Skype
- Whatsapp 
- Gmail
- SMS/MMS (regardless of app used)
- AOSP Contacts
- AOSP Dialler (Call log)


REQUIREMENTS 

Host PC:

- Linux OS (tested on Ubuntu 14.04)
- SQLite3
- 'pv' command
- ADB, as distributed via the Google Android SDK. This must also be in your $PATH

Client Android device:

- Must be rooted
- Must have BusyBox installed
- Must have USB Debug enabled


HOW TO INSTALL

Either install from the Debian package 

or 

Install dependencies and copy the contents of 'afft-src' to /opt/afft/


HOW TO USE

- Run /opt/afft/main.sh
- Give the case a name. Case folders will appear in your home directory under 'afft-cases'
- Hook up your desired device, make sure it is in developer mode
- Select Option 1 to image the device. Give the the name of the device's drive/partition you want to image (usually mmcblk0)
- Select Option 2 to try and mount the image partitions as read-only. If this fails or the partition mounts are incomplete, use option 4 then Option 5 and retry this step.
- Select Option 3 to extract any data it can from the mounted images.

BUG-REPORTS

I am interested in all bug reports and contributions. All contributions must be under the GPLv2 license (or compatible) to be considered for merging into mainline. Of particular importance are the following:

- Phone compatibility reports patches - This is only tested on the Google Nexus 5 phone and Google Nexus 7 (2012 model) tablet. As many manufacturers diverge from stock Android, compatibility issues are of paramount concern.

- Extractor scripts for particular apps, and any compatibility issues surrounding them (I have provide a template with instructions for writing your own scripts)


TO-DO

- Support for the full AOSP app stack
- Full Google Applications stack support (currently only Gmail is supported)
- Adapt the extraction scripts for use on removable media on the device itself (sans PC)
- Tinder Support
- Twitter Support
- Report generating via LaTeX


FAQ:

Any Windows or OSX support?

Only partial. The data extraction scripts will not work on either, the former due to a lack of loopback interfaces and the latter due to lack of EXT 2/3/4 support. Imaging should work fine so long as you have netcat-traditional and pv installed on the PC. All extracted data is presented in universal formats, so the data can be extracted using a Live-CD and then read on any OS.

Any chance of support for X app?

File a report and we will consider it. If the app is fairly popular and holds data potentially useful to an investigation (eg: Google Maps = yes, Sonic Dash = no) I will try to incorporate it into the program

This doesn't work on phone/tablet X!

Leave a ticket on the Sourceforge page detailing the phone model, Android version and custom ROM name (if one is being used), and I will try my best to get it working.


LEGAL

LICENSE
This program is licensed under GPLv2. Full details of the license are provided in the LICENSE file. In essence, feel free to share this with your friends, modify it, improve upon it, sell support, etc. BUT: You cannot distribute a copy that has my name (or the name of any other contributer) removed, nor can you remove the GPLv2 licensing. If you distribute a modified version in binary (somehow) you must also distribute the source code, and both must be licensed under GPLv2 or compatible.

The Windows packager for the toolkit also distributes some free/open source software, notably ADB and Rodney Beede's Win32 port of Netcat. 

* The Netcat family, including this build, is GPLv2 software, and the source for the build used here can be found at: https://www.rodneybeede.com/downloads/nc111nt_rodneybeede.zip

* ADB is licensed under Apache 2.0 The source code for ADB can be found at https://android.googlesource.com/platform/system/core/+/android-4.4_r1/adb/adb.c

DISCLAIMER
This program is provided under the understanding that it is to be used on devices only for purposes where lawful authorisation is in place (including but not limited to: your own device, a device for which you have express and fully-informed permission from the owner, a device for which you have a valid subpoena regarding it's data, etc). By using this program, you hereby state that you understand this and accept any consequences that arise from the use of this tool, and that neither the program's author or contributors are responsible for your use of the tool. The tool notifies the user on first startup and records affirmative responses for each user.
