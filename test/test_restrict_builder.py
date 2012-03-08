#! /usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
"""Test RestrictionEnzymeBuilder.

Note this script does not attempt in silico cloning as the primers produced
will not work.  They will not produce the correct reading frame without the
addition of two bases after the forward restriction site.

"""
from __future__ import print_function, division

import os, sys
sys.path.insert(0, os.pardir)

import unittest2 as unittest

from Bio import SeqIO
from Bio import Restriction

import const.codon as codon
import const.restriction as restriction
from const.builder import RestrictionEnzymeBuilder


class RestrictionEnzymeBuilderIntegrationTestCase(unittest.TestCase):

    def test_restrictionbuilder(self):
        with open('gapdh_dna.fsa') as handle:
            s = SeqIO.read(handle, 'fasta')

        builder = RestrictionEnzymeBuilder()
        builder.nucleotide_seq = s.seq
        builder.add_start_position(3)
        builder.add_start_position(15)
        builder.add_stop_position(101)
        builder.add_stop_position(78)

        builder.forward_enzyme = Restriction.BamHI
        builder.reverse_enzyme = Restriction.Bpu1102I

        builder.forward_overhang = 'AAAAAA'
        builder.reverse_overhang = 'TTTTTT'
        builder.insert_start_codon = False
        builder.insert_stop_codon = True

        builder.target_temperature = 60
        builder.target_primer_length = None

        constructs = builder.design()

        ## for construct in constructs:
        ##     print(construct.forward_primer)
        ##     print(construct.reverse_primer)
        ##     print(construct.protein_seq)
        ##     print(construct.start_position, construct.stop_position)
