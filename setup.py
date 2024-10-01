#!/usr/bin/env python3
"""Setup script for image2ascii"""

import codecs
import os
import re
from setuptools import setup, find_packages


def read(*parts):
    """Read file and return contents"""
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    """Return version number from main module"""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


INSTALL_REQUIRES = [
    'setuptools',
    'ascii_magic',
    'justpy',
    'html2image'
]

PYTHON_REQUIRES = '>=3.7'

setup(name='image2ascii',
      packages=find_packages(),
      version=find_version('image2ascii', 'image2ascii.py'),
      license='Apache License 2.0',
      install_requires=INSTALL_REQUIRES,
      python_requires=PYTHON_REQUIRES,
      platforms=['linux', 'windows'],
      description='Generate ASCII art from images',
      long_description='Generate ASCII art from images',
      author='Johan van der Knijff',
      author_email='johan.vanderknijff@kb.nl',
      maintainer='Johan van der Knijff',
      maintainer_email='johan.vanderknijff@kb.nl',
      url='https://github.com/KBNLresearch/image2ascii',
      download_url=('https://github.com/KBNLresearch/image2ascii/archive/' +
                    find_version('image2ascii', 'image2ascii.py') + '.tar.gz'),
      zip_safe=False,
      entry_points={'console_scripts': [
                        'image2ascii = image2ascii.image2ascii:main']},
      classifiers=[
          'Programming Language :: Python :: 3',]
     )
