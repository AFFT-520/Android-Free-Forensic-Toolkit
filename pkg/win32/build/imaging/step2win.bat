SET casepath=%1
SET workdir=%2
SET imagefile="%casepath%\image\image.dd"
cd %workdir%
..\bin\adb.exe forward tcp:5555 tcp:5555
..\bin\nc.exe 127.0.0.1 5555 > %imagefile%
..\bin\adb.exe shell 'killall busybox'