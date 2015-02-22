#!/bin/bash

clear
echo "Connect the phone via USB, ensure Developer seetings are on and root is enabled. Press any key when ready"
read -n 1 placebo
adb shell "su -c \"sqlite3 /data/system/locksettings.db \\\"update locksettings set value=65536 where name='lockscreen.password_type';\\\"\""
