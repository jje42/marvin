#! /usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
"""Test LICBuilder.

"""
from __future__ import print_function, division

import os, sys
sys.path.insert(0, os.pardir)

import unittest2 as unittest

import const.codon as codon
import const.restriction as restriction
from const.builder import LICBuilder

from Bio import SeqIO


class LICBuilderIntegrationTestCase(unittest.TestCase):

    def test_licbuilder(self):
        with open('gapdh_dna.fsa') as handle:
            s = SeqIO.read(handle, 'fasta')

        builder = LICBuilder()
        builder.nucleotide_seq = s.seq
        builder.add_start_position(3)
        builder.add_start_position(15)
        builder.add_stop_position(101)
        builder.add_stop_position(78)

        builder.forward_lic_seq = 'CAGGGACCCGGT'
        builder.reverse_lic_seq = 'CGAGGAGAAGCCCGGTTA'

        builder.forward_overhang = 'AAAAAA'
        builder.reverse_overhang = 'TTTTTT'
        builder.insert_start_codon = True
        builder.insert_stop_codon = True

        builder.target_temperature = 60
        builder.target_primer_length = None

        constructs = builder.design()

        ## for construct in constructs:
        ##     print(construct.forward_primer)
        ##     print(construct.reverse_primer)
        ##     print(construct.protein_seq)
        ##     print(construct.start_position, construct.stop_position)
