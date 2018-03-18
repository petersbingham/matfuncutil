# -*- coding: utf-8 -*-

from distutils.core import setup
import shutil
shutil.copy('README.md', 'matfuncutil/README.md')

setup(name='matfuncutil',
      version='0.11',
      description='Containers for functional data in discrete and continuous forms.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['matfuncutil'],
      package_data={'matfuncutil': ['tests/*', 'README.md']}
     )
