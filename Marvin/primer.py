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
""""""
from __future__ import print_function, division

from Bio.Seq import Seq


class Primer(object):

    """Individual primer."""

    def __init__(self, position, overhang, cloning_seq, start_stop,
                 primer, reverse=False):
        """Primer initialisation."""
        self.position       = position
        self.overhang       = overhang
        self.cloning_seq = cloning_seq
        self.start_stop     = start_stop
        self.primer         = primer
        self.reverse        = reverse
        self.tag            = ''

    seq = property(lambda s: Seq(str(s)), None, None, '')

    def write(self, handle):
        """Write primer to handle."""
        pass

    def __str__(self):
         return ''.join([self.overhang, self.cloning_seq,
                         self.start_stop, self.primer]).lower()

    def __repr__(self):
        return repr([self.position, self.overhang, self.cloning_seq,
                     self.start_stop, self.primer, self.reverse])


class PrimerDesigner(object):

    """Create primer for at a specific start position.
    """

    def __init__(self, sequence, start, mode, **kwds):
        """
        Arguments:
           sequence: DNA sequence (str) to build primer for.
           start: the start position of the primer.
           mode: 'Forward' | 'Reverse' | 'Site'
        """
        self.sequence = sequence
        self.start = start

        if mode not in ['Forward', 'Reverse', 'Site']:
            raise ValueError('invalid mode: {0}'.format(mode))
        self.mode = mode

        try:
            self.target_temperature = int(kwds['temperature'])
        except (KeyError, ValueError):
            self.target_temperature = 65

        try:
            self.primer_length = int(kwds['primer_length'])
        except (KeyError, ValueError):
            self.primer_length = None

        if mode == 'Forward':
            self.primer = self._forward_primer(sequence, start)
        elif mode == 'Reverse':
            self.primer = self._reverse_primer(sequence, start)
        else:
            self.primer = self._site_primer(sequence, start)

    def _Tm(self, sequence):
        """Return melting temperature of sequence."""
        if len(sequence) > 0:
            GCnr = len([i for i in sequence if i in 'GgCc'])
            return 64.9 + ((41 * (GCnr-16.4)) / float(len(sequence)))
        return 0

    def _stop(self, sequence):
        """Determine when a primer is accepted.

        There are two conditions that may be used to determine the
        length of a primer: melting temperature or number of bases.  The
        default is to use a melting temperature of 65C.  To override
        this one of the keywords 'temperature' or 'primer_length' must
        be supplied to the __init__() function.  If both are given
        'primer_length' will be used.
        """
        if self.primer_length:
            if len(sequence) == self.primer_length:
                return True
            return False
        if self._Tm(sequence) >= self.target_temperature:
            return True
        return False

    def _forward_primer(self, sequence, n):
        x = self._prot_to_nuc_residue(n)
        s = sequence[x:]
        return self._designprimer(s, 0)

    def _reverse_primer(self, sequence, n):
        x = self._prot_to_nuc_residue_reverse(n)
        s = sequence[:x]
        return self._designprimer(s.reverse_complement(), 0)

    def _designprimer(self, sequence, start):
        s = sequence[start:]
        i = 1  # initial size of primer
        p = s[:i]
        #while self._Tm(p) < target:
        while not self._stop(p):
            i += 1
            if i == len(s) + 1:
                raise ValueError('failed to design primer')
            p = s[:i]
        return p

    def _site_primer(self, sequence, start):
        start = self._prot_to_nuc_residue(start)
        primer = sequence[start]
        x = 0
        while not self._stop(primer):
            x += 1
            k = max(start - x, 0)
            m = min(start + x, len(sequence))
            primer = sequence[k:m]
            if (start - x) < 0 and (start + x) > len(sequence):
                raise ValueError('failed to design primer')
        return primer

    def _prot_to_nuc_residue(self, n):
        """Convert a protein residue number to a nucleotide residue
        number."""
        # Should be ((n - 1) * 3) + 1, but Python indexes from 0
        return (n - 1) * 3
        
    def _prot_to_nuc_residue_reverse(self, n):
        """Convert a protein residue number to a nucleotide residue
        number for a reverse primer."""
        return ((n - 1) * 3) + 3

        
    def __str__(self):
        #return self.primer.tostring().upper()
        return self.primer.tostring()

        
    def __len__(self):
        return len(self.primer)

        
    def __iter__(self):
        for i in self.primer.tostring().upper():
            yield i

