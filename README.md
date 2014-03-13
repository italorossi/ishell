ishell
======

Create interactive shell with Python.

## Example

    #!/usr/bin/env python

    from ishell.command import Command, Console
    from ishell import logger


    def main():
        logger.info("Welcome to ishell.")
        console = Console(prompt="someone@someplace ", prompt_delim="#")
        configure = Command('configure', help='Configure mode')
        terminal = Command('terminal')
        interface = Command('interface', help='Configure interface parameters.')
        configure.addChild(terminal)
        configure.addChild(interface)
        console.addChild(configure)
        console.loop()

    if __name__ == '__main__':
        main()


> More documentation is coming
