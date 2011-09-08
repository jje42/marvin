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
"""Restriction enzyme functions.
"""
from __future__ import print_function, division

from Bio.Seq import Seq
from Bio import Restriction


def do_not_cut(sequence):
    """Return a list of enzymes that do not cut sequence."""
    if isinstance(sequence, str):
        sequence = Seq(sequence)
    a = Restriction.Analysis(Restriction.CommOnly, sequence)
    noncutters = a.do_not_cut(1, -1).keys()
    return noncutters


def common_enzymes():
    """Return a list of common restriction enzymes."""
    return Restriction.CommOnly


def sequence(enzyme, ambiguous_bases=None):
    """Return the sequence that enzyme recognises.

    REBASE Recognition sequences representations use the standard
    abbreviations (Eur. J. Biochem. 150: 1-5, 1985) to represent
    ambiguity::

       R = G or A
       Y = C or T
       M = A or C
       K = G or T
       S = G or C
       W = A or T
       B = not A (C or G or T)
       D = not C (A or G or T)
       H = not G (A or C or T)
       V = not T (A or C or G)
       N = A or C or G or T
                        
    Parameters:
       ambiguous_bases: dict that deals with the conversion of ambiguous
       nucleotide bases.
    """
    if ambiguous_bases is None:
        ambiguous_bases = dict(A='A', T='T', C='C', G='G',
                               R='G', Y='C', M='A', K='G',
                               S='G', W='A', B='C', D='A',
                               H='A', V='A', N='A')
    e = getattr(Restriction, enzyme)
    return Seq(''.join(ambiguous_bases[x] for x in e.site))


