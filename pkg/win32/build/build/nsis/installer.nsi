!define PRODUCT_NAME "Android Free Forensic Toolkit Alpha"
!define PRODUCT_VERSION "3"
!define PY_VERSION "3.4.0"
!define PY_MAJOR_VERSION "3.4"
!define BITNESS "32"
!define ARCH_TAG ""
!define INSTALLER_NAME "Android_Free_Forensic_Toolkit_Alpha_3.exe"
!define PRODUCT_ICON "afft.ico"
 
SetCompressor lzma

RequestExecutionLevel admin

; Modern UI installer stuff 
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"

; UI pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${INSTALLER_NAME}"
InstallDir "$PROGRAMFILES${BITNESS}\${PRODUCT_NAME}"
ShowInstDetails show

Section -SETTINGS
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
SectionEnd


Section "Python ${PY_VERSION}" sec_py
  File "python-${PY_VERSION}${ARCH_TAG}.msi"
  DetailPrint "Installing Python ${PY_MAJOR_VERSION}, ${BITNESS} bit"
  ExecWait 'msiexec /i "$INSTDIR\python-${PY_VERSION}${ARCH_TAG}.msi" \
            /qb ALLUSERS=1 TARGETDIR="$COMMONFILES${BITNESS}\Python\${PY_MAJOR_VERSION}"'
  Delete $INSTDIR\python-${PY_VERSION}${ARCH_TAG}.msi
SectionEnd

Section "dateutil" sec_du
  DetailPrint "Downloading Dateutil Python Module"
  ExecWait '""$COMMONFILES${BITNESS}\Python\${PY_MAJOR_VERSION}\Scripts\pip.exe" install python-dateutil'
SectionEnd

Section "APSW" sec_apsw
  File "apsw32.exe"
  DetailPrint "Installing APSW"
  ExecWait '"$INSTDIR\apsw32.exe"'
  Delete $INSTDIR\apsw32.exe
SectionEnd

Section "!${PRODUCT_NAME}" sec_app
  SectionIn RO
  SetShellVarContext all
  File ${PRODUCT_ICON}
  SetOutPath "$INSTDIR\pkgs"
  File /r "pkgs\*.*"
  SetOutPath "$INSTDIR"
  
  ; Install files
    SetOutPath "$INSTDIR"
      File "afft.ico"
      File "Android_Free_Forensic_Toolkit_Alpha.launch.py"
  
  ; Install directories
  
  ; Install shortcuts
  ; The output path becomes the working directory for shortcuts
  SetOutPath "%HOMEDRIVE%\%HOMEPATH%"
    CreateShortCut "$SMPROGRAMS\Android Free Forensic Toolkit Alpha.lnk" "py" \
      '"$INSTDIR\Android_Free_Forensic_Toolkit_Alpha.launch.py"' "$INSTDIR\afft.ico"
  SetOutPath "$INSTDIR"
  
  ; Byte-compile Python files.
  DetailPrint "Byte-compiling Python modules..."
  nsExec::ExecToLog ' -m compileall -q "$INSTDIR\pkgs"'
  WriteUninstaller $INSTDIR\uninstall.exe
  ; Add ourselves to Add/remove programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayIcon" "$INSTDIR\${PRODUCT_ICON}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "NoRepair" 1
SectionEnd

Section "Uninstall"
  SetShellVarContext all
  Delete $INSTDIR\uninstall.exe
  Delete "$INSTDIR\${PRODUCT_ICON}"
  RMDir /r "$INSTDIR\pkgs"
  ; Uninstall files
    Delete "$INSTDIR\afft.ico"
    Delete "$INSTDIR\Android_Free_Forensic_Toolkit_Alpha.launch.py"
  ; Uninstall directories
  ; Uninstall shortcuts
      Delete "$SMPROGRAMS\Android Free Forensic Toolkit Alpha.lnk"
  RMDir $INSTDIR
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
SectionEnd


; Functions

Function .onMouseOverSection
    ; Find which section the mouse is over, and set the corresponding description.
    FindWindow $R0 "#32770" "" $HWNDPARENT
    GetDlgItem $R0 $R0 1043 ; description item (must be added to the UI)

    StrCmp $0 ${sec_app} "" +2
      SendMessage $R0 ${WM_SETTEXT} 0 "STR:${PRODUCT_NAME}"
    
FunctionEnd