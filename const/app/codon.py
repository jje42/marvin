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
Codon Usage Database (www.kazusa.or.jp/codon)
"""
import re
import urllib, urllib2
import wx

import const.codon


class CodonFrame(wx.Frame):

    def __init__(self, parent, topframe):
        wx.Frame.__init__(self, parent, title='Select Codon Usage Table')
        self.topframe = topframe
        self.search_text = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search_text.SetDescriptiveText('e.g., Escherichia coli')
        self.search_text.ShowSearchButton(False)

        search_button = wx.Button(self, wx.ID_FIND)

        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self.search_text, 1, wx.ALIGN_CENTRE_VERTICAL | wx.RIGHT,
                         5)
        search_sizer.Add(search_button, 0)

        self.species = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition)

        panel = wx.Panel(self, style=wx.SUNKEN_BORDER)
        close_button = wx.Button(panel, wx.ID_CLOSE)
        apply_button = wx.Button(panel, wx.ID_APPLY)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add((-1, 1), 1)
        button_sizer.Add(close_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        button_sizer.Add(apply_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        panel.SetSizer(button_sizer)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, label=('Search with the Latin '
                                            'name of your species:')),
                 0, wx.ALL, 10)
        vbox.Add(search_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        vbox.AddSpacer(5)
        vbox.Add(self.species, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        vbox.Add(panel, 0, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(button_sizer)
        self.SetSizer(vbox)
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.OnSearch, search_button)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, apply_button)
        self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)

        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearch, search_button)

    def OnSearch(self, event):
        try:
            result = const.codon.search(self.search_text.GetValue())
        except ValueError as err:
            msg = ('Sorry, no species found. Check your spelling\nand '
                   'try again.')
            dlg = wx.MessageDialog(self, msg, 'Error',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()            
        else:
            names = ['%s %s' % (x[0], x[1]) for x in result]
            self.d = result
            self.Populate(names)

    def OnClose(self, event):
        self.Close()
    
    def OnSelect(self, event):
        x = self.species.GetSelections()
        if x:
            x = x[0]
            sp_name, sp_id = self.d[x]
            builder = self.topframe.builder 
            builder.codon_table = const.codon.usage_table(sp_id)
            self.Close()

    def Populate(self, choices):
        self.species.Set(choices)


if __name__ == '__main__':
    
    class App(wx.App):
        def OnInit(self):
            frame = CodonFrame(None, None)
            frame.Show(True)
            return True

    app = App(1)
    app.MainLoop()
