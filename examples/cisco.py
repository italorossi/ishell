#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ishell.command import Command
from ishell.console import Console
from ishell.utils import _print

import getpass


class InterfaceConsole(Command):
    """Interface Console.

    Parameters:
    interface name -- Press tab for options
    """
    def args(self):
        return ["FastEthernet0/0", "FastEthernet1/0"]

    def run(self, line):
        interface = line.split()[-1]
        self.interface = interface
        self.prompt = "RouterA(config-if-%s)" % self.interface
        self.prompt_delim = "#"
        ip = Command("ip", help="Configure ip parameters: address")
        address = Command("address")
        address.run = self.set_address
        self.addChild(ip).addChild(address)
        self.loop()

    def set_address(self, line):
        addr = line.split()[-1]
        _print("Setting interface %s address %s" % (self.interface, addr))


class RouteAdd(Command):
    """RouteAdd Command.

    Parameters:
    network gateway - Example: ip route add 10.0.0.0/8 192.168.0.1
    """
    def run(self, line):
        _print("Route added!")


class ConfigureTerminal(Command):
    """Configure Console.

    Childs:
    interface -- Configure mode for interface
    ip --  IP configuration: route add
    """

    def run(self, line):
        self.prompt = "RouterA(config)"
        self.prompt_delim = "#"
        ip = Command("ip", help="Set ip configurations")
        route = Command("route")
        add = RouteAdd("add")

        interface = InterfaceConsole("interface", dynamic_args=True,
                                     help="Configure interface parameters")

        self.addChild(interface)
        self.addChild(ip).addChild(route).addChild(add)
        self.loop()


class Show(Command):
    """Show Command.

    Childs:
    running-config -- Show RAM configuration
    startup-config --  Show NVRAM configuration
    """

    def args(self):
        return ["running-config", "startup-config"]

    def run(self, line):
        arg = line.split()[-1]
        if arg not in self.args():
            _print("%% Invalid argument: %s" % arg)
            _print("\tUse:")
            _print("\trunning-config -- Show RAM configuration")
            _print("\tstartup-config --  Show NVRAM configuration")
            return
        _print("Executing show %s..." % arg)


class Enable(Command):
    """Enable Command.

    Default password is 'python', if typed correctly you get access
    to router's enable console.

    Childs:
    configure -- Enter configure mode
    show -- Show configurations
    """

    def run(self, line):
        self.prompt = "RouterA"
        self.prompt_delim = "#"
        password = getpass.getpass()
        if password != 'python':
            _print("%% Invalid Password")
            return

        configure = Command("configure", help="Enter configure mode")
        terminal = ConfigureTerminal("terminal")
        configure.addChild(terminal)
        show = Show('show', help="Show configurations", dynamic_args=True)
        self.addChild(configure)
        self.addChild(show)
        self.loop()


class PingCommand(Command):
    """Ping Command.

    Parameters:
    destination -- Destination ip
    """

    def run(self, line):
        destination = line.split()[-1]
        import subprocess
        try:
            subprocess.call(['ping', '-c5', '%s' % destination])
        except KeyboardInterrupt:
            _print("ping canceled.")
            return


class TraceRouteCommand(Command):
    """TraceRoute Command.

    Parameters:
    destination -- Destination ip
    """

    def run(self, line):
        destination = line.split()[-1]
        import subprocess
        try:
            subprocess.call(['traceroute', '%s' % destination])
        except KeyboardInterrupt:
            _print("Traceroute canceled.")
            return


def main():
    console = Console("RouterA")
    enable = Enable("enable", help="Enter enable mode")
    ping = PingCommand('ping', help="Ping destination ip. Ex: ping 8.8.8.8")
    traceroute = TraceRouteCommand('traceroute', help="Trace route to destination ip. Ex: traceroute 8.8.8.8")
    console.addChild(enable)
    console.addChild(ping)
    console.addChild(traceroute)
    console.loop()

if __name__ == '__main__':
    main()
