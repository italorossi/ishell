# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('Evolux Console')
hdlr = logging.FileHandler('newshell.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s(%(lineno)s) %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
