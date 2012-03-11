import os
import sys
import textwrap
from StringIO import StringIO
import wx

import Marvin
import Marvin.restriction
import Marvin.app.predictors
import Marvin.app.preferences as preferences
from Marvin.app.emboss import EmbossFrame



class ProteinPage(wx.Panel):

    def __init__(self, parent, topframe, mode='Restrict'):
        wx.Panel.__init__(self, parent)

        # This is a stub until I find a better way of doing it.
        have_emboss = False

        self.topframe = topframe
        #self._mode = mode
        self._mode = ''
        self._predictions = []

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(wx.Button(self, 20, 'Translate'), 0, wx.ALL, 5)
        self.hbox.Add(wx.Button(self, 23, 'Run Predictors'), 0, wx.ALL, 5)
        self.hbox.Add(wx.Button(self, wx.ID_SAVE, 'Save'), 0, wx.ALL, 5)
        self.hbox.Add(wx.Button(self, wx.ID_CLEAR, 'Clear'), 0, wx.ALL, 5)
        self.hbox.Add(wx.Button(self, 22, 'Clear Positions'), 0, wx.ALL, 5)
        if have_emboss:
            self.hbox.Add(wx.Button(self, 25, 'EMBOSS'), 0, wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnTranslate, id=20)
        self.Bind(wx.EVT_BUTTON, self.OnRun,       id=23)
        self.Bind(wx.EVT_BUTTON, self.OnSave,      id=wx.ID_SAVE)
        if have_emboss:
            self.Bind(wx.EVT_BUTTON, self.OnEmboss,    id=25)

        # Forward
        self.t1          = wx.StaticText(self, -1, 'Forward Overhang:')
        self.fw_overhang = wx.TextCtrl(self, 21, '', style=wx.TE_LEFT)
        self.fw_overhang.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.t2          = wx.StaticText(self, -1, 'Restriction Site:')
        self.fw_rs_entry = wx.TextCtrl(self)
        self.fw_rs_btn = wx.Button(self, label='Select')
        #self.fwrs        = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT)
        self.fw_lic = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY | wx.CB_SORT)
        self.fw_start    = wx.CheckBox(self, -1, 'Add start codon', style=wx.ALIGN_RIGHT)

        # Reverse
        self.t4          = wx.StaticText(self, -1, 'Reverse Overhang:')
        self.rv_overhang = wx.TextCtrl(self, 24, '', style=wx.TE_LEFT)
        self.rv_overhang.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.t5          = wx.StaticText(self, -1, 'Restriction Site:')
        #self.rvrs        = wx.ComboBox(self, 25, style=wx.CB_READONLY | wx.CB_SORT)
        self.rv_rs_entry = wx.TextCtrl(self)
        self.rv_rs_btn = wx.Button(self, label='Select')
        self.rv_lic = wx.ComboBox(self, 25, style=wx.CB_READONLY | wx.CB_SORT)

        self.rv_stop     = wx.CheckBox(self, -1, 'Add stop codon', style=wx.ALIGN_RIGHT)

        self.win = ProteinCanvas(self, topframe)

        fwbox = wx.BoxSizer(wx.HORIZONTAL)
        fwbox.Add(self.t1,          0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        fwbox.Add(self.fw_overhang, 0, wx.ALL, 5)
        fwbox.Add(self.t2,          0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        #fwbox.Add(self.fwrs,        0, wx.ALL, 5)
        fwbox.Add(self.fw_rs_entry, 0, wx.ALL, 5)
        fwbox.Add(self.fw_rs_btn, 0, wx.ALL, 5)
        fwbox.Add(wx.StaticText(self, label='LIC sequence:'), 0, wx.ALIGN_CENTRE_VERTICAL)
        fwbox.Add(self.fw_lic, 0, wx.ALL, 5)
        fwbox.Add(self.fw_start,    0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

        rvbox = wx.BoxSizer(wx.HORIZONTAL)
        rvbox.Add(self.t4,          0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        rvbox.Add(self.rv_overhang, 0, wx.ALL, 5)
        rvbox.Add(self.t5,          0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        #rvbox.Add(self.rvrs,        0, wx.ALL, 5)
        rvbox.Add(self.rv_rs_entry, 0, wx.ALL, 5)
        rvbox.Add(self.rv_rs_btn, 0, wx.ALL, 5)
        rvbox.Add(wx.StaticText(self, label='LIC sequence:'), 0, wx.ALIGN_CENTRE_VERTICAL)
        rvbox.Add(self.rv_lic, 0, wx.ALL, 5)        
        rvbox.Add(self.rv_stop,     0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)


        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 5))
        vbox.Add(self.hbox, 0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(fwbox, 0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add(rvbox, 0, wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        vbox.Add(self.win, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON,   self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_BUTTON,   self.win.OnClearPositions, id=22)
        self.Bind(wx.EVT_COMBOBOX, self.OnComboChange)
        self.Bind(wx.EVT_TEXT,     self.OnTextChange)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.Bind(wx.EVT_BUTTON, self.OnSelectEnzyme, self.fw_rs_btn)
        self.Bind(wx.EVT_BUTTON, self.OnSelectEnzyme, self.rv_rs_btn)

        self.set_mode(mode)

    def OnClear(self, event):
        self._predictions = []
        self.win.ClearCanvas(event)

    def OnSave(self, event):
        #wild = 'Text files (*.txt)|*.txt'
        dia = wx.FileDialog(self, message='Save file as...',
                            defaultDir=os.getcwd(),
                            defaultFile='',
                            style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if dia.ShowModal() == wx.ID_OK:
            path = dia.GetPath()
            try:
                f_out = open(path, 'w')
            except IOError:
                pass
            else:
                kwds = dict(width=50,
                            break_on_hyphens=False,
                            initial_indent='',
                            subsequent_indent='')
                protseq = self.topframe.builder.protein_seq.tostring()
                ps = [textwrap.wrap(protseq, **kwds)]
                names = ['Protein']
                for predictor in self._predictions:
                    name = predictor.name()
                    p = ''.join(predictor.prediction())
                    ps.append(textwrap.wrap(p, **kwds))
                    names.append(name)
                N = max(len(n) for n in names)
                for x in zip(*ps):
                    for i, y in enumerate(x):
                        f_out.write('{0:{2}}{1}\n'.format(names[i], y, N))
                    f_out.write('\n')
                f_out.close()
        dia.Destroy()

    def OnTranslate(self, event):
        nucseq = self.topframe.nucPage.text.GetValue()
        if nucseq:
            self.topframe.builder.nucleotide_seq = nucseq
            protseq = self.topframe.builder.protein_seq
            if self.mode == 'Restrict':
                pass
                #self.SetRestrictionSites()
            else:
                self.SetLICSequences()
            self.win.DrawProteinSequence(protseq)
        else:
            self.topframe.statusbar.Warn(
                'You must enter a nucleotide sequence!')

    def OnRun(self, event):
        """Run predictions.
        """
        protseq = self.topframe.builder.protein_seq
        prefs = preferences.get_preferences()
        # NB, predictors is the module name, DON'T overwrite it.
        d = [(o, (p, c, u)) for p, (o, c, u) in prefs['predictors'].iteritems()]
        d.sort()
        ordered_predictors = [(p, (c, u)) for (o, (p, c, u)) in d]
        for predictor, (classname, use) in ordered_predictors:
            if use:
                self.topframe.SetStatusText('Running {0}'.format(predictor))
                #C = getattr(__import__(__name__), classname)
                C = getattr(Marvin.app.predictors, classname)
                p = C(protseq)
                self._predictions.append(p)
                self.win.DrawPrediction(p)
        self.topframe.SetStatusText('')


    def get_mode(self):
        return self._mode

    def set_mode(self, mode):
        if mode == 'Restrict':
            self._mode = mode
            self.fw_lic.Enable(False)
            #self.fw_rs_entry.Enable(True)
            self.fw_rs_entry.Enable(False)
            self.fw_rs_btn.Enable(True)
            self.rv_lic.Enable(False)
            #self.rv_rs_entry.Enable(True)
            self.rv_rs_entry.Enable(False)
            self.rv_rs_btn.Enable(True)
        if mode == 'LIC':
            self._mode = mode
            self.fw_lic.Enable(True)
            self.fw_rs_entry.Enable(False)
            self.fw_rs_btn.Enable(False)
            self.rv_lic.Enable(True)
            self.rv_rs_entry.Enable(False)
            self.rv_rs_btn.Enable(False)
            self.SetLICSequences()
        if mode == 'Mutate':
            self._mode = mode
            self.fw_lic.Enable(False)
            self.fw_rs_entry.Enable(False)
            self.fw_rs_btn.Enable(False)
            self.rv_lic.Enable(False)
            self.rv_rs_entry.Enable(False)
            self.rv_rs_btn.Enable(False)

    mode = property(get_mode, set_mode, None, None)

    def SetLICSequences(self):
        prefs = preferences.get_preferences()
        self.fw_lic.Clear()
        self.rv_lic.Clear()
        self.fw_lic.Append('')
        self.rv_lic.Append('')
        for name, sequence in prefs['lic_sequences']:
            # Ignore anything that doesn't have a sequence.
            if sequence:
                if name:
                    self.fw_lic.Append(name)
                    self.rv_lic.Append(name)
                else:
                    self.fw_lic.Append(sequence)
                    self.rv_lic.Append(sequence)

    def OnSelectEnzyme(self, event):
        # There must be a sequence before calling this dialog
        sequence = self.topframe.builder.nucleotide_seq
        if sequence:
            dia = RestrictionDialog(self, sequence)
            dia.ShowModal()
            Id = event.GetEventObject().GetId()
            if Id == self.fw_rs_btn.GetId():
                if dia.enzyme is not None:
                    self.fw_rs_entry.Clear()
                    self.fw_rs_entry.AppendText(str(dia.enzyme))
                    #s = Marvin.restriction.sequence(dia.enzyme)
                    #self.topframe.builder.forward_cloning_seq = str(s)
                    self.topframe.builder.forward_enzyme = dia.enzyme
            elif Id == self.rv_rs_btn.GetId():
                if dia.enzyme is not None:
                    self.rv_rs_entry.Clear()
                    self.rv_rs_entry.AppendText(str(dia.enzyme))
                    # s = Marvin.restriction.sequence(dia.enzyme)
                    # s.reverse_complement()
                    # self.topframe.builder.reverse_cloning_seq = str(s)
                    self.topframe.builder.reverse_enzyme = dia.enzyme
            else:
                pass
        else:
            dia = wx.MessageDialog(self, 'You need to enter a sequence to work on',
                                   'foo', wx.OK | wx.ICON_ERROR)
            dia.ShowModal()
            dia.Destroy()


    def OnComboChange(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()

        if self.topframe.builder.mode == 'LIC':
            prefs = preferences.get_preferences()
            if obj.GetId() == self.fw_lic.GetId():
                for i, j in prefs['lic_sequences']:
                    if i == value:
                        #self.topframe.builder.forward_cloning_seq = j
                        self.topframe.builder.forward_lic_seq = j
            elif obj.GetId() == self.rv_lic.GetId():
                for i, j in prefs['lic_sequences']:
                    if i == value:
                        #self.topframe.builder.reverse_cloning_seq = j
                        self.topframe.builder.reverse_lic_seq = j
            else:
                pass
            

    def OnTextChange(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        oid = obj.GetId()
        if oid == self.fw_overhang.GetId() or oid == self.rv_overhang.GetId():
            if set(value.lower()).issubset('atgc'):
                obj.SetBackgroundColour('WHITE')
            else:
                obj.SetBackgroundColour('RED')
            if obj.GetId() == self.fw_overhang.GetId():
                self.topframe.builder.forward_overhang = value
            elif obj.GetId() == self.rv_overhang.GetId():
                self.topframe.builder.reverse_overhang = value
            else:
                pass

    def OnCheck(self, event):
        """Handler for checkboxes."""
        obj = event.GetEventObject()
        if obj.GetId() == self.fw_start.GetId():
            self.topframe.builder.insert_start_codon = obj.GetValue()
        elif obj.GetId() == self.rv_stop.GetId():
            self.topframe.builder.insert_stop_codon = obj.GetValue()

    def OnEmboss(self, event):
        e = EmbossFrame(self, self.topframe)
        e.Show(True)


class CanvasObject:
    def __init__(self, x, y, w, h, residue, number, state):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.residue = residue
        self.number = number
        self.state = state
        self.original_residue = residue # for site-mut

    def get_brush(self):
        if self.state == 'start':
            return wx.Brush('green', wx.SOLID)
        elif self.state == 'stop':
            return wx.Brush('red', wx.SOLID)
        elif self.state == 'mutate':
            return wx.Brush('YELLOW', wx.SOLID)
        else:
            return wx.Brush('white', wx.SOLID)

    brush = property(get_brush, None, None, None)


class ProteinCanvas(wx.ScrolledWindow):

    def __init__(self, parent, topframe):
        wx.ScrolledWindow.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.topframe = topframe
        #self.SetBackgroundColour('WHITE')
        self.SetVirtualSize((5000, 5000))
        self.SetScrollRate(20, 20)
        self.dc = wx.PseudoDC()

        self.objids = {}

        self.width = 25
        self.height = 25
        self.indent = 100
        self.current_prediction_line = 150

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

    def ConvertEventCoords(self, event):
        vx, vy = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        return (event.GetX() + (vx * dx), event.GetY() + (vy * dy))

    def OnMouse(self, event):
        hitradius = 1
        dc = self.dc
        dc.BeginDrawing()

        builder = self.topframe.builder
        mode = builder.mode

        if mode == 'Restrict' or mode == 'LIC':
            if event.LeftDown():
                x, y = self.ConvertEventCoords(event)
                L = dc.FindObjects(x, y, hitradius)
                if L:
                    id = L[0]
                    obj = self.objids[id]
                    dc.ClearId(id)
                    dc.SetId(id)
                    if obj.state == 'start':
                        obj.state = None
                        builder.remove_start_position(obj.number)
                    else:
                        obj.state = 'start'
                        builder.add_start_position(obj.number)
                        builder.remove_stop_position(obj.number)
                    r = dc.GetIdBounds(id)
                    x, y, w, h = r.Get()
                    self.DrawSquare(dc, obj)
                    self.Refresh(True)

            if event.RightDown():
                x, y = self.ConvertEventCoords(event)
                L = dc.FindObjects(x, y, hitradius)
                if L:
                    id = L[0]
                    obj = self.objids[id]
                    dc.ClearId(id)
                    dc.SetId(id)
                    if obj.state == 'stop':
                        obj.state = None
                        builder.remove_stop_position(obj.number)
                    else:
                        obj.state = 'stop'
                        builder.add_stop_position(obj.number)
                        builder.remove_start_position(obj.number)
                    r = dc.GetIdBounds(id)
                    x, y, w, h = r.Get()
                    self.DrawSquare(dc, obj)
                    self.Refresh(True)

        if mode == 'Mutate':
            #if event.MiddleDown():
            if event.LeftDown():
                x, y = self.ConvertEventCoords(event)
                L = dc.FindObjects(x, y, hitradius)
                if L:
                    id = L[0]
                    obj = self.objids[id]
                    dc.ClearId(id)
                    dc.SetId(id)
                    if obj.state == 'mutate':
                        builder.remove_site(obj.number, obj.original_residue, obj.residue)
                        obj.state = None
                        obj.residue = obj.original_residue
                    else:
                        obj.state = 'mutate'
                        mutate_dialog = MutateResidue(self)
                        mutate_dialog.ShowModal()
                        if mutate_dialog.residue:
                            obj.residue = mutate_dialog.residue
                        builder.add_site(obj.number, obj.original_residue, obj.residue)
                    r = dc.GetIdBounds(id)
                    x, y, w, h = r.Get()
                    self.DrawSquare(dc, obj)
                    self.Refresh(True)

        dc.EndDrawing()

    def ClearCanvas(self, event):
        if isinstance(self.topframe.builder, Marvin.ConstructBuilder):
            self.topframe.builder.remove_start_position()
            self.topframe.builder.remove_stop_position()
        else:
            self.topframe.builder.remove_site()

        self.dc.RemoveAll()
        self.Refresh(True)

    def OnClearPositions(self, event):
        dc = self.dc
        dc.BeginDrawing()

        for id, obj in self.objids.iteritems():
            dc.ClearId(id)
            dc.SetId(id)
            obj.state = None
            obj.residue = obj.original_residue
            r = dc.GetIdBounds(id)
            x, y, w, h = r.Get()
            self.DrawSquare(dc, obj)
            self.Refresh(True)

        dc.EndDrawing()
        ## if self.topframe.builder.mode in ['Restrict', 'LIC']:
        ##     self.topframe.builder = Marvin.ConstructBuilder()
        ## else:
        ##     self.topframe.builder = Marvin.SiteBuilder()
        self.topframe.builder.clear_positions()


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.PrepareDC(dc)
        bg = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(bg)
        dc.Clear()
        xv, yv = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        x, y = (xv * dx, yv * dy)
        rgn = self.GetUpdateRegion()
        rgn.Offset(x, y)
        r = rgn.GetBox()
        self.dc.DrawToDCClipped(dc, r)

    def GetExtent(self, text):
        tmpdc = wx.PaintDC(self)
        self.PrepareDC(tmpdc)
        return tmpdc.GetTextExtent(text)

    def DrawSquare(self, dc, obj):
        """Draw individual square (residue).

        It would make more sense for this to be a method of CanvasObject, but
        it calls GetExtent() that calls PrepareDC() which is a method of the
        base class so this isn't possible.

        """
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(obj.brush)
        dc.DrawRectangle(obj.x, obj.y, obj.w, obj.h)
        dc.SetPen(wx.BLACK_PEN)
        dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        #width, height = self.GetExtent(obj.residue)
        width, height = 15, 15
        x1 = obj.x + (obj.w / 2.0) - (width / 2.0)
        y1 = obj.y + (obj.h / 2.0) - (height / 2.0)
        dc.DrawText(obj.residue, x1, y1)

    def DrawProteinSequence(self, protseq):
        self.objids = {}
        dc = self.dc
        dc.BeginDrawing()
        x, y, w, h = self.indent, 80, self.width, self.height
        dc.SetPen(wx.BLACK_PEN)
        dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        dc.DrawText('Protein', 10, y+5)

        for i, residue in enumerate(protseq):
            id = wx.NewId()
            dc.SetId(id)

            obj = CanvasObject(x,y,w,h,residue,i+1,None)
            self.DrawSquare(dc, obj)
            r = wx.Rect(x, y, w, h)
            dc.SetIdBounds(id, r)
            self.objids[id] = obj
            x += w

        dc.SetId(wx.NewId())
        x, y = self.indent, 80
        for i in range(len(protseq)):
            if i == 0 or (i+1) % 10 == 0:
                _x = x + (w * i)
                dc.DrawLine(_x, y, _x, y - 40)
                dc.DrawLine(_x, y - 40, _x + 10, y - 40)
                dc.DrawText(str(i+1), _x + 15, y - 50)
        dc.EndDrawing()
        self.Refresh(True)
        self.SetVirtualSize((len(protseq) * w + 500, 5000))

    def DrawPrediction(self, predictor):
        x = self.indent
        width, height = self.width, self.height
        dc = self.dc
        dc.BeginDrawing()
        y = self.current_prediction_line
        id = wx.NewId()
        dc.SetId(id)
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.Brush('WHITE', wx.SOLID))
        dc.DrawText(predictor.name(), 10, y+5)
        if hasattr(predictor, 'Draw'):
            f = getattr(predictor, 'Draw')
            f(self, x, width, height, y)
        else:
            for pred in predictor.prediction():
                self.DrawSquare(dc, x, y, width, height, pred, wx.Brush('white', wx.SOLID))
                x += width
        dc.EndDrawing()
        self.Refresh(True)
        self.current_prediction_line += (height + 20)



class MutateResidue(wx.Dialog):
    three_to_one = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D',
                    'Cys': 'C', 'Glu': 'E', 'Gln': 'Q', 'Gly': 'G',
                    'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K',
                    'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S',
                    'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V'}

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Mutate Residue')
        self.residue = None
        gbox = wx.GridSizer(5, 5, 2, 2)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Ala'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Cys'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Asp'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Glu'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Phe'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Gly'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'His'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Ile'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Lys'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Leu'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Met'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Asn'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Pro'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Gln'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Arg'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Ser'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Thr'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Val'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Trp'), 0)
        gbox.Add(wx.Button(self, wx.ID_ANY, 'Tyr'), 0)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, wx.ID_ANY, label='Select residue to mutate to'),
                 0, wx.ALL, 20)
        vbox.Add(gbox, 0, wx.LEFT | wx.RIGHT, 20)
        vbox.Add(wx.Button(self, wx.ID_CANCEL, 'Cancel'), 0, wx.ALIGN_CENTRE | wx.ALL, 20)
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Bind(wx.EVT_BUTTON, self.OnClick)

    def OnClick(self, event):
        label = event.EventObject.GetLabelText()
        try:
            self.residue = MutateResidue.three_to_one[label]
        except KeyError:
            self.residue = None
        self.Destroy()


from Bio import Restriction

class RestrictionDialog(wx.Dialog):
    def __init__(self, parent, nucleotide_seq):
        wx.Dialog.__init__(self, parent, title='Select a restriction enzyme')
        self.sequence = nucleotide_seq
        self.enzyme = ''

        enzymes = Marvin.restriction.do_not_cut(nucleotide_seq)
        self.noncutters = [str(x) for x in enzymes]

        self.search = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.lst = wx.ListBox(self, style=wx.LB_SINGLE)
        self.lst.InsertItems(sorted(self.noncutters), 0)
        self.select = wx.Button(self, wx.ID_OK, label='OK')
        self.cancel = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        #self.clear = wx.Button(self, wx.ID_CLEAR, label='Clear')
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(self.cancel, 0, wx.ALIGN_RIGHT)
        #buttons.Add(self.clear, 0, wx.ALIGN_RIGHT)
        buttons.Add(self.select, 0, wx.ALIGN_RIGHT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.lst, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(buttons, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Centre()
        self.Bind(wx.EVT_TEXT, self.DoOnSearch, self.search)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, self.select)
        #self.Bind(wx.EVT_BUTTON, self.OnClear, self.clear)

    def DoOnSearch(self, event):
        term = self.search.GetValue()
        new_list = []
        for item in self.noncutters:
            if item.lower().startswith(term):
                new_list.append(item)
        self.lst.Clear()
        self.lst.InsertItems(sorted(new_list), 0)

    def OnSelect(self, event):
        index = self.lst.GetSelection()
        value = self.lst.GetString(index)
        #self.enzyme = value
        self.enzyme = getattr(Restriction, value)
        self.Destroy()

    # def OnClear(self, event):
    #     self.enzyme = ''
    #     self.Destroy()
        
    def OnCancel(self, event):
        self.enzyme = None
        self.Destroy()
        

