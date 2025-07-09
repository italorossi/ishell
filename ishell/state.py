#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager


class ConsoleState:
    """
    Manages console state including prompt, delimiter, and other console properties.
    Provides context management for temporary state changes and eliminates global state.
    """
    
    def __init__(self, prompt="Prompt", prompt_delim=">", welcome_message=None):
        """
        Initialize console state.
        
        Args:
            prompt (str): The prompt string to display
            prompt_delim (str): The delimiter to append to the prompt
            welcome_message (str): Optional welcome message to display
        """
        self.prompt = prompt
        self.prompt_delim = prompt_delim
        self.welcome_message = welcome_message
        self._exit = False
        self._previous_state = None
        
    @property
    def full_prompt(self):
        """Get the full prompt string with delimiter."""
        return self.prompt + self.prompt_delim
        
    def set_prompt(self, prompt, prompt_delim=None):
        """
        Set the prompt and optionally the delimiter.
        
        Args:
            prompt (str): New prompt string
            prompt_delim (str): Optional new delimiter
        """
        self.prompt = prompt
        if prompt_delim is not None:
            self.prompt_delim = prompt_delim
            
    def set_welcome_message(self, message):
        """Set the welcome message."""
        self.welcome_message = message
        
    def set_exit(self, exit_flag=True):
        """Set the exit flag."""
        self._exit = exit_flag
        
    def should_exit(self):
        """Check if the console should exit."""
        return self._exit
        
    def save_state(self):
        """Save current state for later restoration."""
        self._previous_state = {
            'prompt': self.prompt,
            'prompt_delim': self.prompt_delim,
            'welcome_message': self.welcome_message,
            '_exit': self._exit
        }
        
    def restore_state(self):
        """Restore previously saved state."""
        if self._previous_state:
            self.prompt = self._previous_state['prompt']
            self.prompt_delim = self._previous_state['prompt_delim']
            self.welcome_message = self._previous_state['welcome_message']
            self._exit = self._previous_state['_exit']
            self._previous_state = None
            
    @contextmanager
    def temporary_state(self, prompt=None, prompt_delim=None, welcome_message=None):
        """
        Context manager for temporary state changes.
        
        Args:
            prompt (str): Temporary prompt
            prompt_delim (str): Temporary delimiter
            welcome_message (str): Temporary welcome message
            
        Yields:
            ConsoleState: The modified state object
        """
        # Save current state
        original_prompt = self.prompt
        original_delim = self.prompt_delim
        original_welcome = self.welcome_message
        
        # Apply temporary changes
        if prompt is not None:
            self.prompt = prompt
        if prompt_delim is not None:
            self.prompt_delim = prompt_delim
        if welcome_message is not None:
            self.welcome_message = welcome_message
            
        try:
            yield self
        finally:
            # Restore original state
            self.prompt = original_prompt
            self.prompt_delim = original_delim
            self.welcome_message = original_welcome
            
    def display_welcome(self):
        """Display the welcome message if set."""
        if self.welcome_message:
            sys.stdout.write(self.welcome_message + "\n\r")
            
    def get_display_prompt(self):
        """Get the prompt string for display."""
        return self.full_prompt + " "
        
    def __str__(self):
        """String representation of the state."""
        return f"ConsoleState(prompt='{self.prompt}', delim='{self.prompt_delim}')"
        
    def __repr__(self):
        """Detailed string representation."""
        return (f"ConsoleState(prompt='{self.prompt}', "
                f"prompt_delim='{self.prompt_delim}', "
                f"welcome_message='{self.welcome_message}', "
                f"exit={self._exit})")