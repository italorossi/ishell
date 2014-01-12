import unittest
from pycli.console import Console
from pycli.command import Command

class TestConsole(unittest.TestCase):

    def test_console_creation(self):
        """Console must be created."""
        c = Console()
        assert isinstance(c, Console)

    def test_console_has_prompt(self):
        """Console should have a default prompt string."""
        c = Console()
        assert c.prompt == "Promp> "


class TestCommand(unittest.TestCase):
    def test_command_creation(self):
        """Command must be created with name and default help message."""
        cmd = Command('configure')
        assert cmd.name == 'configure'
        assert cmd.help == 'No help provided'
        assert cmd.dynamic_args == False

    def test_simple_completion(self):
        """Command must complete with only one option."""
        cmd1 = Command('configure')
        cmd2 = Command('terminal')
        cmd1.addChild(cmd2)
        candidates = cmd1.complete('', '', 0, run=False, full_line='configure ')
        assert 'terminal ' == candidates
        candidates = cmd1.complete('', '', 1, run=False, full_line='configure ')
        assert None == candidates

    def test_double_completion(self):
        """Command must complete with two options."""
        cmd1 = Command('configure')
        cmd2 = Command('terminal')
        cmd3 = Command('interface')
        cmd1.addChild(cmd2)
        cmd1.addChild(cmd3)
        candidates = cmd1.complete('', '', 0, run=False, full_line='configure ')
        assert 'terminal ' == candidates
        candidates = cmd1.complete('', '', 1, run=False, full_line='configure ')
        assert 'interface ' == candidates
        candidates = cmd1.complete('', '', 2, run=False, full_line='configure ')
        assert None == candidates

    def test_completion_with_buffer(self):
        """Command must complete correctly with buffer provided."""
        cmd1 = Command('configure')
        cmd2 = Command('terminal')
        cmd1.addChild(cmd2)
        candidates = cmd1.complete(['t'], 't', 0, run=False, full_line='configure ')
        assert 'terminal ' == candidates
        candidates = cmd1.complete(['t'], 't', 1, run=False, full_line='configure ')
        assert None == candidates


if __name__ == '__main__':
    unittest.main()
