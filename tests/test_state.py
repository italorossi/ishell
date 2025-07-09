#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
from io import StringIO
from ishell.state import ConsoleState


class TestConsoleState(unittest.TestCase):
    
    def test_console_state_creation(self):
        """ConsoleState must be created with default values."""
        state = ConsoleState()
        self.assertEqual(state.prompt, "Prompt")
        self.assertEqual(state.prompt_delim, ">")
        self.assertIsNone(state.welcome_message)
        self.assertFalse(state.should_exit())
        
    def test_console_state_custom_values(self):
        """ConsoleState must be created with custom values."""
        state = ConsoleState(
            prompt="RouterA",
            prompt_delim="#",
            welcome_message="Welcome to RouterA"
        )
        self.assertEqual(state.prompt, "RouterA")
        self.assertEqual(state.prompt_delim, "#")
        self.assertEqual(state.welcome_message, "Welcome to RouterA")
        
    def test_full_prompt_property(self):
        """full_prompt property should return prompt + delimiter."""
        state = ConsoleState("RouterA", "#")
        self.assertEqual(state.full_prompt, "RouterA#")
        
    def test_set_prompt(self):
        """set_prompt should update prompt and optionally delimiter."""
        state = ConsoleState()
        state.set_prompt("NewPrompt", "!")
        self.assertEqual(state.prompt, "NewPrompt")
        self.assertEqual(state.prompt_delim, "!")
        
        # Test setting only prompt
        state.set_prompt("AnotherPrompt")
        self.assertEqual(state.prompt, "AnotherPrompt")
        self.assertEqual(state.prompt_delim, "!")  # Should remain unchanged
        
    def test_set_welcome_message(self):
        """set_welcome_message should update welcome message."""
        state = ConsoleState()
        state.set_welcome_message("New welcome message")
        self.assertEqual(state.welcome_message, "New welcome message")
        
    def test_set_exit(self):
        """set_exit should update exit flag."""
        state = ConsoleState()
        self.assertFalse(state.should_exit())
        
        state.set_exit(True)
        self.assertTrue(state.should_exit())
        
        state.set_exit(False)
        self.assertFalse(state.should_exit())
        
    def test_save_and_restore_state(self):
        """save_state and restore_state should work correctly."""
        state = ConsoleState("Original", ">", "Original welcome")
        
        # Save current state
        state.save_state()
        
        # Modify state
        state.set_prompt("Modified", "!")
        state.set_welcome_message("Modified welcome")
        state.set_exit(True)
        
        # Verify modifications
        self.assertEqual(state.prompt, "Modified")
        self.assertEqual(state.prompt_delim, "!")
        self.assertEqual(state.welcome_message, "Modified welcome")
        self.assertTrue(state.should_exit())
        
        # Restore state
        state.restore_state()
        
        # Verify restoration
        self.assertEqual(state.prompt, "Original")
        self.assertEqual(state.prompt_delim, ">")
        self.assertEqual(state.welcome_message, "Original welcome")
        self.assertFalse(state.should_exit())
        
    def test_temporary_state_context_manager(self):
        """temporary_state context manager should work correctly."""
        state = ConsoleState("Original", ">", "Original welcome")
        
        with state.temporary_state("Temporary", "!", "Temporary welcome"):
            # Inside context, state should be modified
            self.assertEqual(state.prompt, "Temporary")
            self.assertEqual(state.prompt_delim, "!")
            self.assertEqual(state.welcome_message, "Temporary welcome")
            
        # Outside context, state should be restored
        self.assertEqual(state.prompt, "Original")
        self.assertEqual(state.prompt_delim, ">")
        self.assertEqual(state.welcome_message, "Original welcome")
        
    def test_temporary_state_partial_changes(self):
        """temporary_state should allow partial state changes."""
        state = ConsoleState("Original", ">", "Original welcome")
        
        with state.temporary_state(prompt="NewPrompt"):
            # Only prompt should change
            self.assertEqual(state.prompt, "NewPrompt")
            self.assertEqual(state.prompt_delim, ">")  # Unchanged
            self.assertEqual(state.welcome_message, "Original welcome")  # Unchanged
            
        # Should be restored
        self.assertEqual(state.prompt, "Original")
        
    def test_display_welcome(self):
        """display_welcome should write welcome message to stdout."""
        state = ConsoleState(welcome_message="Test welcome")
        
        # Capture stdout
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            state.display_welcome()
            self.assertEqual(captured_output.getvalue(), "Test welcome\n\r")
        finally:
            sys.stdout = original_stdout
            
    def test_display_welcome_no_message(self):
        """display_welcome should do nothing when no welcome message."""
        state = ConsoleState()
        
        # Capture stdout
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            state.display_welcome()
            self.assertEqual(captured_output.getvalue(), "")
        finally:
            sys.stdout = original_stdout
            
    def test_get_display_prompt(self):
        """get_display_prompt should return prompt with space."""
        state = ConsoleState("RouterA", "#")
        self.assertEqual(state.get_display_prompt(), "RouterA# ")
        
    def test_string_representation(self):
        """String representation should be informative."""
        state = ConsoleState("RouterA", "#")
        self.assertEqual(str(state), "ConsoleState(prompt='RouterA', delim='#')")
        
    def test_repr_representation(self):
        """Repr should be detailed."""
        state = ConsoleState("RouterA", "#", "Welcome")
        expected = ("ConsoleState(prompt='RouterA', "
                   "prompt_delim='#', "
                   "welcome_message='Welcome', "
                   "exit=False)")
        self.assertEqual(repr(state), expected)


if __name__ == '__main__':
    unittest.main()