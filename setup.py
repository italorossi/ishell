#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ishell
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requires = f.readlines()


setup(
    name='ishell',
    version=ishell.__version__,
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
