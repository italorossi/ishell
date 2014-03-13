# -*- coding: utf-8 -*-


from ishell.utils import _print
import logging


class ConsoleLogHandler(logging.StreamHandler):
    def emit(self, record):
        _print(self.format(record))

    def flush(self):
        pass


logger = logging.getLogger('console app')
hdlr = ConsoleLogHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s(%(lineno)s) %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
