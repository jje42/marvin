from distutils.core import setup


description = """
Marvin is a program to help molecular biologists when designing protein
constructs (truncated versions of proteins of interest).  It designs the
PRC primers needed to amplify the chosen constructs, and provides tools
for restriction enzyme based cloning, LIC cloning and site directed
mutagenesis.
"""

setup(name='marvin',
      version='0.6.2',
      packages=['Marvin', 'Marvin.app'],
      scripts=['scripts/marvin.py'],
      provides=['Marvin', 'Marvin.app'],

      author='Jonathan Ellis',
      author_email='jonathan.j.ellis@gmail.com',
      description='A program to aid crystallography construct design.',
      long_description=description,
      url='http://jjellis.github.com/marvin',
      classifiers = [
          'Topic :: Scientific/Engineering',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)'
      ],
      license = 'GPL'
     )
