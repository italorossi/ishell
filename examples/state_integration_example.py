#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ishell.console import Console
from ishell.command import Command
from ishell.utils import _print


class StateAwareCommand(Command):
    """Command that demonstrates state management integration."""
    
    def run(self, line):
        if self.parent_console:
            _print(f"Current console state: {self.parent_console.state}")
            _print(f"Full prompt: {self.parent_console.state.full_prompt}")
            
            # Demonstrate temporary state changes
            with self.parent_console.state.temporary_state(
                prompt="TemporaryState",
                prompt_delim=">"
            ):
                _print("In temporary state:")
                _print(f"  Prompt: {self.parent_console.state.full_prompt}")
                
            _print("Back to original state:")
            _print(f"  Prompt: {self.parent_console.state.full_prompt}")
        else:
            _print("No parent console available")


class NestedStateCommand(Command):
    """Command that creates nested console with state management."""
    
    def run(self, line):
        if self.parent_console:
            _print("Creating nested console with different state...")
            
            # Create a nested console with different state
            nested_console = Console("NestedConsole", ">", "Welcome to nested console")
            
            # Add some commands to the nested console
            help_cmd = Command("help", help="Show help")
            help_cmd.run = lambda line: _print("Nested console help")
            
            exit_cmd = Command("exit", help="Exit nested console")
            exit_cmd.run = lambda line: nested_console.state.set_exit(True)
            
            nested_console.addChild(help_cmd)
            nested_console.addChild(exit_cmd)
            
            _print("Entering nested console...")
            nested_console.loop()
            _print("Exited nested console")
        else:
            _print("No parent console available")


class ConfigCommand(Command):
    """Command that demonstrates configuration state management."""
    
    def run(self, line):
        if self.parent_console:
            _print("Entering configuration mode...")
            
            # Save current state
            self.parent_console.state.save_state()
            
            # Change to configuration state
            self.parent_console.state.set_prompt("ConfigMode", ">")
            self.parent_console.state.set_welcome_message("Configuration mode active")
            
            _print(f"Current state: {self.parent_console.state.full_prompt}")
            _print("Configuration mode active. Type 'exit' to return.")
            
            # Create a simple config console
            config_console = Console("ConfigMode", ">", "Configuration mode active")
            
            # Add config commands
            interface_cmd = Command("interface", help="Configure interface")
            interface_cmd.run = lambda line: _print("Interface configuration")
            
            ip_cmd = Command("ip", help="Configure IP")
            ip_cmd.run = lambda line: _print("IP configuration")
            
            exit_cmd = Command("exit", help="Exit configuration mode")
            exit_cmd.run = lambda line: config_console.state.set_exit(True)
            
            config_console.addChild(interface_cmd)
            config_console.addChild(ip_cmd)
            config_console.addChild(exit_cmd)
            
            config_console.loop()
            
            # Restore original state
            self.parent_console.state.restore_state()
            _print("Exited configuration mode")
            _print(f"Restored state: {self.parent_console.state.full_prompt}")
        else:
            _print("No parent console available")


def main():
    """Demonstrate integrated state management."""
    
    # Create main console with state management
    console = Console("MainConsole", ">", "Welcome to State Management Demo")
    
    # Add state-aware commands
    state_cmd = StateAwareCommand("state", help="Show state information")
    nested_cmd = NestedStateCommand("nested", help="Enter nested console")
    config_cmd = ConfigCommand("config", help="Enter configuration mode")
    
    console.addChild(state_cmd)
    console.addChild(nested_cmd)
    console.addChild(config_cmd)
    
    # Start the console
    console.loop()


if __name__ == '__main__':
    main()