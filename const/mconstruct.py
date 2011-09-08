# -*- mode: python; coding: utf-8; -*-
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
