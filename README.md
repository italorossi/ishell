ishell
===

[![PyPI version](https://badge.fury.io/py/ishell.svg)](http://badge.fury.io/py/ishell)
![Travis](https://api.travis-ci.org/italorossi/ishell.svg?branch=master)
![Downloads](https://img.shields.io/pypi/dm/ishell.svg)

Create an interactive shell with Python.

ishell helps you to easily create an interactive shell for your application. It supports command completion, dynamic arguments, a command history, and chaining of commands.

![Cisco like console](http://i.imgur.com/RKzuwDu.png)

Installation
-----------

You can install ishell using pip:
    
    pip install ishell
    
## Basics

#### Console

When building your first application you can start with one console. You can specify the prompt and prompt delimiter:

```python
from ishell.console import Console
console = Console(prompt="someone@someplace ", prompt_delim="#")
console.loop()
```

Then you have:

![Console](http://i.imgur.com/jebkhlQ.png)

#### Command

The next step is to create a new command and attach it to the console:

```python
from ishell.console import Console
from ishell.command import Command
console = Console(prompt="someone@someplace ", prompt_delim="#")

class UsersCommand(Command):
    def run(self, line):
        print "Showing all users..."

users_command = UsersCommand("users", help="Show all users")

console.addChild(users_command)
console.loop()
```

With the users_command attached to the console you can just hit ENTER and a help message will be printed, if you press TAB the users command will be entered and you can hit ENTER again to execute the command:

![Users Command](http://i.imgur.com/opZZt1J.png)

##### Command Arguments

You can complete commands with dynamic arguments:

```python
from ishell.console import Console
from ishell.command import Command
console = Console(prompt="someone@someplace ", prompt_delim="#")

class UsersCommand(Command):
    def args(self):
        return ['online', 'offline']

    def run(self, line):
        last_arg = line.split()[-1]
        print "Showing all users %s..." % last_arg

users_command = UsersCommand("users", help="Show all users", dynamic_args=True)

console.addChild(users_command)
console.loop()
```

![Users arguments](http://i.imgur.com/YmoENgG.png)


##### Connecting Commands

You can connect commands with each other to build a more verbose command line: (Press TAB to complete)

```python
from ishell.console import Console
from ishell.command import Command
console = Console(prompt="someone@someplace ", prompt_delim="#")

class UsersCommand(Command):
    def args(self):
        return ['online', 'offline']

    def run(self, line):
        last_arg = line.split()[-1]
        print "Showing all users %s..." % last_arg

users_command = UsersCommand("users", help="Show all users", dynamic_args=True)

show = Command("show", help="Show command helper")
console.addChild(show).addChild(users_command)
console.loop()
```

Example: show users [online|offline]

![Show Users](http://i.imgur.com/zkXHCVE.png)

- Check examples directory for cisco like terminal and a linux minimal shell.

