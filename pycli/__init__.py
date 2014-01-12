#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import readline

from termcolor import cprint

logger = logging.getLogger('Evolux Console')
hdlr = logging.FileHandler('newshell.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s(%(lineno)s) %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

red = lambda x: cprint(x, 'red')
grey = lambda x: cprint(x, 'grey')
green = lambda x: cprint(x, 'green')
yellow = lambda x: cprint(x, 'yellow')
blue = lambda x: cprint(x, 'blue')
magenta = lambda x: cprint(x, 'magenta')
cyan = lambda x: cprint(x, 'cyan')
white = lambda x: cprint(x, 'white')

__version__ = "0.1"
