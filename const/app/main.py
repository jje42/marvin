# -*- mode: python; -*-
#
# Copyright (C) 2011 Jonathan Ellis
#
# Author: Jonathan Ellis <jonathan.ellis.research@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
"""
"""
import os
import wx
from wx.lib.wordwrap import wordwrap

import const
import const.app.preferences as prefs
from const.app.nucleotide import NucleotidePage
from const.app.protein import ProteinPage
from const.app.primer import PrimerPage
from const.app.help import HelpFrame
from const.app.preferences import PreferencesFrame
from const.app.codon import CodonFrame


class CustomStatusBar(wx.StatusBar):

    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, wx.ID_ANY)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-5, -1])
        ID_TIMER = wx.NewId()
        self.timer = wx.Timer(self, ID_TIMER)
        self.blink = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=ID_TIMER)

    def OnTimer(self, event):
        self.blink += 1
        if self.blink == self._duration:
            self.BackgroundColour = wx.NullColour
            self.SetStatusText('', 0)
            self.Refresh()
            self.timer.Stop()
            self.blink = 0

    def Update(self, message, duration=5, bgcolour=None):
        if bgcolour:
            self.BackgroundColour = bgcolour
        self._duration = duration
        self.timer.Start()
        self.SetStatusText(message, 0)

    def Warn(self, message, duration=5):
        self.Update(message, duration, 'RED')

    def SetMode(self, mode):
        self.SetStatusText('MODE: {0}'.format(mode), 1)
        

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1100, 700))

        self.builder = const.ConstructBuilder()

        menubar = wx.MenuBar()

        mfile = wx.Menu()
        mfile.Append(wx.ID_OPEN, '&Open', 'Open a document')
        mfile.AppendSeparator()
        #mquit = wx.MenuItem(mfile, 105, '&Quit\tCtrl+Q', 'Quit the application')
        mfile.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit the application')
        menubar.Append(mfile, '&File')

        medit = wx.Menu()
        ID_CODON = wx.NewId()
        medit.Append(ID_CODON, '&Codon Usage', 'Select codon usage table')
        medit.Append(wx.ID_PREFERENCES, '&Preferences', 'Configure the application')
        menubar.Append(medit, '&Edit')

        self.Bind(wx.EVT_MENU, self.ShowCodon, id=ID_CODON)
        self.Bind(wx.EVT_MENU, self.ShowPreferences, id=wx.ID_PREFERENCES)

        mmode = wx.Menu()
        mmode.Append(301, 'Restriction', 'Activate Restriction mode', wx.ITEM_RADIO)
        mmode.Append(302, 'LIC', 'Activate LIC mode', wx.ITEM_RADIO)
        mmode.Append(303, 'Site Mutagenesis', 'Activate Site Mutagenesis mode',
                     wx.ITEM_RADIO) 
        menubar.Append(mmode, '&Mode')

        self.Bind(wx.EVT_MENU, self.OnModeChange, id=301)
        self.Bind(wx.EVT_MENU, self.OnModeChange, id=302)
        self.Bind(wx.EVT_MENU, self.OnModeChange, id=303)
        

        mhelp = wx.Menu()
        contents = wx.MenuItem(mhelp, wx.ID_HELP, '&Contents', '')

        mhelp.AppendItem(contents)
        mhelp.AppendSeparator()
        mhelp.Append(wx.ID_ABOUT, '&About', '')
        menubar.Append(mhelp, '&Help')

        self.Bind(wx.EVT_MENU, self.OnHelp, id=wx.ID_HELP)

        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        self.SetMenuBar(menubar)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.note = wx.Notebook(self, -1)

        self.nucPage = NucleotidePage(self.note, self)
        self.protPage = ProteinPage(self.note, self)
        self.priPage = PrimerPage(self.note, self)
        self.note.AddPage(self.nucPage, 'Nucleotide')
        self.note.AddPage(self.protPage, 'Protein')
        self.note.AddPage(self.priPage, 'Primers')
        self.nucPage.SetFocus()

        vbox.Add(self.note, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vbox)
        self.statusbar = CustomStatusBar(self)
        self.statusbar.SetMode(self.builder.mode)
        self.SetStatusBar(self.statusbar)

        self.Centre()

    def OnNew(self, event):
        self.statusbar.Update('New Command')
        self.nucPage.OnClear(None)
        self.note.ChangeSelection(0)

    def OnOpen(self, event):
        self.statusbar.Update('Open Command')

    def OnSave(self, event):
        self.statusbar.Update('Save Command')

    def OnExit(self, event):
        self.Close()

    def OnModeChange(self, event):
        """Change the function mode.

        Whenever the user changes the mode, a new Builder is initiated
        (the type of which depends on the mode selected).  The protein
        canvas is cleared and if there is a nucleotide sequence loaded
        it will be re-translated.
        """
        if event.GetId() == 301:
            self.protPage.mode = 'Restrict'
            self.builder = const.ConstructBuilder()
            self.statusbar.SetMode('Restriction')
            self.protPage.OnClear(None)
            if self.nucPage.text.GetValue():            
                self.protPage.OnTranslate(None)

        elif event.GetId() == 302:
            self.protPage.mode = 'LIC'
            self.builder = const.ConstructBuilder()
            self.statusbar.SetMode('LIC')
            self.protPage.OnClear(None)
            if self.nucPage.text.GetValue():
                self.protPage.OnTranslate(None)

        elif event.GetId() == 303:
            self.protPage.mode = 'Mutate'
            self.builder = const.SiteBuilder()
            self.statusbar.SetMode('Site Mutagenisis')
            self.protPage.OnClear(None)
            if self.nucPage.text.GetValue():
                self.protPage.OnTranslate(None)

        else:
            pass

    def ShowPreferences(self, event):
        pref = PreferencesFrame(self)
        pref.Show(True)

    def ShowCodon(self, event):
        codon = CodonFrame(self, self)
        codon.Show(True)

    def OnHelp(self, event):
        h = HelpFrame(self)
        h.Show(True)

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = 'Construct'
        info.Version = const.__version__
        info.Copyright = '(C) 2010-2011 Jonathan Ellis'
        info.Description = wordwrap('Design your primers here',
                                    350, wx.ClientDC(self))
        info.WebSite = ''
        info.Developers = ['Jonathan Ellis']
        licenceText = const.__license__
        info.License = wordwrap(licenceText, 1500, wx.ClientDC(self))
        wx.AboutBox(info)
        

class Application(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, -1, 'Construct')
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = Application()
    app.MainLoop()
