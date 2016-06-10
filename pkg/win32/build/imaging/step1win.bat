SET dev=%1
SET workdir=%2
cd %workdir%
..\bin\adb.exe forward tcp:5555 tcp:5555
..\bin\adb.exe shell "su -c \"busybox nc -l -p 5555 -e busybox dd if=/dev/block/%dev%\""