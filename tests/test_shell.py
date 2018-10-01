import unittest
from ishell.console import Console
from ishell.command import Command

class TestConsole(unittest.TestCase):

    def test_console_creation(self):
        """Console must be created."""
        c = Console()
        assert isinstance(c, Console)

    def test_console_has_prompt(self):
        """Console should have a default prompt string."""
        c = Console()
        assert c.prompt == "Prompt"
        assert c.prompt_delim == ">"

    def test_console_has_empty_welcome_message(self):
        """Console should has an empty welcome message."""
        c = Console()
        assert c.welcome_message == ""

    def test_console_has_welcome_message(self):
        """Console should have a welcome message."""
        c = Console(welcome_message='welcome message')
        assert c.welcome_message == "welcome message"


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
        # State 0 must print all commands followed by help message
        # and return None as candidates
        candidates = cmd1.complete('', '', 0, run=False, full_line='configure ')
        assert None == candidates
        candidates = cmd1.complete('', 'in', 0, run=False, full_line='configure in')
        assert 'interface ' == candidates
        candidates = cmd1.complete('', 't', 0, run=False, full_line='configure t')
        assert 'terminal ' == candidates

    def test_completion_with_buffer(self):
        """Command must complete correctly with buffer provided."""
        cmd1 = Command('configure')
        cmd2 = Command('terminal')
        cmd1.addChild(cmd2)
        candidates = cmd1.complete(['t'], 't', 0, run=False, full_line='configure ')
        assert 'terminal ' == candidates
        candidates = cmd1.complete(['t'], 't', 1, run=False, full_line='configure ')
        assert None == candidates

    def test_completion_with_dynamic_arg(self):
        cmd1 = Command('show')
        cmd2 = Command('call', dynamic_args=True)
        cmd3 = Command('calls', dynamic_args=True)
        cmd2.args = lambda: ['100', '101']
        cmd3.args = lambda: ['continuous', 'raw']
        cmd1.addChild(cmd2)
        cmd1.addChild(cmd3)

        candidates = cmd1.complete(['c'], '', 0, run=False, full_line='show calls')
        self.assertEqual(None, candidates)
        candidates = cmd1.complete(['c'], 'c', 0, run=False, full_line='show calls')
        self.assertEqual('call ', candidates)
        candidates = cmd1.complete(['c'], 'c', 1, run=False, full_line='show calls')
        self.assertEqual('calls ', candidates)

        candidates = cmd2.complete([''], '', 0, run=False, full_line='show calls')
        self.assertEqual(None, candidates)
        candidates = cmd2.complete([''], '1', 0, run=False, full_line='show calls')
        self.assertEqual('100', candidates)
        candidates = cmd2.complete([''], '1', 1, run=False, full_line='show calls')
        self.assertEqual('101', candidates)

        candidates = cmd3.complete([''], '', 0, run=False, full_line='show calls c')
        self.assertEqual(None, candidates)
        candidates = cmd3.complete([''], 'c', 0, run=False, full_line='show calls c')
        self.assertEqual('continuous', candidates)
        candidates = cmd3.complete([''], 'r', 0, run=False, full_line='show calls c')
        self.assertEqual('raw', candidates)

        candidates = cmd1.complete(['calls', 'c'], 'c', 0, run=False, full_line='show calls c')
        self.assertEqual('continuous', candidates)

        candidates = cmd2.complete(['1'], '1', 0, run=False, full_line='show calls c')
        self.assertEqual('100', candidates)
        candidates = cmd2.complete(['1'], '1', 1, run=False, full_line='show calls c')
        self.assertEqual('101', candidates)

if __name__ == '__main__':
    unittest.main()
