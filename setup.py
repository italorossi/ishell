#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import platform

# If we're on Windows, use pyreadline instead of gnureadline
if platform == 'win32':
    requires_file = 'win_requirements.txt'
else:
    requires_file = 'requirements.txt'

with open(requires_file) as f:
    requires = f.readlines()

ishell_version = "0.1.7"

setup(
    name='ishell',
    version=ishell_version,
    author=u'Ítalo Rossi',
    author_email='italorossib@gmail.com',
    description='Build Interactive Shells with Python',
    license='MIT',
    keywords='cli terminal console shell interactive',
    url='http://github.com/italorossi/ishell',
    packages=find_packages(exclude=('tests', 'docs')),
    long_description='Build Interactive Shells with Python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=requires
)
