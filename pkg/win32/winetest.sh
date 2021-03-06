#!/bin/bash
rm -rf ./build
cp -rf ../../src ./build
cp ../installer.cfg ./build/installer.cfg
cp ./afft.ico ./build/afft.ico
mkdir pynsist_pkgs
7z x ./win-binaries/apsw-3.8.10.1-r1.win32-py3.4.exe -oapsw
cp -rf apsw ./pynsist_pkgs/apsw
rm -rf apsw
cp -rf ./pynsist_pkgs ./build/pynsist_pkgs
cd build
python3.4 -m nsist installer.cfg
wine ./build/nsis/Android_Free_Forensic_Toolkit_Alpha_3.exe
wine py.exe C:\\Program\ Files\ \(x86\)\\Android\ Free\ Forensic\ Toolkit\ Alpha\\Android_Free_Forensic_Toolkit_Alpha.launch.py
