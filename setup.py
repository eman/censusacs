#!/usr/bin/env python
import os
from setuptools import setup

project_dir = os.path.abspath(os.path.dirname(__file__))
description = 'Cenus ACS - Get ACS Data from the US Census'

long_descriptions = []
for rst in ('README.rst', 'LICENSE.rst'):
    with open(os.path.join(project_dir, rst), 'r') as f:
        long_descriptions.append(f.read())


setup(name='censusacs',
      version='0.9.1',
      description=description,
      long_description='\n\n'.join(long_descriptions),
      author='Kevala Analytics, Inc.',
      author_email='eman@kevalaanalytics.com',
      url='https://://github.com/KevalaAnalytics',
      license='BSD',
      py_modules=['censusacs'],
      install_requires=['requests', 'pandas'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Census',
          'Topic :: Utilities',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3'],
      keywords='Census ACS',
      )
