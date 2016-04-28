#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import re

version_raw    = open('nekpy/_version.py').read()
version_regex  = r"^__version__ = ['\"]([^'\"]*)['\"]"
version_result = re.search(version_regex, version_raw, re.M)
if version_result:
    version_string = version_result.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(name='nekpy',
      version=version_string,
      description='Nek-related utilities in python',
      url='http://github.com/maxhutch/nekpy/',
      author='https://raw.github.com/maxhutch/nekpy/master/AUTHORS.md',
      author_email='maxhutch@gmail.com',
      maintainer='Max Hutchinson',
      maintainer_email='maxhutch@gmail.com',
      license='MIT',
      keywords='nek5000',
      install_requires=list(open('requirements.txt').read().strip()
                            .split('\n')),
      long_description=(open('README.rst').read() if exists('README.rst')
                              else ''),
      packages=['nekpy', 'nekpy.dask', 'nekpy.tools'],
      package_dir={'nekpy.tools': 'nekpy/tools'},
      package_data={'nekpy.tools': ['default.json', 'template*']}, 
      zip_safe=False)
