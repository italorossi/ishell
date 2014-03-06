# -*- coding: utf-8 -*-

import sys
import shell
import readline


def _print(msg):
    line_buffer = readline.get_line_buffer()
    # Clearing prompt
    sys.stdout.write("\r")
    sys.stdout.write("\033[K")
    sys.stdout.write(str(msg))
    # Restoring prompt
    sys.stdout.write("\n%s" % shell._current_prompt)
    if line_buffer:
        sys.stdout.write(" %s" % line_buffer)
    sys.stdout.flush()
