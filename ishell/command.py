#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
from ishell import logger
from ishell.console import Console
from ishell.utils import _print

__all__ = ["Command"]

class Command(Console):
    def  __init__(self, name, help='No help provided', dynamic_args=False):
        Console.__init__(self)
        self.name = name
        self.childs = {}
        self.dynamic_args = dynamic_args
        self.help = help

    def log(self, msg):
        logger.info('Command %s - %s' % msg)

    def args(self):
        """Overwrite this method with custom completions."""
        return ['10', '20']

    def _dynamic_args(self, state, buf=''):
        args = self.args()
        completions = [c for c in args if buf is None or c.startswith(buf)]
        completions = completions + [None]
        logger.debug("Returned dynamic args: %s" % completions)
        return completions[state]

    def complete(self, line, buf, state, run=False, full_line=None):
        logger.debug('Walked to: %s' % self.name)
        if line:
            # Trying to walk to the next child or suggest the next one
            next_command = line[0]
            has_arg_completed = False
            if self.dynamic_args:
                if len(line) > 1:
                    logger.debug("Dynamic arg '%s' found" % line[0])
                    has_arg_completed = True
                    # Dynamic arg already filled, jump to next word
                    next_command = line[1]
                    line.pop(0)

            if next_command in self.childs.keys():
                if buf:
                    count = 0
                    for c in self.childs.keys():
                        if c.startswith(buf):
                            count += 1
                    if count > 1:
                        logger.debug("More than one candidate, not walking in %s" % buf)
                        return self._next_command(state, buf)
                logger.debug("Found %s in childs, walking." % next_command)
                # Already completed, walking
                cmd = self.childs[next_command]
                return cmd.complete(line[1:], buf, state, run, full_line)
            else:
                logger.debug('Not walking because %s was not found in childs' % next_command)
                if has_arg_completed:
                    return self._next_command(state, next_command)

        logger.debug('Line=>%s, Buf=>%s, state=>%s' % (line, buf, state))

        if run:
            logger.debug('Executing %s' % self.name)
            return self.run(full_line.rstrip())

        logger.debug('Starting arg complete')

        # Checking if user already typed a valid arg without space at end
        if self.dynamic_args:
            if len(line) and buf and line[0] in self.args():
                readline.insert_text(" ")
                logger.debug("Inserted blank space")
            elif len(line) and not buf and line[0] not in self.args():
                logger.debug("Found an unknown arg, suggesting next command.")
                return self._next_command(state, buf)

        if buf == self.name:
            readline.insert_text(" ")
            logger.debug("Inserted blank space")

        if not self.dynamic_args:
            return self._next_command(state, buf)

        if self.dynamic_args:
            if (buf.strip() in self.args()):
                return self._next_command(state, buf)
            elif line and line[0] in self.args():
                return self._next_command(state, buf)
            else:
                return self._dynamic_args(state, buf)
        else:
            return self._next_command(state, buf)

    def _next_command(self, state, buf=''):
        args = self.childs.keys()
        completions = [c + ' ' for c in args if c.startswith(buf)]
        completions = completions + [None]
        logger.debug('PossibleCompletions=>%s' % completions)
        if len(completions) > 2 and state == 0 and not buf:
            logger.debug("Showing all completions...")
            _print("Possible Completions:")
            for child in self.childs.keys():
                _print("  %s%s" % (child.ljust(16), self.childs[child].help))
            return None
        return completions[state]

    def run(self, line):
        _print("Exec %s(line=%s), overwrite this method!" % (self.name, line))

    def __repr__(self):
        return "<Command:(%s), Childs(%s)>" % (self.name, "-".join(self.childs))
