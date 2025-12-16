#!/usr/bin/env python3
"""
Test script for Turing Machine logic (without GUI)
"""

import sys

# Import the TuringMachine class from the main module
from turing_machine import TuringMachine


def get_binary_number(tape):
    """Extract the binary number from the tape."""
    # Find first and last non-blank symbols
    result = []
    found_digit = False
    for symbol in tape:
        if symbol in ['0', '1']:
            found_digit = True
            result.append(symbol)
        elif found_digit and symbol == '_':
            break
    return ''.join(result)


def test_binary_increment():
    """Test the binary increment Turing machine."""
    print("Testing Turing Machine - Binary Increment")
    print("=" * 50)
    
    machine = TuringMachine()
    
    # Get initial number
    initial = get_binary_number(machine.tape)
    initial_decimal = int(initial, 2) if initial else 0
    print(f"Initial tape: {' '.join(machine.tape[:8])}")
    print(f"Initial binary: {initial} (decimal: {initial_decimal})")
    print()
    
    # Run the machine
    print("Executing steps...")
    step = 0
    while machine.step():
        step += 1
        print(f"Step {step}: State={machine.current_state}, "
              f"Pos={machine.head_position}, "
              f"Symbol={machine.tape[machine.head_position]}, "
              f"Tape={' '.join(machine.tape[:8])}")
        
        if step > 100:  # Safety limit
            print("ERROR: Too many steps! Machine may be in infinite loop.")
            sys.exit(1)
    
    print()
    print(f"Machine halted after {machine.step_count} steps")
    
    # Get final number
    final = get_binary_number(machine.tape)
    final_decimal = int(final, 2) if final else 0
    print(f"Final tape: {' '.join(machine.tape[:8])}")
    print(f"Final binary: {final} (decimal: {final_decimal})")
    print()
    
    # Verify correctness
    expected_decimal = initial_decimal + 1
    if final_decimal == expected_decimal:
        print(f"✓ SUCCESS: {initial_decimal} + 1 = {final_decimal}")
        return True
    else:
        print(f"✗ FAILED: Expected {expected_decimal}, got {final_decimal}")
        return False


def test_multiple_cases():
    """Test multiple binary numbers."""
    print("\nTesting Multiple Cases")
    print("=" * 50)
    
    test_cases = [
        ['_', '1', '_', '_', '_'],           # 1 -> 10
        ['_', '1', '0', '_', '_', '_'],      # 10 -> 11
        ['_', '1', '1', '_', '_', '_'],      # 11 -> 100
        ['_', '1', '1', '1', '_', '_', '_'], # 111 -> 1000
    ]
    
    all_passed = True
    
    for i, initial_tape in enumerate(test_cases):
        machine = TuringMachine()
        machine.tape = initial_tape.copy()
        
        initial = get_binary_number(machine.tape)
        initial_decimal = int(initial, 2) if initial else 0
        
        while machine.step() and machine.step_count < 100:
            pass
        
        final = get_binary_number(machine.tape)
        final_decimal = int(final, 2) if final else 0
        
        expected = initial_decimal + 1
        passed = (final_decimal == expected)
        all_passed = all_passed and passed
        
        status = "✓" if passed else "✗"
        print(f"{status} Test {i+1}: {initial} ({initial_decimal}) -> {final} ({final_decimal}), "
              f"Expected: {expected}")
    
    print()
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    
    return all_passed


if __name__ == "__main__":
    success1 = test_binary_increment()
    success2 = test_multiple_cases()
    
    if success1 and success2:
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("The Turing machine is working correctly.")
        sys.exit(0)
    else:
        sys.exit(1)
