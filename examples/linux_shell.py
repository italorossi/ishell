#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ishell.command import Command
from ishell.console import Console

import subprocess


class LS(Command):
    def run(self, line):
        args = line.split()
        command = ['ls']
        command_args = []
        if len(line) > 1:
            command_args = args[1:]
        subprocess.call(command + command_args)


class Bash(Command):
    def run(self, line):
        subprocess.call(['bash'])


class Top(Command):
    def run(self, line):
        subprocess.call(['top'])


class DiskIO(Command):
    def run(self, line):
        try:
            subprocess.call(['iostat', '1'])
        except KeyboardInterrupt:
            print("iostat stopped.")


def main():
    console = Console("root@dev:~", '#')
    ls = LS("ls")
    bash = Bash("bash")
    top = Top("top")
    console.addChild(ls)
    console.addChild(bash)
    console.addChild(top)
    console.addChild(Command('show')).addChild(Command('disk')).addChild(DiskIO('io'))
    console.loop()


if __name__ == '__main__':
    main()
