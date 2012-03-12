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
from Bio.Seq import Seq

class CodonError(Exception):
    pass

class PrimerPage(wx.Panel):

    def __init__(self, parent, topframe):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.topframe   = topframe
        self.constructs     = None
        
        self.design_bt  = wx.Button(self, wx.ID_ANY, 'Design')
        self.update_bt  = wx.Button(self, wx.ID_ANY, 'Update Translations')
        self.save_bt    = wx.Button(self, wx.ID_SAVE, 'Save')
        self.clear_bt   = wx.Button(self, wx.ID_CLEAR, 'Clear')
        self.rb1        = wx.RadioButton(self, label='Melting Temperature:',style=wx.RB_GROUP)
        self.temp_spin  = wx.SpinCtrl(self, min=0, max=200, initial=65)
        self.rb2        = wx.RadioButton(self, label='Number of Bases:')
        self.base_spin  = wx.SpinCtrl(self, min=1, max=100, initial=18)
        self.t0         = wx.StaticText(self, label='Tag:')
        self.t0.SetToolTip(wx.ToolTip('This tag will be added to the start of\neach primer'))
        self.tag        = wx.TextCtrl(self, value='')

        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.t1         = wx.StaticText(self, label='Primers:')
        self.primer_win = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.primer_win.SetFont(font)

        self.t3 = wx.StaticText(self, label='Primer Translation:')
        self.trans_win = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.trans_win.SetFont(font)
        self.t2         = wx.StaticText(self, label='Sequences:') 
        self.seq_win    = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.seq_win.SetFont(font)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.design_bt, 0, wx.LEFT | wx.RIGHT, 5)
        hbox.Add(self.update_bt, 0, wx.LEFT | wx.RIGHT, 5)
        hbox.Add(self.save_bt,   0, wx.LEFT | wx.RIGHT, 5)
        hbox.Add(self.clear_bt,  0, wx.LEFT | wx.RIGHT, 5)

        opts_box = wx.BoxSizer(wx.HORIZONTAL)
        opts_box.Add(self.rb1,       0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        opts_box.Add(self.temp_spin, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        opts_box.Add(self.rb2,       0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        opts_box.Add(self.base_spin, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        opts_box.Add(self.t0,        0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        opts_box.Add(self.tag,       1, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 5))
        vbox.Add(hbox,            0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(opts_box,        0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.t1,         0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.primer_win, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.t3,         0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.trans_win,  1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.t2,         0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.seq_win,    1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)

        self.Bind(wx.EVT_BUTTON, self.OnDesign, id=self.design_bt.GetId())
        self.Bind(wx.EVT_BUTTON, self.UpdateTranslations, id=self.update_bt.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_SPINCTRL, self.TempSpin, id=self.temp_spin.GetId())
        self.Bind(wx.EVT_SPINCTRL, self.BaseSpin, id=self.base_spin.GetId())

        self.SetSizer(vbox)

    def TempSpin(self, event):
        self.rb1.SetValue(True)

    def BaseSpin(self, event):
        self.rb2.SetValue(True)

    def OnClear(self, event):
        self.primer_win.ChangeValue('')
        self.seq_win.ChangeValue('')
        self.trans_win.ChangeValue('')
        self.constructs = None

    def OnDesign(self, event):
        if self.rb1.GetValue():
            kwds = {'temperature': self.temp_spin.GetValue()}
        elif self.rb2.GetValue():
            kwds = {'primer_length': self.base_spin.GetValue()}
        else:
            print 'ERROR'

        try:
            self.constructs = self.topframe.builder.design(**kwds)
        except CodonError as err:
            self.topframe.statusbar.Warn('No codon usage table set - '
                                         'using E. coli (go to Edit '
                                         '-> Codon Usage)')
            self.constructs = self.topframe.builder.design(use_default=True,
                                                           **kwds)
        for construct in self.constructs:
            self.print_primer(construct.forward_primer)
            self.print_primer(construct.reverse_primer)

        for construct in self.constructs:
            self.seq_win.AppendText(
                '%s-%s:%s\n' % (construct.start_position,
                                construct.stop_position,
                                construct.protein_seq))
                
                
        self.UpdateTranslations(None)

    def print_primer(self, primer):
        t = self.tag.GetValue()
        tag = '%s%s' % (t, '_' if t else '')
        win = self.primer_win
        win.SetForegroundColour('black')
        if primer.reverse:
            win.AppendText('%s%s_RV:' % (tag, primer.position))
        else:
            win.AppendText('%s%s_FW:' % (tag, primer.position))
        win.SetForegroundColour('blue')
        win.AppendText(primer.overhang)
        win.SetForegroundColour('red')
        win.AppendText(primer.cloning_seq)
        win.SetForegroundColour('green')
        win.AppendText(primer.start_stop)
        win.SetForegroundColour('black')
        win.AppendText(primer.primer)
        win.AppendText(os.linesep)
            
    def UpdateTranslations(self, event):
        """Translate primer.

        Translate each primer in all three reading frames and display the
        protein sequence in the translation window.
        
        """
        def display_lines(lines):
            for line in lines:
                prefix, seq = line.split(':')
                s = Seq(seq)
                if 'RV' in prefix:
                    s = s.reverse_complement()
                for i in range(3):
                    prot = s[i:].translate()
                    self.trans_win.AppendText(
                        'Frame_%d_%s:%s%s' % (i+1, prefix, prot, os.linesep)) 

        self.trans_win.SetValue('')
        text = self.primer_win.GetValue()
        display_lines([L for L in text.splitlines() if 'FW' in L])
        display_lines([L for L in text.splitlines() if 'RV' in L])

    def OnSave(self, event):
        if self.constructs:
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
                except IOError:
                    pass
                else:
                    t = self.tag.GetValue()
                    tag = '%s%s' % (t, '_' if t else '')

                    for construct in self.constructs:
                        f_out.write('%s%sFW:%s%s' % (
                            tag, construct.start_position,
                            construct.forward_primer, os.linesep))
                        f_out.write('%s%sRV:%s%s' % (
                            tag, construct.stop_position,
                            construct.reverse_primer, os.linesep))

                    for construct in self.constructs:
                        f_out.write('%d-%d:%s%s' % (
                            construct.start_position,
                            construct.stop_position,
                            construct.protein_seq,
                            os.linesep))
                    f_out.close()
            dia.Destroy()
        else:
            self.topframe.statusbar.Warn(
                'There are no constructs to save')
