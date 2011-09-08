# -*- mode: python -*-
# 
# Copyright (C) Jonathan Ellis 2010
# 
# Author: Jonathan Ellis, D.Phil
# Email:  jonathanjamesellis@gmail.com
# 
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
