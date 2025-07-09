# ConsoleState Integration Guide

## Overview

The `ConsoleState` class provides a comprehensive solution for managing console state in the ishell library. It eliminates the need for global state variables and provides better encapsulation, testing, and debugging capabilities.

## Key Features

### 1. State Management
- **Encapsulated State**: All console state (prompt, delimiter, welcome message, exit flag) is managed in one place
- **No Global Variables**: Eliminates the need for `ishell._current_prompt` global variable
- **Type Safety**: Provides clear interfaces for state manipulation

### 2. Context Management
- **Temporary State Changes**: Use context managers for temporary state modifications
- **Automatic Restoration**: State is automatically restored when exiting context
- **Partial Changes**: Modify only specific state properties as needed

### 3. State Persistence
- **Save/Restore**: Save current state and restore it later
- **State History**: Track state changes for debugging
- **Predictable Behavior**: Clear state transitions

## Usage Examples

### Basic Usage

```python
from ishell.state import ConsoleState

# Create a new state
state = ConsoleState("RouterA", "#", "Welcome to RouterA")

# Access state properties
print(state.full_prompt)  # "RouterA#"
print(state.welcome_message)  # "Welcome to RouterA"
```

### Temporary State Changes

```python
# Use context manager for temporary changes
with state.temporary_state("ConfigMode", ">", "Entered config mode"):
    print(state.full_prompt)  # "ConfigMode>"
    # Do work in this context
    
# State is automatically restored
print(state.full_prompt)  # "RouterA#"
```

### State Persistence

```python
# Save current state
state.save_state()

# Modify state
state.set_prompt("InterfaceMode", "$")

# Restore original state
state.restore_state()
```

### Partial State Changes

```python
# Change only the prompt
with state.temporary_state(prompt="NewPrompt"):
    print(state.full_prompt)  # "NewPrompt#"
    
# Change only the delimiter
with state.temporary_state(prompt_delim="!"):
    print(state.full_prompt)  # "RouterA!"
```

## Integration with Existing Codebase

### Current Issues

1. **Global State**: `ishell._current_prompt` is used globally
2. **Scattered Logic**: State management is spread across multiple files
3. **Hard to Test**: Global state makes testing difficult
4. **No Context Management**: No way to temporarily change state

### Proposed Integration

#### 1. Update Console Class

```python
# In console.py
from ishell.state import ConsoleState

class Console(object):
    def __init__(self, prompt="Prompt", prompt_delim=">", welcome_message=None):
        self.childs = {}
        # Replace individual state properties with ConsoleState
        self.state = ConsoleState(prompt, prompt_delim, welcome_message)
        self._exit = False

    def loop(self):
        # Use state for prompt management
        prompt = self.state.get_display_prompt()
        
        # Display welcome using state
        self.state.display_welcome()
        
        # Rest of loop implementation...
```

#### 2. Update Command Class

```python
# In command.py
class Command(Console):
    def __init__(self, name, help='No help provided', dynamic_args=False):
        Console.__init__(self)
        self.name = name
        self.childs = {}
        self.dynamic_args = dynamic_args
        self.help = help
        
    def run(self, line):
        # Commands can access console state through self.state
        if hasattr(self, 'parent_console'):
            console_state = self.parent_console.state
            # Use console_state for state management
```

#### 3. Update Utils

```python
# In utils.py
def _print(msg):
    line_buffer = readline.get_line_buffer()
    sys.stdout.write("\r")
    sys.stdout.write("\033[K")
    sys.stdout.write(str(msg))
    
    # Use state instead of global variable
    if hasattr(ishell, '_current_state'):
        prompt = ishell._current_state.get_display_prompt()
    else:
        prompt = "Prompt> "
        
    sys.stdout.write("\n%s" % prompt)
    if line_buffer:
        sys.stdout.write(" %s" % line_buffer)
    sys.stdout.flush()
```

## Benefits

### 1. Better Encapsulation
- State is managed in one place
- Clear interfaces for state manipulation
- No more global variables

### 2. Improved Testing
- State can be easily mocked
- Context managers provide predictable behavior
- State changes are explicit and testable

### 3. Enhanced Debugging
- State transitions are clear and traceable
- Context managers provide automatic cleanup
- State history can be logged

### 4. Better Maintainability
- Clear separation of concerns
- Easier to add new state properties
- More predictable behavior

## Migration Strategy

### Phase 1: Add ConsoleState
- ✅ Create ConsoleState class
- ✅ Add comprehensive tests
- ✅ Create usage examples

### Phase 2: Integrate with Console
- Update Console class to use ConsoleState
- Maintain backward compatibility
- Update tests

### Phase 3: Update Commands
- Modify Command class to access state
- Update existing commands to use new state management
- Update examples

### Phase 4: Remove Global State
- Remove `ishell._current_prompt`
- Update utils.py to use state management
- Final cleanup

## Testing

The ConsoleState class includes comprehensive tests covering:
- Basic state creation and access
- Temporary state changes
- State persistence (save/restore)
- Context manager functionality
- Edge cases and error conditions

Run tests with:
```bash
python3 -m unittest tests.test_state -v
```

## Conclusion

The ConsoleState class provides a solid foundation for improving state management in the ishell library. It eliminates global state dependencies, provides better encapsulation, and enables more predictable and testable code. The integration can be done gradually while maintaining backward compatibility.