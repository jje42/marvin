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
import os
import wx


class NucleotidePage(wx.Panel):
    def __init__(self, parent, topframe):
        wx.Panel.__init__(self, parent)
        self.topframe = topframe

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        open_button = wx.Button(self, wx.ID_OPEN, 'Open')
        hbox.Add(open_button, 0, wx.LEFT|wx.RIGHT, 5)
        hbox.Add(wx.Button(self, wx.ID_SAVE, 'Save'), 0, wx.LEFT|wx.RIGHT, 5)
        hbox.Add(wx.Button(self, wx.ID_CLEAR, 'Clear'), 0, wx.LEFT|wx.RIGHT, 5) 

        self.Bind(wx.EVT_BUTTON, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=wx.ID_CLEAR)

        open_button.SetToolTipString('Open a nucleotide FastA file')

        self.text = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.text.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.text.SetForegroundColour('BLACK')

        vbox.Add((-1, 5))
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add(self.text, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(vbox)

    def OnOpen(self, event):
        filters = 'FASTA files|*.fsa;*.fasta;*.fa;*.seq'
        dia = wx.FileDialog(self,
                            'Choose a file',
                            os.getcwd(),
                            '',
                            wildcard=filters,
                            style=wx.OPEN)
        if dia.ShowModal() == wx.ID_OK:
            path = dia.GetPath()
            self.topframe.SetStatusText('You selected: {0}'.format(path))
            self.OpenFile(path)
        dia.Destroy()

    def OpenFile(self, path):
        with open(path) as f_in:
            data = f_in.read()
        self.text.AppendText(data)
        

    def OnSave(self, event):
        wild = '|'.join(['FASTA (*.fst)', '*.fsa',
                         'FASTA (*.fasta)', '*.fasta',
                         'FASTA (*.fs)', '*.fs',
                         'FASTA (*.seq)', '*.seq'])
        dia = wx.FileDialog(self, message='Save file as...',
                            defaultDir=os.getcwd(),
                            defaultFile='',
                            style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if dia.ShowModal() == wx.ID_OK:
            path = dia.GetPath()
            try:
                f_out = open(path, 'w')
                f_out.write(self.text.GetValue())
                f_out.close()
            except IOError as err:
                pass
        dia.Destroy()
 
    def OnClear(self, event):
        self.text.ChangeValue('')
