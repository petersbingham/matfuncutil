# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil
shutil.copy('README.md', 'matfuncutil/README.md')

dir_setup = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_setup, 'matfuncutil', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

setup(name='matfuncutil',
      version=__version__,
      description='Containers for functional data in discrete and continuous forms.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['matfuncutil'],
      package_data={'matfuncutil': ['tests/*', 'README.md']}
     )
