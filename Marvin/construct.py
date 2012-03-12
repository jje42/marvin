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


class Construct(object):

    """A protein construct."""

    def __init__(self, forward_primer, reverse_primer, protein_seq):
        self.forward_primer = forward_primer
        self.reverse_primer = reverse_primer
        self.nucleotide_seq = None
        #self.protein_seq    = self.nucleotide_seq.translate()
        self.protein_seq = protein_seq
        self.start_position = self.forward_primer.position
        self.stop_position  = self.reverse_primer.position

    def _is_valid(self):
        if self.forward_primer is None:
            return False
        if self.reverse_primer is None:
            return False
        if self.nucleotide_seq is None:
            return False
        return True

    valid = property(_is_valid, None, None, '')

    def __len__(self):
        """Should the length be protein or nucleotide?"""
        pass
