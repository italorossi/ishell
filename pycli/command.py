#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
from pycli import logger

__all__ = ["Command"]

class Command:
    def  __init__(self, name, help='No help provided', dynamic_args=False):
        self.name = name
        self.childs = {}
        self.child_names = []
        self.dynamic_args = dynamic_args
        self.help = help

    def log(self, msg):
        logger.info('Command %s - %s' % msg)

    def addChild(self, cmd):
        self.child_names.append(cmd.name)
        self.childs[cmd.name] = cmd
        return cmd

    def args(self, word=None):
        """Overwrite this method with custom completions"""
        return [c for c in ['10', '20', '30'] if word is None or c.startswith(word)]

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

            if next_command in self.child_names:
                # Already completed, walking
                cmd = self.childs[next_command]
                return cmd.complete(line[1:], buf, state, run, full_line)
            else:
                logger.debug('Not walking because %s was not found in childs' % next_command)
                if has_arg_completed:
                    # Completing with child commands
                    completions = [c + ' ' for c in self.child_names if c.startswith(next_command)] + [None]
                    logger.debug('PossibleCompletions=>%s' % completions)
                    return completions[state]

        logger.debug('Line=>%s, Buf=>%s, state=>%s' % (line, buf, state))

        if run:
            logger.debug('Executing %s' % self.name)
            self.run(full_line.rstrip())

        logger.debug('Starting arg complete')

        # Checking if user already typed a valid arg without space at end
        if self.dynamic_args:
            if len(line) and buf and line[0] in self.args():
                readline.insert_text(" ")
                logger.debug("Inserted blank space")

        if buf == self.name:
            readline.insert_text(" ")
            logger.debug("Inserted blank space")

        # Starting complete for this command
        # TODO: Reduce this code
        # if self.dynamic_args():
        #     return self.get_dynamic_args(line, buf)
        # else:
        #     return

        if not buf.strip():
            if not self.dynamic_args:
                logger.debug('No buf provided, returning all possibilities: %s' % self.child_names)
                completions = [c + ' ' for c in self.child_names] + [None]
                logger.debug('PossibleCompletions=>%s' % completions)
                return completions[state]
            else:
                if not line:
                    completions = [c + ' ' for c in self.args()] + [None]
                    logger.debug('PossibleCompletions=>%s' % completions)
                    return completions[state]
                else:
                    completions = [c + ' ' for c in self.child_names] + [None]
                    logger.debug('PossibleCompletions=>%s' % completions)
                    return completions[state]
        else:
            if not self.dynamic_args:
                completions = [c + ' ' for c in self.child_names if c.startswith(buf)] + [None]
                logger.debug('PossibleCompletions=>%s' % completions)
                return completions[state]
            else:
                if buf.strip() in self.args():
                    # Jump to the next possibles commands
                    completions = [c + ' ' for c in self.child_names if c.startswith(buf)] + [None]
                    logger.debug('PossibleCompletions=>%s' % completions)
                    return completions[state]
                else:
                    completions = [c + ' ' for c in self.args() if c.startswith(buf)] + [None]
                    logger.debug('PossibleCompletions=>%s' % completions)
                    return completions[state]

    def run(self, line):
        print "Exec %s(line=%s), overwrite this method!" % (self.name, line)

    def __repr__(self):
        return "<Command:(%s), Childs(%s)>" % (self.name, "-".join(self.childs))
