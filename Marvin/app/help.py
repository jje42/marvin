import wx
import wx.richtext as richtext
import wx.html

help_text = '''
<h1>Marvin</h1>

<h2>Using Marvin</h2>
<p>
First open a DNA sequence.  Should be cDNA as the program can't cope
with introns.
</p>
<p>
Select the mode from the "mode" menu.
</p>
<p>
Move to the "Protein" tab and click "Translate" button.  You should see
a translation of your DNA sequence appear in the box below.
</p>
<p>
Optionally, click "Run Predictors" to submit your (protein) sequence to
various web servers.  This may take some time depending on how long the
servers take to respond, but the result should appear below the protein
sequence.
</p>
<p>
Select construct start positions by left-clicking with the mouse on the
protein residue where you would like a construct to start.  It should
turn green to indicate a start position.  If you change your mind,
left-clicking on a residue again will deselect it as a starting residue.
</p>
<p>
Select end residues for your constructs by right-clicking with the
mouse.  This time the residue should turn red to indicate an end
position.  Again, you can deselect an end residue by right-clicking
again.
</p>
<p>
Add any forward or reverse overhangs by simply entering the DNA sequence
into the boxes provided.
</p>
<p>
If you decide that all of your selected positions are wrong, you can
simply remove them all be clicking the "Clear Positions" button.
</p>
<p>
Clicking the "Clear" button will remove *everything* from the textarea
at the bottom of the Protein tab.
</p>

<h4>Restriction Enzymes</h4>
<p>
You can select forward and reverse restiction enzyme sites to insert
into your primers by clicking the appropriate select box.  A selection
box should appear were you can scroll through restriction enzymes to
select the one you want.  If you type the first characters of a
restriction enzyme into the search box the list will be filtered to
enzymes that start with those characters.  This helps prevent you from
having to scroll through a large number of enzymes.  Note that, by
default, only restriction enzyme that do NOT cut your protein are
available in the selection box.
</p>

<h4>LIC Cloning</h4>
<p>
If you are performing LIC cloning, you can select forward and reverse
overhangs from the drop down boxes.
</p>
<p>
The first time you start Marvin, there won't be any LIC overhang
sequences available.  You must add these yourself by selecting the Edit
-> Preferences menu.  When the Preferences dialog box appears go to the
LIC tab.  Click on the "Add" button to add new LIC overhangs.  As well
as entering the overhang sequence, you can also enter a more human
readable name to help you identfy each overhang (for example, labelling
them as forward and reverse overhangs).
</p>
<p>
Once you have added LIC sequences, Marvin will remember them so you will
only have to do this once.
</p>

<h3>Designing Primers</h3>
<p>
Once you're happy with your selection of start and end positions for
your constructs, you can move to the "Primers" tab.
</p>
<p>
select melting temperature or number of bases.
</p>
<p>
Click "Design" button
</p>
'''


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

##        self.text = richtext.RichTextCtrl(self)
##
##        self.text.BeginAlignment(richtext.TEXT_ALIGNMENT_CENTRE)
##        self.text.BeginBold()
##        self.text.BeginFontSize(14)
##        self.text.WriteText("Sorry, you're on your own.\n")
##        self.text.EndFontSize()
##        self.text.EndBold()
##        self.text.EndAlignment()
##
##        self.text.Newline()
##        self.text.WriteText("There's no help yet, try comming back "
##                            "later.\n")
##
##        vbox = wx.BoxSizer(wx.VERTICAL)
##        vbox.Add(self.text, 1, wx.EXPAND | wx.ALL, 10)

        hwin = wx.html.HtmlWindow(self)
        hwin.SetPage(help_text)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hwin, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)

    def OnClose(self, event):
        self.Destroy()    
