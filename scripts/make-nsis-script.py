#! /usr/bin/env python
"""Create NSIS control script.

This program creates the NSIS script needed to build a Windows installer.

"""
from __future__ import print_function, division
import os

template = '''\
; NSIS install script for marvin.
; This script was automatically generated with make-nsis-script.py.
;
Name "Marvin"
OutFile "marvin-0.6.exe"
InstallDir $PROGRAMFILES\marvin
InstallDirRegKey HKLM "Software\marvin" "Install_Dir"
RequestExecutionLevel admin

;--------------------
; Pages

Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------

Section "Marvin"
   SectionIn RO
   SetOutPath $INSTDIR

   ; Install files

%(install_files)s

   WriteRegStr HKLM SOFTWARE\marvin "Install_Dir" "$INSTDIR"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\marvin" "DisplayName" "marvin"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\marvin" "UninstallString" '"$INSTDIR\uninstall.exe"'
   WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\marvin" "NoModify" 1
   WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\marvin" "NoRepair" 1
   WriteUninstaller "uninstall.exe"
SectionEnd

Section "Start Menu Shortcuts"
   CreateDirectory "$SMPROGRAMS\marvin"
   CreateShortCut "$SMPROGRAMS\marvin\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
   CreateShortCut "$SMPROGRAMS\marvin\Marvin.lnk" "$INSTDIR\marvin.exe" "" "$INSTDIR\marvin.exe" 0
SectionEnd

;--------------------
;
; Uninstaller

Section "Uninstall"
   ; Remove registry keys
   DeleteRegKey HKLM "Software\Mirosoft\Windows\CurrentVersion\Uninstall\marvin"
   DeleteRegKey HKLM SOFTWARE\marvin

   ; Remove file and uninstaller
   
%(delete_files)s

   Delete $INSTDIR\uninstall.exe
   Delete "$SMPROGRAMS\marvin\*.*"
   RMDir "$SMPROGRAMS\marvin"
   RMDir "$INSTDIR"
SectionEnd
'''

fs = os.listdir(os.getcwd())

install_files = os.linesep.join(['   File "%s"' % x for x in fs])
delete_files = os.linesep.join(['   Delete "$INSTDIR\%s"' % x for x in fs])

print(template % vars())

    
