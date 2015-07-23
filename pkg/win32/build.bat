xcopy ..\..\src\ .\build /q /i
xcopy .\pynsist_pkgs .\build\pynsist_pkgs
copy ..\installer.cfg .\build\installer.cfg
copy .\afft.ico .\build\afft.cio
python -m nsist installer.cfg
