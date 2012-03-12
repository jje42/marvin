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
import wx
import wx.richtext as richtext


class HelpFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Help', size=(500, 500))

        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER |
                                     wx.TB_FLAT | wx.TB_TEXT)

        toolbar.AddSeparator()
        toolbar.AddSimpleTool(wx.ID_EXIT,
                              wx.ArtProvider_GetBitmap(wx.ART_QUIT),
                              'Exit',
                              'Exit')
        toolbar.Realize()

        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)

        statusbar = self.CreateStatusBar()

        self.text = richtext.RichTextCtrl(self)

        self.text.BeginAlignment(richtext.TEXT_ALIGNMENT_CENTRE)
        self.text.BeginBold()
        self.text.BeginFontSize(14)
        self.text.WriteText("Sorry, you're on your own.\n")
        self.text.EndFontSize()
        self.text.EndBold()
        self.text.EndAlignment()

        self.text.Newline()
        self.text.WriteText("There's no help yet, try comming back "
                            "later.\n")

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.text, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(vbox)

    def OnClose(self, event):
        self.Destroy()    
