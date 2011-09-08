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
import sys
import pprint
import platform
import cPickle
import wx
import wx.lib.mixins.listctrl as listmix


class PreferencesFrame(wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Preferences',
                          size=(400, 650))

        self.prefs = get_preferences()

        note = wx.Notebook(self, wx.ID_ANY)

        predPage = PredictorPage(note, self)
        resPage = RestrictionPage(note, self)
        licPage = LICPage(note, self)
        tagPage = TagPage(note, self)
        
        note.AddPage(predPage, 'Predictors')
        note.AddPage(resPage, 'Restriction')
        note.AddPage(licPage, 'LIC')
        note.AddPage(tagPage, 'Tags')

        close = wx.Button(self, wx.ID_CLOSE, 'Close')
        close.SetFocus()
        self.Bind(wx.EVT_BUTTON, self.OnClose)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(note, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)
        vbox.Add(close, 0, wx.ALL | wx.ALIGN_RIGHT, 10)

        self.SetSizer(vbox)
        self.Centre()

    def OnClose(self, event):
        ## config_file = get_config_file_name()
        ## try:
        ##     f_out = open(config_file, 'w')
        ## except IOError:
        ##     pass
        ## else:
        ##     pprint.pprint(self.prefs, f_out)
        ##     f_out.close()
        save(self.prefs)
        self.Destroy()


class PredictorPage(wx.Panel):
    def __init__(self, parent, topframe):
        wx.Panel.__init__(self, parent)
        self.topframe = topframe
        predictors = self.topframe.prefs['predictors']

        vbox = wx.BoxSizer(wx.VERTICAL)

        t = wx.StaticText(self, label='Select predictors to use')
        vbox.Add(t, 0, wx.ALL, 10)

        d = [(o, (p, c, u)) for p, (o, c, u) in predictors.iteritems()]
        d.sort()

        predictors = [(p, (o, c, u)) for (o, (p, c, u)) in d]

        for predictor, (order, classname, use) in predictors:
            cb = wx.CheckBox(self, wx.ID_ANY, predictor)
            vbox.Add(cb, 0, wx.LEFT | wx.RIGHT, 10)
            if use:
                cb.SetValue(True)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def OnCheck(self, event):
        obj = event.GetEventObject()
        self.topframe.prefs['predictors'][obj.GetLabel()][2] = obj.GetValue()

class RestrictionPage(wx.Panel):
    def __init__(self, parent, topframe):
        wx.Panel.__init__(self, parent)
        self.topframe = topframe
        boldfont = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)

        self.t1 = wx.StaticText(self, label='Ambiguous residue codes')
        self.t1.SetFont(wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD))

        self.cutters = wx.CheckBox(self, label='Show cutter restriction enzymes')
        self.cutters.SetValue(self.topframe.prefs['include_cutters'])

        mono = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.SetFont(mono)

        kwds = dict(majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rb_b = wx.RadioBox(self, label='B', choices=list('BCGT'),  **kwds)
        self.rb_d = wx.RadioBox(self, label='D', choices=list('DAGT'),  **kwds)
        self.rb_h = wx.RadioBox(self, label='H', choices=list('HACT'),  **kwds)
        self.rb_k = wx.RadioBox(self, label='K', choices=list('KGT'),   **kwds)
        self.rb_m = wx.RadioBox(self, label='M', choices=list('MAC'),   **kwds)
        self.rb_n = wx.RadioBox(self, label='N', choices=list('NACGT'), **kwds)
        self.rb_r = wx.RadioBox(self, label='R', choices=list('RAG'),   **kwds)
        self.rb_s = wx.RadioBox(self, label='S', choices=list('SCG'),   **kwds)
        self.rb_v = wx.RadioBox(self, label='V', choices=list('VACG'),  **kwds)
        self.rb_w = wx.RadioBox(self, label='W', choices=list('WAT'),   **kwds)
        self.rb_y = wx.RadioBox(self, label='Y', choices=list('YCT'),   **kwds)

        self.DoLayout()
        self.SetDefaultValues()
        self.Bind(wx.EVT_RADIOBOX, self.SetValue)
        self.Bind(wx.EVT_CHECKBOX, self.OnCuttersCheck, self.cutters)

    def DoLayout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.cutters, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)        
        vbox.Add(self.t1, 0, wx.ALL, 10)
        vbox.Add(self.rb_b, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_d, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_h, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_k, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_m, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_n, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_r, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_s, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_v, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_w, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        vbox.Add(self.rb_y, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.SetSizer(vbox)        


    def OnCuttersCheck(self, event):
        self.topframe.prefs['include_cutters'] = self.cutters.GetValue()

    def RadioGetChoices(self, rb):
        d = {}
        idx = rb.GetSelection()
        for i in range(rb.GetCount()):
            d[rb.GetString(i)] = True if i == idx else False
        return d
    
    def SetDefaultValues(self):

        def convert(p, rb):
            c = [k for k, v in p.iteritems() if v][0]
            d = dict([(rb.GetString(i), i) for i in range(rb.GetCount())])
            return d[c]

        prefs = self.topframe.prefs['ambiguous_bases']
        self.rb_b.SetSelection(convert(prefs['B'], self.rb_b))
        self.rb_d.SetSelection(convert(prefs['D'], self.rb_d))
        self.rb_h.SetSelection(convert(prefs['H'], self.rb_h))
        self.rb_k.SetSelection(convert(prefs['K'], self.rb_k))
        self.rb_m.SetSelection(convert(prefs['M'], self.rb_m))
        self.rb_n.SetSelection(convert(prefs['N'], self.rb_n))
        self.rb_r.SetSelection(convert(prefs['R'], self.rb_r))
        self.rb_s.SetSelection(convert(prefs['S'], self.rb_s))
        self.rb_v.SetSelection(convert(prefs['V'], self.rb_v))
        self.rb_w.SetSelection(convert(prefs['W'], self.rb_w))
        self.rb_y.SetSelection(convert(prefs['Y'], self.rb_y))

    def SetValue(self, event):
        prefs = self.topframe.prefs['ambiguous_bases']
        prefs['B'] = self.RadioGetChoices(self.rb_b)
        prefs['D'] = self.RadioGetChoices(self.rb_d)
        prefs['H'] = self.RadioGetChoices(self.rb_h)
        prefs['K'] = self.RadioGetChoices(self.rb_k)
        prefs['M'] = self.RadioGetChoices(self.rb_m)
        prefs['N'] = self.RadioGetChoices(self.rb_n)
        prefs['R'] = self.RadioGetChoices(self.rb_r)
        prefs['S'] = self.RadioGetChoices(self.rb_s)
        prefs['V'] = self.RadioGetChoices(self.rb_v)
        prefs['W'] = self.RadioGetChoices(self.rb_w)
        prefs['Y'] = self.RadioGetChoices(self.rb_y)

class LICListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin,
                  listmix.TextEditMixin):

    def __init__(self, parent, topframe):
        self.topframe = topframe
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT
                             | wx.SUNKEN_BORDER
                             | wx.LC_VRULES | wx.LC_HRULES)

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Sequence')
        for name, sequence in self.topframe.prefs['lic_sequences']:
            pos = self.InsertStringItem(sys.maxint, name)
            self.SetStringItem(pos, 1, sequence)
            if name == '' and sequence == '':
                self.SetItemBackgroundColour(pos, wx.Colour(230, 230, 230))
        listmix.TextEditMixin.__init__(self)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEdit)

    def OnEdit(self, event):
        idx = event.m_itemIndex

        white = wx.WHITE
        gray = wx.Colour(230, 230, 230)

        if event.GetColumn() == 0:
            col_0 = event.GetLabel()
            col_1 = self.GetItem(idx, 1).GetText()
        else:
            col_0 = self.GetItem(idx, 0).GetText()
            col_1 = event.GetLabel()

        if col_0 == '' and col_1 == '':
            self.SetItemBackgroundColour(idx, gray)
        else:
            self.SetItemBackgroundColour(idx, white)
        try:
            self.topframe.prefs['lic_sequences'][idx] = [col_0, col_1]
        except IndexError:
            self.topframe.prefs['lic_sequences'].append([col_0, col_1])

    def OnAdd(self, event):
        pos = self.InsertStringItem(sys.maxint, u'')
        self.SetStringItem(pos, 1, u'')
        num_items = self.GetItemCount()
        item = self.GetItem(num_items - 1)
        item.SetBackgroundColour(wx.Colour(230, 230, 230))
        self.SetItem(item)

    def OnRemove(self, event):
        item = self.GetFocusedItem()
        print 'Item =', item
        key = [self.GetItem(item, 0).GetText(), self.GetItem(item, 1).GetText()]
        try:
            idx = self.topframe.prefs['lic_sequences'].index(key)
        except ValueError:
            pass
        else:
            d = self.topframe.prefs['lic_sequences'] 
            self.topframe.prefs['lic_sequences'] = d[:idx] + d[idx+1:]
        self.DeleteItem(item)


class LICPage(wx.Panel):
    def __init__(self, parent, topframe):
        wx.Panel.__init__(self, parent)
        lc = LICListCtrl(self, topframe)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, wx.ID_ADD, 'Add'), 0, wx.LEFT | wx.RIGHT, 10)
        hbox.Add(wx.Button(self, wx.ID_REMOVE, 'Remove'), 0, wx.LEFT | wx.RIGHT, 10)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(lc, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, 10)
        self.Bind(wx.EVT_BUTTON, lc.OnAdd, id=wx.ID_ADD)
        self.Bind(wx.EVT_BUTTON, lc.OnRemove, id=wx.ID_REMOVE)
        self.SetSizer(vbox)


class TagPage(wx.Panel):
    def __init__(self, parent, topframe):
        wx.Panel.__init__(self, parent)


#------------------------------------------------------------------------------

def config_file_name():
    """Return the path to the configuration file.

    """
    if platform.system() == 'Linux':
        return os.path.join(os.getenv('HOME'), '.constructrc')
    elif platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'constructrc')
    else:
        # Simply create a file in the current directory.
        return 'constructrc'


_default_config = dict(
    predictors=dict(HNN=[0, 'PredictorHNN', 1],
                    GORIV=[1, 'PredictorGOR_IV', 1],
                    RONN=[2, 'PredictorRONN', 1],
                    IUPred=[3, 'PredictorIUPred', 1],
                    GlobPlot=[4, 'PredictorGlobPlot', 1]),
    include_cutters=0,
    ambiguous_bases=dict(B=dict(C=1, G=0, T=0),
                         D=dict(A=1, G=0, T=0),
                         H=dict(A=1, C=0, T=0),
                         K=dict(G=1, T=0),
                         M=dict(A=1, C=0),
                         N=dict(A=1, C=0, G=0, T=0),
                         R=dict(A=1, G=0),
                         S=dict(C=1, G=0),
                         V=dict(A=1, C=0, G=0),
                         W=dict(A=1, T=0),
                         Y=dict(C=1, T=0)), 
    lic_sequences=[['Test1', 'cagggacccggt'],
                   ['Test2', 'cgaggagaagcccggtta']])


def load():
    """Load the configuration dict."""
    config = _default_config
    configfile = config_file_name()
    try:
        with open(configfile, 'rb') as handle:
            config = cPickle.load(handle)
    except IOError as err:
        pass
    return config


def save(config):
    """Save the configuration dict."""
    configfile = config_file_name()
    try:
        with open(configfile, 'wb') as handle:
            cPickle.dump(config, handle)
    except IOError:
        pass

get_config_file_name = config_file_name    
get_preferences = load

## def get_preferences():
##     """Return preferences dict."""
##     # But what's the best location to store it?
##     config_file = get_config_file_name()
##     if os.path.isfile(config_file):
##         try:
##             f_in = open(config_file)
##         except IOError:
##             sys.stderr.write('file error\n')
##         else:
##             config = eval(f_in.read())
##             f_in.close()
##             return config
##     else:
##         return _default_config


def test():
    class TestFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent)
            panel = LICPage(self, PreferencesFrame(self))
            self.Centre()
            
    class App(wx.App):
        def OnInit(self):
            frame = TestFrame(None)
            frame.Show(True)
            return True

    app = App(0)
    app.MainLoop()


if __name__ == '__main__':
    test()
