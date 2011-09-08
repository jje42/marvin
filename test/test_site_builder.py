#! /usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
""""""
from __future__ import print_function, division


import os, sys
sys.path.insert(0, os.pardir)

import construct.codon as codon
import const.restriction as restriction
from const.builder import SiteBuilder

from Bio import SeqIO

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

for construct in constructs:
    print(construct.forward_primer)
    print(construct.reverse_primer)
    print(construct.protein_seq)
    print(construct.start_position, construct.stop_position)
