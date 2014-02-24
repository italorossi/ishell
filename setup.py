# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pycli',
    version='0.1.0',
    author=u'Ítalo Rossi',
    author_email='italorossib@gmail.com',
    description='Build powerful CLI with Python',
    license='MIT',
    keywords='cli terminal console',
    url='http://github.com/italorossi/pycli',
    py_modules=['pycli'],
    long_description='Build powerful CLI with Python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        "readline",
    ]
)
