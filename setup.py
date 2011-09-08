from distutils.core import setup

import const


setup(name='construct',
      version=const.__version__,
      description='A program to aid crystallography construct design.',
      author='Jonathan Ellis',
      author_email='jonathan.j.ellis@gmail.com',
      url='',
      packages=['const', 'const.app'],
      scripts=['scripts/construct.py'],
      provides=['const', 'const.app'],
      #requires=['wx (>=2.8)', 'Bio'],
      install_requires=[
          'wx (>=2.8)',
          'Bio',
          ]
      )

## setup(name='construct',
##       version=construct.__version__,
##       description='',
##       author='Jonathan Ellis',
##       author_email='jonathan.j.ellis@gmail.com',
##       url='',
##       packages=['construct', 'construct.app'],
##       package_dir={'construct': 'construct',
##                    'construct.app': 'construct/app'},
##       scripts=['scripts/construct'],
##       long_description='',
##       ## classifiers=['License :: ???',
##       ##              'Programming Language :: Python'],
##       ## keywords='',
##       ## license='',
##       )


