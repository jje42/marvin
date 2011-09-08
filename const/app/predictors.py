# -*- mode: python; -*-
# 
# Copyright (C) Jonathan Ellis 2010
# 
# Author: Jonathan Ellis, D.Phil
# Email:  jonathanjamesellis@gmail.com
# 
# This program is not in the public domain.
# 
# It may not be copied or made available to third parties, without express
# permission from the author, but it may be freely used by anyone who has
# obtained it directly from the author.
# 
# The code may be modified as required, but any modifications must be
# documented so that the person responsible can be identified. If
# someone else breaks this code, the author doesn't want to be blamed
# for code that does not work! You may not distribute any
# modifications, but are encouraged to send them to the author so
# that they may be incorporated into future versions of the code.
# 
# In no event shall the author or any institution in which he is working be
# liable to any party for direct, indirect, special, incidental, or consequential
# damages, including lost profits, arising out of the use of this software and
# its documentation, even if the author has been advised of the possibility of
# such damage.
# 
# The author specifically disclaims any warranties, including, but not 
# limited to, the implied warranties of merchantability and fitness for 
# a particular purpose.  the software provided hereunder is on an "as is" 
# basis, and the author has no obligations to provide maintenance, support, 
# updates, enhancements, or modifications. 
import sys
import re
import urllib
import urllib2
import random

import wx    # Needed by some predictor to draw on canvas

__all__ = ['PredictorHNN',
           'PredictorGOR_IV',
           'PredictorRONN',
           'PredictorIUPred',
           'PredictorGlobPlot']

class Predictor(object):
    """Base class for predictors.

    Sub-classes need to generate their predictions at initialisation time, and
    then call set_prediction().
    """

    Name = ''

    def __init__(self, sequence, name=None):
        """sequence is the protein sequence (str) that this predictor should
        make predictions about."""
        self._sequence = sequence
        self._prediction = []
        self._name = name

    def sequence(self):
        """Return the protein sequence (str)."""
        return self._sequence

    def prediction(self):
        """Return the prediction.  The prediction is stored as a list with one
        element for each amino acid of the protein sequence."""
        if self._prediction:
            return self._prediction
        raise AssertionError('prediction is empty')

    def set_prediction(self, prediction):
        """Set the prediction.  The prediction must be a sequence that has the
        same length as the protein sequence that it predicts."""
        if len(prediction) != len(self._sequence):
            print len(self._sequence)
            print len(prediction), prediction
            raise ValueError('prediction must be same length as sequence')
        self._prediction = prediction

    def set_name(self, name):
        self._name = name

    def name(self):
        return self._name

    def isvalid(self):
        """Returns True if the prediction is valid, that is, the prediction is
        the same length as the protein sequence.  No check that the prediction
        is even remotely valid is made."""
        return len(self._sequence) == len(self._prediction)

    def __len__(self):
        return len(self._prediction)

    def __iter__(self):
        for i in self._prediction:
            yield i

    def __getitem__(self, n):
        return self._prediction[n]

class PredictorDummy(Predictor):

    """Dummy Predictor implementation for testing."""
    Name = 'Dummy'

    def __init__(self, sequence):
        Predictor.__init__(self, sequence)
        self._prediction = [random.choice('HS-') for i in
                            range(len(sequence))]
        self.set_name("Dummy")

class PredictorHNN(Predictor):

    base_url = 'http://npsa-pbil.ibcp.fr'
    regex = re.compile(r'^Prediction result file \(text\).*href=(.+?)>HNN')
    script_url = base_url + '/cgi-bin/secpred_hnn.pl'
    Name = 'HNN'

    def __init__(self, sequence):
        try:
            Predictor.__init__(self, sequence)
            self.set_name('HNN')
            data = urllib.urlencode(dict(title='', notice=sequence,
                                         ali_width=70))
            req = urllib2.Request(PredictorHNN.script_url, data=data)
            handle = urllib2.urlopen(req)
            for line in handle:
                match = PredictorHNN.regex.search(line)
                if match:
                    fname = match.group(1)
                    self._fname = fname
                    self.parse_text_file(PredictorHNN.base_url + fname)
            handle.close()
        except IOError:
            self.set_prediction([' ' for i in range(len(sequence))])
            
    def parse_text_file(self, url):
        p = []
        try:
            handle = urllib2.urlopen(url)
        except urllib2.URLError as err:
            sys.stderr.write('failed to get text file\n')
            sys.exit(1)
        for i, line in enumerate(handle):
            if i < 4:
                continue
            items = line.split()
            if items:
                p.append(items[0])
        handle.close()
        self.set_prediction(p)

    def Draw(self, canvas, indent, width, height, current_y):
        dc = canvas.dc
        x = indent
        y = current_y
        for pred in self:
            dc.SetPen(wx.BLACK_PEN)
            if pred == 'E':
                brush = wx.Brush('yellow', wx.SOLID)
            elif pred == 'H':
                brush = wx.RED_BRUSH
            else:
                brush = wx.WHITE_BRUSH
            dc.SetBrush(brush)
            dc.DrawRectangle(x, y, width, height)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
            #w, h = canvas.GetExtent(pred)
            w, h = 15, 15
            x1 = x + (width / 2.0) - (w / 2.0)
            y1 = y + (height / 2.0) - (h / 2.0)
            dc.DrawText(pred, x1, y1)
            x += width
            
class PredictorGOR_IV(Predictor):

    base_url = 'http://npsa-pbil.ibcp.fr'
    regex = re.compile(r'^Prediction result file \(text\).*href=(.+?)>GOR4')
    Name = 'GOR-IV'
    
    def __init__(self, sequence):
        Predictor.__init__(self, sequence)
        self.set_name('GOR-IV')
        try:
            data = urllib.urlencode(dict(title='', notice=sequence,
                                         ali_width=70))
            uri = PredictorGOR_IV.base_url + '/cgi-bin/secpred_gor4.pl'
            req = urllib2.Request(uri, data=data)
            handle = urllib2.urlopen(req)
            for line in handle.readlines():
                m = PredictorGOR_IV.regex.search(line)
                if m:
                    fname = m.group(1)
                    self._fname = fname
                    uri = PredictorGOR_IV.base_url + fname
                    hnn_handle = urllib2.urlopen(uri)
                    lines = hnn_handle.readlines()
                    self._lines = lines
                    p = []
                    for line2 in lines[4:]:
                        items = line2.split()
                        if items:
                            p.append(items[0])
                    self.set_prediction(p)
                    hnn_handle.close()
            handle.close()
        except:
            self.set_prediction([' ' for i in range(len(sequence))])

    def Draw(self, canvas, indent, width, height, current_y):
        dc = canvas.dc
        x = indent
        y = current_y
        for pred in self:
            dc.SetPen(wx.BLACK_PEN)
            if pred == 'E':
                brush = wx.Brush('yellow', wx.SOLID)
            elif pred == 'H':
                brush = wx.RED_BRUSH
            else:
                brush = wx.WHITE_BRUSH
            dc.SetBrush(brush)
            dc.DrawRectangle(x, y, width, height)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
            #w, h = canvas.GetExtent(pred)
            w, h = 15, 15
            x1 = x + (width / 2.0) - (w / 2.0)
            y1 = y + (height / 2.0) - (h / 2.0)
            dc.DrawText(pred, x1, y1)
            x += width
            


class PredictorRONN(Predictor):

    Name = 'RONN'

    def __init__(self, sequence):
        Predictor.__init__(self, sequence)
        self.set_name('RONN')
        base_url = 'http://www.strubi.ox.ac.uk/RONN'
        try:
            data = urllib.urlencode(dict(sequence=sequence, display_probs='n'))
            req = urllib2.Request(base_url, data=data)
            handle = urllib2.urlopen(req)
            lines = handle.read()
            handle.close()
            m = re.search(r'<p>Disordered regions:</p><p>(.+?)</p>', lines)
            if m:
                d = []
                for start, stop in [i.split(' - ') for i in m.group(1).split(',')]:
                    d.extend(range(int(start), int(stop)+1))
                p = []
                for i in range(1, len(sequence) + 1):
                    if i in d:
                        p.append('d')
                    else:
                        p.append('-')
                self.set_prediction(p)
        except:
            # If we fail for any reason set empty prediction,
            self.set_prediction([' ' for i in range(len(sequence))])

    def Draw(self, canvas, indent, width, height, current_y):
        dc = canvas.dc
        x = indent
        y = current_y
        for pred in self:
            dc.SetPen(wx.BLACK_PEN)
            if pred == 'd':
                brush = wx.Brush('RED', wx.SOLID)
            else:
                brush = wx.WHITE_BRUSH
            dc.SetBrush(brush)
            dc.DrawRectangle(x, y, width, height)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
            #w, h = canvas.GetExtent(pred)
            w, h = 15, 15
            x1 = x + (width / 2.0) - (w / 2.0)
            y1 = y + (height / 2.0) - (h / 2.0)
            dc.DrawText(pred, x1, y1)
            x += width

class PredictorIUPred(Predictor):
    Name = 'IUPred'
    def __init__(self, sequence):
        Predictor.__init__(self, sequence)
        self.set_name('IUPred')
        url = 'http://iupred.enzim.hu/pred.php'
        try:
            # title
            # seq
            # type long/short/glob
            # output data/graph
            # WS 50,100,200,300,400,500,1000,2000
            data = urllib.urlencode(dict(title='', seq=sequence, type='long',
                                         output='data'))
            req = urllib2.Request(url, data=data)
            handle = urllib2.urlopen(req)
            lines = handle.read()
            handle.close()
            s = self.strip_ml_tags(lines)
            s = s.strip().split('\n')
            regex = re.compile(r'\s*(\d+)\s+(\w)(.+)')
            p = []
            for line in s[1:]:
                m = regex.search(line)
                #print int(m.group(1)), m.group(2), float(m.group(3))
                #int(round(0.47439483, 1) * 10) -> 5
                p.append(str(int(round(float(m.group(3)), 1) * 10)))
            self.set_prediction(p)
        except:
            self.set_prediction([' ' for i in range(len(sequence))])

    def strip_ml_tags(self, in_text):
        """Description: Removes all HTML/XML-like tags from the input text.
        Inputs: s --> string of text
        Outputs: text string without the tags

        # doctest unit testing framework

        >>> test_text = \"Keep this Text <remove><me /> KEEP </remove> 123\"
        >>> strip_ml_tags(test_text)
        'Keep this Text  KEEP  123'
        """
        # convert in_text to a mutable object (e.g. list)
        s_list = list(in_text)
        i,j = 0,0

        while i < len(s_list):
                # iterate until a left-angle bracket is found
                if s_list[i] == '<':
                        while s_list[i] != '>':
                                # pop everything from the the left-angle
                                # bracket until the right-angle bracket
                                s_list.pop(i)

                        # pops the right-angle bracket, too
                        s_list.pop(i)
                else:
                        i=i+1

        # convert the list back into text
        join_char=''
        return join_char.join(s_list)

    def Draw(self, canvas, indent, width, height, current_y):
        """IUPred scores range from 0-1, here they have been converted to
        integers (0-10).
        """
        dc = canvas.dc
        x = indent
        y = current_y
        for pred in self:
            dc.SetPen(wx.BLACK_PEN)
            #colour = wx.Colour(255, 0, 0, 255 * (int(pred) / 10.0))

            p = 255 * (int(pred) / 10.0)
            colour = wx.Colour(255, 255 - p, 255 - p)
            brush = wx.Brush(colour, wx.SOLID)
            dc.SetBrush(brush)
            dc.DrawRectangle(x, y, width, height)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
            #w, h = canvas.GetExtent(pred)
            w, h = 15, 15
            x1 = x + (width / 2.0) - (w / 2.0)
            y1 = y + (height / 2.0) - (h / 2.0)
            dc.DrawText(pred, x1, y1)
            x += width    


class PredictorGlobPlot(Predictor):

    Name = 'GlobPlot'

    def __init__(self, sequence):
        Predictor.__init__(self, sequence)
        self.set_name('GlobPlot')
        url = 'http://globplot.embl.de/cgiDict.py'
        try:
            data = urllib.urlencode(dict(key='process',
                                         SP_entry='',
                                         sequence_string=sequence,
                                         params='RL',
                                         peak_frame_dis=5,
                                         join_frame_dis=4,
                                         do_smart='true',
                                         peak_frame_dom=74,
                                         join_frame_dom=15,
                                         do_dydx='true',
                                         do_raw='true',
                                         do_invert='true',
                                         do_casp='true',
                                         plot_title='',
                                         smooth_frame_1=10,
                                         smooth_frame_2=10))
            req = urllib2.Request(url, data=data)
            handle = urllib2.urlopen(req)
            lines = handle.read()
            handle.close()
            m = re.search(r'<h3>Disordered by Russell.*<h3>', lines, re.DOTALL)
            t = re.search(r'&gt.+<br>', m.group(), re.DOTALL)
            d = []
            items = re.findall(r'\d+-\d+', t.group())
            if items:
                for item in items:
                    start, stop = item.split('-')
                    d.extend(range(int(start), int(stop)+1))
                    p = []
                    for i in range(1, len(sequence) + 1):
                        if i in d:
                            p.append('d')
                        else:
                            p.append('-')
                    self.set_prediction(p)
            else:
                raise AssertionError()
        except:
            self.set_prediction([' ' for i in range(len(sequence))])

    def Draw(self, canvas, indent, width, height, current_y):
        dc = canvas.dc
        x = indent
        y = current_y
        for pred in self:
            dc.SetPen(wx.BLACK_PEN)
            if pred == 'd':
                brush = wx.Brush('RED', wx.SOLID)
            else:
                brush = wx.WHITE_BRUSH
            dc.SetBrush(brush)
            dc.DrawRectangle(x, y, width, height)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
            #w, h = canvas.GetExtent(pred)
            w, h = 15, 15
            x1 = x + (width / 2.0) - (w / 2.0)
            y1 = y + (height / 2.0) - (h / 2.0)
            dc.DrawText(pred, x1, y1)
            x += width
