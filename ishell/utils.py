# -*- coding: utf-8 -*-

import sys
import ishell
import readline


def _print(msg):
    line_buffer = readline.get_line_buffer()
    # Clearing prompt
    sys.stdout.write("\r")
    sys.stdout.write("\033[K")
    sys.stdout.write(str(msg))
    # Restoring prompt - use state management if available, fallback to global
    if hasattr(ishell, '_current_prompt') and ishell._current_prompt:
        prompt = ishell._current_prompt
    else:
        prompt = "Prompt> "
    sys.stdout.write("\n%s" % prompt)
    if line_buffer:
        sys.stdout.write(" %s" % line_buffer)
    sys.stdout.flush()
