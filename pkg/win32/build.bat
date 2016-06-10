rd .\build /q /s
mkdir .\build
mkdir .\build\build
mkdir .\build\build\nsis
copy .\apsw32.exe .\build\build\nsis\
copy .\default.nsi .\build\default.nsi
xcopy ..\..\src\* .\build /q /i /s
copy .\installer.cfg .\build\installer.cfg
copy .\afft.ico .\build\afft.ico
py -m nsist .\build\installer.cfg
.\build\build\nsis\Android_Free_Forensic_Toolkit_Alpha_3.exe
