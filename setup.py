from distutils.core import setup

import Marvin


setup(name='marvin',
      version=Marvin.__version__,
      description='A program to aid crystallography construct design.',
      author='Jonathan Ellis',
      author_email='jonathan.j.ellis@gmail.com',
      url='',
      packages=['Marvin', 'Marvin.app'],
      scripts=['scripts/marvin.py'],
      provides=['Marvin', 'Marvin.app'],
      requires=['wx (>=2.8)', 'Bio'],
      )
