#! /usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
"""Create NSIS control script.

This program creates the NSIS script needed to build a Windows installer.

"""
from __future__ import print_function, division
import os

template = '''\
; NSIS install script for construct.
; This script was automatically generated with make-nsis-script.py.
;
Name "Construct"
OutFile "construct-1.0.exe"
InstallDir $PROGRAMFILES\construct
InstallDirRegKey HKLM "Software\construct" "Install_Dir"
RequestExecutionLevel admin

;--------------------
; Pages

Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------

Section "Construct"
   SectionIn RO
   SetOutPath $INSTDIR

   ; Install files

%(install_files)s

   WriteRegStr HKLM SOFTWARE\construct "Install_Dir" "$INSTDIR"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\construct" "DisplayName" "construct"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\construct" "UninstallString" '"$INSTDIR\uninstall.exe"'
   WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\construct" "NoModify" 1
   WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\construct" "NoRepair" 1
   WriteUninstaller "uninstall.exe"
SectionEnd

Section "Start Menu Shortcuts"
   CreateDirectory "$SMPROGRAMS\construct"
   CreateShortCut "$SMPROGRAMS\construct\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
   CreateShortCut "$SMPROGRAMS\construct\Construct.lnk" "$INSTDIR\construct.exe" "" "$INSTDIR\construct.exe" 0
SectionEnd

;--------------------
;
; Uninstaller

Section "Uninstall"
   ; Remove registry keys
   DeleteRegKey HKLM "Software\Mirosoft\Windows\CurrentVersion\Uninstall\construct"
   DeleteRegKey HKLM SOFTWARE\construct

   ; Remove file and uninstaller
   
%(delete_files)s

   Delete $INSTDIR\uninstall.exe
   Delete "$SMPROGRAMS\construct\*.*"
   RMDir "$SMPROGRAMS\construct"
   RMDir "$INSTDIR"
SectionEnd
'''

fs = os.listdir(os.getcwd())

install_files = os.linesep.join(['   File "%s"' % x for x in fs])
delete_files = os.linesep.join(['   Delete "$INSTDIR\%s"' % x for x in fs])

print(template % vars())

    
