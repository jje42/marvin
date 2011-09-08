# -*- mode: python; -*-
#
# Copyright (C) 2011 Jonathan Ellis
#
# Author: Jonathan Ellis <jonathan.ellis.research@gmail.com>
#
from distutils.core import setup

import const


setup(name='construct',
      version=const.__version__,
      description='A program to aid crystallography construct design.',
      author='Jonathan Ellis',
      author_email='jonathan.ellis.research@gmail.com',
      url='',
      packages=['const', 'const.app'],
      scripts=['scripts/construct.py'],
      provides=['const', 'const.app'],
      requires=['wx (>=2.8)', 'Bio'],
      )
