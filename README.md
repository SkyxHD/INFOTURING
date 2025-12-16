# INFOTURING

A visual simulation of a Turing machine with an interactive interface.

## Overview

This project implements a visual Turing machine simulator that demonstrates how a Turing machine works. The example machine performs **binary increment** - it takes a binary number as input and increments it by 1.

### Example Machine: Binary Increment

- **Input**: `1011` (11 in decimal)
- **Output**: `1100` (12 in decimal)

#### Visual Example

```
Initial:  _ [1] 0  1  1  _  _  _
             ↑
          (HEAD, State: start)

Final:    _  1 [1] 0  0  _  _  _
                ↑
          (HEAD, State: halt)

Result: 1011 + 1 = 1100 (11 + 1 = 12) ✓
```

The machine uses the following states:
- `start`: Moves to the rightmost digit of the binary number
- `carry`: Handles the carry operation (changes 1→0, moves left)
- `write1`: Writes 1 when carry is resolved
- `halt`: Final state

## Screenshots

### Initial State
![Initial State](https://github.com/user-attachments/assets/4d28500e-fee8-49c2-9971-44aeb6e90096)

*Machine at start with input 1011 (11 in decimal)*

### Final State
![Final State](https://github.com/user-attachments/assets/cba51a76-637e-40e9-9fa9-fe26464c09cf)

*Machine halted with output 1100 (12 in decimal) - successfully incremented!*

## Features

- 🎨 **Visual representation** of the tape, head, and current state
- ⏯️ **Interactive controls** for stepping through execution
- 📊 **Live display** of state transitions and step count
- 🔄 **Reset functionality** to restart the simulation
- 📖 **Built-in transition table** for understanding the logic

## Requirements

- Python 3.7 or higher
- Pygame 2.5.0 or higher

## Installation

1. Clone this repository:
```bash
git clone https://github.com/SkyxHD/INFOTURING.git
cd INFOTURING
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Turing machine simulator:

```bash
python turing_machine.py
```

### Controls

- **SPACE**: Step forward one instruction
- **R**: Reset the machine to initial state
- **P**: Pause/Resume automatic execution
- **Q**: Quit the application

## How It Works

The Turing machine operates on a tape divided into cells, each containing a symbol. A read/write head moves along the tape, reading symbols and writing new ones based on the current state and transition rules.

### Transition Rules

The binary increment machine follows these rules:

1. **Start state**: Move right until finding a blank space (end of number)
2. **Carry state**: Move left, changing 1s to 0s (carry propagation)
3. **Write 1**: When encountering a 0 or blank, write 1 and halt

### Visual Elements

- **Yellow cell**: Current head position
- **Red arrow**: Read/write head indicator
- **Green text**: Active state
- **Red text**: Halted state
- **Step counter**: Number of operations performed

## Understanding Turing Machines

A Turing machine is a mathematical model of computation that consists of:
- An infinite tape divided into cells
- A head that can read and write symbols
- A state register that stores the current state
- A finite table of instructions (transition function)

Despite its simplicity, a Turing machine can simulate any computer algorithm, making it a fundamental concept in computer science and the theory of computation.

## License

This project is open source and available for educational purposes.