#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from ishell.console import Console
from ishell.command import Command
from ishell.state import ConsoleState


class TestStateIntegration(unittest.TestCase):
    
    def test_console_has_state(self):
        """Console should have state management."""
        console = Console("TestConsole", ">", "Welcome")
        self.assertIsInstance(console.state, ConsoleState)
        self.assertEqual(console.state.prompt, "TestConsole")
        self.assertEqual(console.state.prompt_delim, ">")
        self.assertEqual(console.state.welcome_message, "Welcome")
        
    def test_console_backward_compatibility(self):
        """Console should maintain backward compatibility."""
        console = Console("TestConsole", ">", "Welcome")
        # Old attributes should still work
        self.assertEqual(console.prompt, "TestConsole")
        self.assertEqual(console.prompt_delim, ">")
        self.assertEqual(console.welcome_message, "Welcome")
        
    def test_command_has_parent_console(self):
        """Command should have parent_console attribute."""
        console = Console("TestConsole", ">")
        cmd = Command("test", help="Test command")
        console.addChild(cmd)
        self.assertEqual(cmd.parent_console, console)
        
    def test_command_can_access_state(self):
        """Command should be able to access console state."""
        console = Console("TestConsole", ">", "Welcome")
        cmd = Command("test", help="Test command")
        console.addChild(cmd)
        
        # Command should be able to access parent console state
        self.assertEqual(cmd.parent_console.state.prompt, "TestConsole")
        self.assertEqual(cmd.parent_console.state.full_prompt, "TestConsole>")
        
    def test_state_synchronization(self):
        """State changes should be synchronized."""
        console = Console("TestConsole", ">", "Welcome")
        
        # Change state through state management
        console.state.set_prompt("NewPrompt", "!")
        
        # Old attributes should be updated for backward compatibility
        self.assertEqual(console.prompt, "NewPrompt")
        self.assertEqual(console.prompt_delim, "!")
        
        # State should reflect changes
        self.assertEqual(console.state.prompt, "NewPrompt")
        self.assertEqual(console.state.prompt_delim, "!")
        self.assertEqual(console.state.full_prompt, "NewPrompt!")
        
    def test_exit_state_management(self):
        """Exit state should be managed through state."""
        console = Console("TestConsole", ">")
        
        # Initially should not exit
        self.assertFalse(console.state.should_exit())
        self.assertFalse(console._exit)
        
        # Set exit through state
        console.state.set_exit(True)
        self.assertTrue(console.state.should_exit())
        self.assertTrue(console._exit)  # Backward compatibility
        
        # Set exit through old method
        console._exit = False
        console.exit()
        self.assertTrue(console.state.should_exit())
        self.assertTrue(console._exit)
        
    def test_multiple_commands_state_access(self):
        """Multiple commands should access the same state."""
        console = Console("TestConsole", ">", "Welcome")
        
        cmd1 = Command("cmd1", help="Command 1")
        cmd2 = Command("cmd2", help="Command 2")
        
        console.addChild(cmd1)
        console.addChild(cmd2)
        
        # Both commands should access the same console state
        self.assertEqual(cmd1.parent_console, console)
        self.assertEqual(cmd2.parent_console, console)
        self.assertEqual(cmd1.parent_console.state, cmd2.parent_console.state)
        
    def test_state_isolation(self):
        """Different consoles should have isolated state."""
        console1 = Console("Console1", ">", "Welcome 1")
        console2 = Console("Console2", "!", "Welcome 2")
        
        self.assertNotEqual(console1.state.prompt, console2.state.prompt)
        self.assertNotEqual(console1.state.prompt_delim, console2.state.prompt_delim)
        self.assertNotEqual(console1.state.welcome_message, console2.state.welcome_message)
        
    def test_state_context_manager_integration(self):
        """State context manager should work with console integration."""
        console = Console("TestConsole", ">", "Welcome")
        
        # Test temporary state changes
        with console.state.temporary_state("TempPrompt", "!", "Temp welcome"):
            self.assertEqual(console.state.prompt, "TempPrompt")
            self.assertEqual(console.state.prompt_delim, "!")
            self.assertEqual(console.state.welcome_message, "Temp welcome")
            
        # State should be restored
        self.assertEqual(console.state.prompt, "TestConsole")
        self.assertEqual(console.state.prompt_delim, ">")
        self.assertEqual(console.state.welcome_message, "Welcome")
        
    def test_state_save_restore_integration(self):
        """State save/restore should work with console integration."""
        console = Console("TestConsole", ">", "Welcome")
        
        # Save current state
        console.state.save_state()
        
        # Modify state
        console.state.set_prompt("ModifiedPrompt", "!")
        console.state.set_welcome_message("Modified welcome")
        
        # Verify modifications
        self.assertEqual(console.state.prompt, "ModifiedPrompt")
        self.assertEqual(console.state.prompt_delim, "!")
        self.assertEqual(console.state.welcome_message, "Modified welcome")
        
        # Restore state
        console.state.restore_state()
        
        # Verify restoration
        self.assertEqual(console.state.prompt, "TestConsole")
        self.assertEqual(console.state.prompt_delim, ">")
        self.assertEqual(console.state.welcome_message, "Welcome")


if __name__ == '__main__':
    unittest.main()