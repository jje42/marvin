# -*- mode: python; coding: utf-8; -*-
""""""
from __future__ import print_function, division

import re
import urllib2

def search(search_term=None):
    """Search codon usage database.

    >>> import pprint
    >>> terms = search()
    >>> pprint.pprint(sorted(terms)[:3])
    [('Escherichia coli', 37762),
     ('Escherichia coli 536', 362663),
     ('Escherichia coli APEC O1', 405955)]
    """
    url = 'http://www.kazusa.or.jp/codon/cgi-bin/spsearch.cgi?species={0}&c=i'
    regex = re.compile(r'<A HREF=".+?species=(\d+)">.+?<I>(.+?)</I>.+?</A><BR>',
                       re.DOTALL)
    if search_term is None:
        search_term = 'Escherichia coli'

    handle = urllib2.urlopen(url.format(search_term.replace(' ', '+')))
    data = handle.read()
    d = []
    found = False
    for match in regex.finditer(data):
        found = True
        species_id = match.group(1)
        species_name = match.group(2).strip()
        d.append((species_name, species_id))
    if found:
        d.sort()
        #names = [x[0] for x in d]
        #names = ['{0} {1}'.format(x[0], x[1]) for x in d]
        return [(x[0], int(x[1])) for x in d]

    raise ValueError('no species found')
                     

              
def usage_table(species_id=37762):
    """Create codon usage table for species.
    
    >>> table = usage_table()
    >>> assert table['A'] == 'GCA'
    >>> assert table['C'] == 'TGT'
    >>> assert table['D'] == 'GAT'
    >>> ''.join(sorted(table.keys()))
    'ACDEFGHIKLMNPQRSTVWY'
    """
    # 37762 is the code for E. coli
    url = 'http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species={0}&aa=1&style=N'
    handle = urllib2.urlopen(url.format(species_id))
    data = handle.read()
    regex = re.compile(
        r'''(?P<codon>[UAGC]{3})
        \s+                     
        (?P<amino>[A-Z])
        \s+
        (?P<frequency>\d+\.\d+)
        \s+
        (?P<per1000>\d+\.\d+)
        \s
        \(\s*(?P<count>\d+)\)''',
        re.VERBOSE)

    match = re.search(r'<PRE>(.+)</PRE>', data, re.DOTALL)
    if match:
        data = match.group(1)

        d = {}
        for line in data.splitlines():
            for match in regex.finditer(line):
                amino = match.group('amino')
                codon = match.group('codon').replace('U', 'T')
                freq = match.group('frequency')
                d.setdefault(amino, []).append((freq, codon))
        for key in d.iterkeys():
            d[key].sort(reverse=True)

        x = {}
        for key in d.iterkeys():
            x[key] = d[key][0][1]

        return x
