# Usage Guide

## Running the Simulator

### Interactive Visual Mode

To run the interactive visual simulator:

```bash
python turing_machine.py
```

This opens a window showing the Turing machine in action. The machine will automatically step through the computation, or you can control it manually.

### Keyboard Controls

- **SPACE**: Step forward one instruction at a time
- **P**: Pause/Resume automatic execution
- **R**: Reset the machine to its initial state
- **Q**: Quit the application

## Understanding the Visualization

### Visual Elements

1. **Tape Cells**: White boxes containing symbols (0, 1, or _ for blank)
2. **Yellow Highlighted Cell**: Current position of the read/write head
3. **Red Arrow (HEAD)**: Points to the cell being read/written
4. **State Display**: Shows the current state in green (or red when halted)
5. **Step Counter**: Number of operations performed
6. **Reading Display**: Current symbol being read from the tape

### Machine States

The binary increment machine uses four states:

- **start**: Initial state; moves right to find the end of the number
- **carry**: Propagates the carry by changing 1→0 and moving left
- **write1**: Writes a 1 to complete the increment
- **halt**: Final state; machine has stopped

## Example Execution

### Initial State
```
Tape:  _ 1 0 1 1 _ _ _
       └─┴─┴─┴─┴─┴─┴─┴─
Position: 1 (at first '1')
State: start
Binary number: 1011 (11 in decimal)
```

### Step-by-Step Execution

1. **Steps 1-4**: Move right through the digits until finding a blank
2. **Step 5**: Enter carry state, move left to the last digit
3. **Steps 6-7**: Change 1s to 0s, continue moving left (carry propagation)
4. **Step 8**: Find a 0, change it to 1, enter write1 state
5. **Step 9**: Enter halt state

### Final State
```
Tape:  _ 1 1 0 0 _ _ _
       └─┴─┴─┴─┴─┴─┴─┴─
State: halt
Binary number: 1100 (12 in decimal)
Result: 11 + 1 = 12 ✓
```

## Testing Without GUI

To test the Turing machine logic without the graphical interface:

```bash
python test_turing_machine.py
```

This runs automated tests that verify the machine correctly increments various binary numbers.

## Creating Screenshots

To generate screenshots of the simulator in different states:

```bash
python demo_screenshot.py
```

This creates PNG images in `/tmp/` showing the initial state, intermediate steps, and final state.

## Customizing the Machine

### Changing the Initial Tape

Edit the `__init__` method in the `TuringMachine` class:

```python
def __init__(self):
    # Change this line to set a different initial binary number
    self.tape = ['_', '1', '0', '1', '1', '_', '_', '_']
    #                    ^ ^ ^ ^  = 1011 in binary (11 in decimal)
```

### Modifying the Transition Table

The transition rules are defined in the `transitions` dictionary:

```python
self.transitions = {
    # Format: (current_state, read_symbol) -> (new_state, write_symbol, direction)
    ('start', '0'): ('start', '0', 'R'),  # In start state, if reading 0: stay in start, write 0, move right
    # Add or modify rules here...
}
```

Where:
- `current_state`: State before the transition
- `read_symbol`: Symbol currently under the head
- `new_state`: State after the transition
- `write_symbol`: Symbol to write to the current cell
- `direction`: 'L' (left), 'R' (right), or 'N' (no move)

## Troubleshooting

### "Module pygame not found"

Install pygame:
```bash
pip install pygame
```

### Display Issues on Headless Systems

If you're running on a server without a display, use the test script instead:
```bash
python test_turing_machine.py
```

Or use the demo screenshot script which runs in headless mode:
```bash
python demo_screenshot.py
```

### ALSA Audio Warnings

Warnings like "ALSA lib confmisc.c..." can be safely ignored. They appear because pygame initializes audio, but the system doesn't have audio hardware configured. The simulation works correctly despite these warnings.

## Additional Resources

For more information about Turing machines:
- [Wikipedia: Turing Machine](https://en.wikipedia.org/wiki/Turing_machine)
- [Stanford Encyclopedia: Turing Machines](https://plato.stanford.edu/entries/turing-machine/)
- [Visual Introduction to Turing Machines](https://turingmachine.io/)
