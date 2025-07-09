#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ishell.state import ConsoleState
from ishell.console import Console
from ishell.command import Command
from ishell.utils import _print


class StateAwareConsole(Console):
    """Console that uses ConsoleState for state management."""
    
    def __init__(self, prompt="Prompt", prompt_delim=">", welcome_message=None):
        super().__init__(prompt, prompt_delim, welcome_message)
        # Create state manager
        self.state = ConsoleState(prompt, prompt_delim, welcome_message)
        
    def loop(self):
        """Override loop to use state management."""
        import readline
        import sys
        from builtins import input
        
        previous_completer = readline.get_completer()
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.walk)
        
        # Use state for prompt management
        prompt = self.state.get_display_prompt()
        
        # Display welcome message using state
        self.state.display_welcome()
        
        while True:
            try:
                sys.stdout.write("\r")
                if self.state.should_exit():
                    break
                sys.stdout.write("\033[K")
                input_ = input(prompt)
                if not input_.strip():
                    self.print_childs_help()
                elif input_ in ('quit', 'exit'):
                    break
                else:
                    self.walk_and_run(input_)
            except (KeyboardInterrupt, EOFError):
                print("exit")
                break
            except Exception:
                import traceback
                print(traceback.format_exc())
                sys.exit(1)
        
        readline.set_completer(previous_completer)


class NestedCommand(Command):
    """Example command that demonstrates state management."""
    
    def run(self, line):
        # This would be integrated with the console's state
        _print("This command would use console state management")
        _print("In a real implementation, it would access console.state")


def demonstrate_state_usage():
    """Demonstrate ConsoleState usage patterns."""
    
    # Create a state instance
    state = ConsoleState("RouterA", "#", "Welcome to RouterA")
    
    print("Initial state:")
    print(f"  Prompt: {state.full_prompt}")
    print(f"  Welcome: {state.welcome_message}")
    
    # Demonstrate temporary state changes
    print("\nDemonstrating temporary state changes:")
    with state.temporary_state("ConfigMode", ">", "Entered config mode"):
        print(f"  Inside context: {state.full_prompt}")
        print(f"  Welcome: {state.welcome_message}")
    
    print(f"  Outside context: {state.full_prompt}")
    
    # Demonstrate state saving/restoration
    print("\nDemonstrating state save/restore:")
    state.save_state()
    state.set_prompt("InterfaceMode", "$")
    print(f"  Modified state: {state.full_prompt}")
    
    state.restore_state()
    print(f"  Restored state: {state.full_prompt}")
    
    # Demonstrate exit management
    print("\nDemonstrating exit management:")
    print(f"  Should exit: {state.should_exit()}")
    state.set_exit(True)
    print(f"  Should exit: {state.should_exit()}")


def main():
    """Demonstrate ConsoleState usage."""
    
    print("=== ConsoleState Demonstration ===\n")
    
    # Show basic state usage
    demonstrate_state_usage()
    
    print("\n=== Integration Example ===")
    print("This shows how ConsoleState would be integrated into the existing codebase:")
    print("- Replace global _current_prompt with ConsoleState instances")
    print("- Use context managers for temporary state changes")
    print("- Provide better state encapsulation and management")
    print("- Enable easier testing and debugging of state changes")


if __name__ == '__main__':
    main()