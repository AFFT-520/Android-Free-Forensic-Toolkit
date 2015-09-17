# Android-Free-Forensic-Toolkit
AFFT is a toolkit to automatically acquire and extract data from Android image dumps. It can perform the following tasks:

-Imaging over USB
-Extraction of supported app data
-Write HTML reports based on said app data
-Create a global timeline of events based on said app data

CURRENTLY SUPPORTED APPS

- Facebook (including Messenger)
- Skype
- Whatsapp 
- Gmail
- Tinder
- Google Maps
- Google Calendar
- SMS/MMS (regardless of app used)
- AOSP Contacts
- AOSP Dialler (Call log)


REQUIREMENTS 

Host PC:

- Windows Linux PC with Python 3.4 and APSW and dateutil installed (packaged versions supply these for you)
- ADB, as distributed via the Google Android SDK. (Provided for you in Windows)
- (Packaging only) NSIS and pynsist

Client Android device:

- Must be rooted
- Must have BusyBox installed
- Must have USB Debug enabled


HOW TO INSTALL

- Windows

Run the .exe file and let it install

- Linux

Install the appropriate packages for your system, or download the source and install Python3.4 with APSW and dateutil.


HOW TO USE

- Open the program. Upon first running, it will display a legal disclaimer and ask you where you wish to store case files. 
- Give the case a name. Case folders will appear in your home directory under 'afft-cases'
- Plug in your desired device, make sure it is in developer mode and rooted.
- The extraction function relies on the image being mounted before executing this function

BUG-REPORTS

I am interested in all bug reports and contributions. All contributions must be under the GPLv2 license (or compatible) to be considered for merging into mainline. Of particular importance are the following:

- Phone compatibility reports patches - This is only tested on the Google Nexus 5 phone and Google Nexus 7 (2012 model) tablet. As many manufacturers diverge from stock Android, compatibility issues are of paramount concern.

- Extractor scripts for particular apps, and any compatibility issues surrounding them (I have provide a template with instructions for writing your own scripts)


TO-DO

- Full Google Applications stack support
- Adapt the extraction scripts for use on removable media on the device itself (sans PC)
- Twitter Support
- Documentation
- DEB/RPM packages

FAQ:

Any Windows or OSX support?

Windows is supported, albeit with some limitations. The mounting scripts will not work on either, the former due to a lack of loopback interfaces and the latter due to lack of EXT 2/3/4 support. As such, a third party progrma like FTK Imager will have to handle mounting. Imaging should work fine so long as you have netcat-traditional installed on the PC. Extractions and reporting tools should otherwise be perfectly functioning with minor differences. All extracted data is presented in universal formats, so the data can be extracted and then read on any OS.

OSX **should** work, but with the same limitations. However I do not have a Mac to test compatibility, and as such I have not released end-user packages for the system either. As such, using this on Mac OSX should be considered only by those that know what they are doing.

Any chance of support for X app?

File a report and we will consider it. If the app is fairly popular and holds data potentially useful to an investigation, I will try to incorporate it into the program

This doesn't work on phone/tablet X!

Leave a issue ticket here detailing the device model, Android version and custom ROM name (if one is being used), and I will try my best to get it working.

Will this work on Android Wear devices (smartwatches)

I have no reason to believe it will as things stand. I am more than happy to write support for it however.


LEGAL

LICENSE
This program is licensed under GPLv2. Full details of the license are provided in the LICENSE file. In essence, feel free to share this with your friends, modify it, improve upon it, sell support, etc. BUT: You cannot distribute a copy that has my name (or the name of any other contributer) removed, nor can you remove the GPLv2 licensing. If you distribute a modified version in binary (somehow) you must also distribute the source code, and both must be licensed under GPLv2 or compatible.

DISCLAIMER
This program is provided under the understanding that it is to be used on devices only for purposes where lawful authorisation is in place (including but not limited to: your own device, a device for which you have express and fully-informed permission from the owner, a device for which you have a valid subpoena regarding it's data, etc). By using this program, or by modifying the disclaimer key in the program's setting file, you hereby state that you understand this and accept any consequences that arise from the use of this tool, and that neither the program's author or contributors are responsible for your use of the tool. The tool notifies the user on first startup and records affirmative responses for each user.