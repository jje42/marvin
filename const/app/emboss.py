# -*- mode: python; -*-
# 
# Copyright (C) Jonathan Ellis 2010
# 
# Author: Jonathan Ellis, D.Phil
# Email:  jonathanjamesellis@gmail.com

import os
from subprocess import Popen, PIPE
import wx
import wx.richtext as richtext


class EmbossFrame(wx.Frame):
    
    def __init__(self, parent, topframe, id=wx.ID_ANY, title='EMBOSS'):
        wx.Frame.__init__(self, parent, id, title)

        self.topframe = topframe
        try:
            self.nucseq = topframe.builder.nucleotide_seq.tostring()
            self.protseq = topframe.builder.protein_seq.tostring()
        except:
            self.OnClose(None)

        vbox = wx.BoxSizer(wx.VERTICAL)


        vbox.Add(wx.Button(self, id=501, label='REMAP'), 0,
                 wx.ALL, 10)

        vbox.Add(wx.Button(self, id=502, label='RESTRICT'), 0,
                 wx.LEFT | wx.RIGHT, 10)

        vbox.Add(wx.Button(self, id=wx.ID_CLOSE, label='Close'), 0,
                 wx.ALL, 10)

        self.SetSizerAndFit(vbox)
        self.Centre()
        #self.Fit()
        self.Bind(wx.EVT_BUTTON, self.Remap, id=501)
        self.Bind(wx.EVT_BUTTON, self.Restrict, id=502)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=wx.ID_CLOSE)

    def OnClose(self, event):
        self.Destroy()

    def Remap(self, event):
        p = Popen(['remap', '-filter', '-stdout', '-auto'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(input=self.nucseq)
        if p.returncode == 0:
            e = EmbossOutputFrame(self, title='REMAP', output=stdout)
            e.Show(True)

    def Restrict(self, event):
        p = Popen(['restrict', '-filter', '-alphabetic', '-stdout', '-auto'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(input=self.nucseq)
        if p.returncode == 0:
            e = EmbossOutputFrame(self, title='RESTRICT', output=stdout,
                                  size=(900, 700))
            e.Show(True)



class EmbossOutputFrame(wx.Frame):
    
    def __init__(self, parent, id=wx.ID_ANY, title='', size=(700, 700),
                 output=None):
        wx.Frame.__init__(self, parent, id, title, size=size)

        save_bt  = wx.Button(self, id=wx.ID_SAVE, label='Save')
        close_bt = wx.Button(self, id=wx.ID_CLOSE, label='Close')        
        self.text = richtext.RichTextCtrl(self)
        self.text.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.text.AppendText(output)
        self.text.SetBackgroundColour('WHITE')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(save_bt, 0, wx.LEFT | wx.RIGHT, 5)
        hbox.Add(close_bt, 0, wx.LEFT | wx.RIGHT, 5)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, 0, wx.ALL, 10)
        vbox.Add(self.text, 1, wx.EXPAND)
        
        self.SetSizer(vbox)
        self.Centre()
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=wx.ID_SAVE)

    def OnClose(self, event):
        self.Destroy()

    def OnSave(self, event):
        wild = 'Text files|*.txt'
        dia = wx.FileDialog(self, message='Save file as...',
                            defaultDir=os.getcwd(),
                            defaultFile='',
                            wildcard=wild,
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


