#! /usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
""""""
from __future__ import print_function, division


import os, sys
sys.path.insert(0, os.pardir)

import unittest2 as unittest

import const.codon as codon
import const.restriction as restriction
from const.builder import SiteBuilder

from Bio import SeqIO


class SiteBuilderIntegrationTestCase(unittest.TestCase):

    def test_sitebuilder(self):
        with open('gapdh_dna.fsa') as handle:
            s = SeqIO.read(handle, 'fasta')

        builder = SiteBuilder()
        builder.nucleotide_seq = s.seq
        builder.add_site(6, 'G', 'A')
        builder.forward_overhang = 'AAAAAA'
        builder.reverse_overhang = 'TTTTTT'
        builder.insert_start_codon = True
        builder.insert_stop_codon = True
        species_list = codon.search('Escherichia coli')
        species_id = species_list[0][1]
        builder.codon_table = codon.usage_table(species_id)
        builder.target_temperature = 60
        builder.target_primer_length = None
        constructs = builder.design()

        ## for construct in constructs:
        ##     print(construct.forward_primer)
        ##     print(construct.reverse_primer)
        ##     print(construct.protein_seq)
        ##     print(construct.start_position, construct.stop_position)

        construct = constructs[0]

        self.assertEqual(str(construct.forward_primer),
                         'aaaaaaatggtagttaaagttgcaattaacggtttcggacgtatcgg')
        self.assertEqual(str(construct.reverse_primer),
                         'ttttttccgatacgtccgaaaccgttaattgcaactttaactaccat')
        self.assertEqual(construct.protein_seq,
                         ('MVVKVAINGFGRIGRLAFRRIQNVEGVEVTRINDLTDPVMLAHLLKYDT'
                          'TQGRFDGTVEVKEGGFEVNGKFIKVSAERDPEQIDWATDGVEIVLEATG'
                          'FFAKKEAAEKHLKGGAKKVVITAPGGNDVKTVVFNTNHDVLDGTETVIS'
                          'GASCTTNCLAPMAKALQDNFGVVEGLMTTIHAYTGDQMILDGPHRGGDL'
                          'RRARAGAANIVPNSTGAAKAIGLVIPELNGKLDGSAQRVPTPTGSVTEL'
                          'VAVLEKNVTVDEVNAAMKAASNESYGYTEDPIVSSDIVGMSYGSLFDAT'
                          'QTKVLDVDGKQLVKVVSWYDNEMSYTAQLVRTLEYFAKIAK*'))
        self.assertEqual(construct.start_position, 6)
        self.assertEqual(construct.stop_position, 6)

