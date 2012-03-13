from distutils.core import setup

import Marvin

description = """
Marvin is a program to help molecular biologists when designing protein
constructs (truncated versions of proteins of interest).  It designs the
PRC primers needed to amplify the chosen constructs, and provides tools
for restriction enzyme based cloning, LIC cloning and site directed
mutagenesis.
"""

setup(name='marvin',
      version=Marvin.__version__,
      description='A program to aid crystallography construct design.',
      long_description=description,
      author='Jonathan Ellis',
      author_email='jonathan.j.ellis@gmail.com',
      url='http://jjellis.github.com/marvin',
      packages=['Marvin', 'Marvin.app'],
      scripts=['scripts/marvin.py'],
      provides=['Marvin', 'Marvin.app'],
      requires=['wx (>=2.8)', 'Bio'],
      classifiers = [
          'Topic :: Scientific/Engineering',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)'
      ],
      license = 'GPL'
     )
