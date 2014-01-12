#!/usr/bin/env python
import sys
import readline
from pycli import logger


class Console:
    def __init__(self, prompt=None):
        self.childs = {}
        if not prompt:
            self.prompt = "Promp> "
        else:
            self.prompt = prompt

    def addChild(self, cmd):
        self.childs[cmd.name] = cmd

    def get_command(self, cmd_name):
        return self.childs[cmd_name]

    def is_child(self, cmd_name):
        for cmd in self.childs.values():
            if cmd_name == cmd.name:
                return True
        return False

    def completions(self, word=None):
        completions = [cmd.name + ' ' for cmd in self.childs.values() \
                                if word is None or cmd.name.startswith(word)]
        return completions

    def walk(self, buf, state, run=False, full_line=None):
        # Current commands in line
        line = readline.get_line_buffer()
        line_commands = line.split()
        if run:
            line_commands = buf.split()
        logger.debug("Line=>%s" % line_commands)

        if not line and not buf and not run:
            completions = self.completions() + [None]
            return completions[state]

        # Traversing current command
        for cmd_name in line_commands:
            if self.is_child(cmd_name):
                logger.debug("Found existing command=>%s" % cmd_name)
                #if not line.endswith(' '):
                    #logger.debug("Inserting space to line buffer")
                    #readline.insert_text(" ")
                cmd = self.get_command(cmd_name)
                return cmd.complete(line_commands[1:], buf, state, run, full_line)

        # Needing completion
        logger.debug('buffer=> %s, state=>%s' % (buf, state))
        tokens = buf.split()
        logger.debug('tokens=>%s' % tokens)

        # Nothing was provided, running root completion
        completions = self.completions(tokens[0])
        completions += [None]
        logger.debug('completions=>%s' % completions)
        logger.debug('END COMPLETE')
        return completions[state]

    def walk_and_run(self, command):
        self.walk(command, 0, run=True, full_line=command)

    def help(self):
        print "Help:"
        for command in self.childs.values():
            print "%15s - %30s" % (command.name, command.help)
        print

    def loop(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.walk)

        while 1:
            try:
                input_ = raw_input(self.prompt)
                if not input_:
                    self.help()
                elif input_ in ('quit', 'exit'):
                    break
                else:
                    self.walk_and_run(input_)

            except Exception, e:
                print "Error: %s" % e
                sys.exit(1)
