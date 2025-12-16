#!/usr/bin/env python3
"""
Visual Turing Machine Simulator
A simple Turing machine that increments a binary number by 1.

Example Machine: Binary Increment
- Input: Binary number on tape (e.g., "1011" = 11 in decimal)
- Output: Binary number + 1 (e.g., "1100" = 12 in decimal)
"""

import pygame
import sys
from typing import Dict, Tuple, List

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CELL_SIZE = 60
CELL_MARGIN = 5
FPS = 2  # Animation speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 255)
GREEN = (50, 205, 50)
RED = (255, 69, 69)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 255)
YELLOW = (255, 255, 150)


class TuringMachine:
    """
    A Turing Machine implementation for binary increment.
    
    States:
    - 'start': Initial state, moves to the rightmost digit
    - 'carry': Handles the carry operation (changes 1 to 0, moves left)
    - 'write1': Writes 1 and halts (no more carry needed)
    - 'halt': Final state
    
    Transition function format:
    (current_state, read_symbol) -> (new_state, write_symbol, direction)
    where direction: 'L' = Left, 'R' = Right, 'N' = No move
    """
    
    def __init__(self):
        # Tape and head position
        self.tape: List[str] = ['_', '1', '0', '1', '1', '_', '_', '_']
        self.head_position: int = 1  # Start at first digit
        self.current_state: str = 'start'
        
        # Transition table for binary increment
        # Format: (state, symbol) -> (new_state, write_symbol, direction)
        self.transitions: Dict[Tuple[str, str], Tuple[str, str, str]] = {
            # Start state: move right to find the rightmost digit
            ('start', '0'): ('start', '0', 'R'),
            ('start', '1'): ('start', '1', 'R'),
            ('start', '_'): ('carry', '_', 'L'),  # Found blank, go back to start carry
            
            # Carry state: handle carry operation
            ('carry', '0'): ('write1', '1', 'N'),  # 0 + carry = 1, done
            ('carry', '1'): ('carry', '0', 'L'),   # 1 + carry = 0, continue carry
            ('carry', '_'): ('write1', '1', 'N'),  # Blank + carry = 1 (overflow)
            
            # Write 1 and halt
            ('write1', '0'): ('halt', '1', 'N'),
            ('write1', '1'): ('halt', '1', 'N'),
            ('write1', '_'): ('halt', '1', 'N'),
        }
        
        self.halted = False
        self.step_count = 0
    
    def step(self) -> bool:
        """Execute one step of the Turing machine. Returns True if machine continues."""
        if self.halted or self.current_state == 'halt':
            self.halted = True
            return False
        
        # Read current symbol
        current_symbol = self.tape[self.head_position]
        
        # Get transition
        key = (self.current_state, current_symbol)
        if key not in self.transitions:
            self.halted = True
            return False
        
        new_state, write_symbol, direction = self.transitions[key]
        
        # Execute transition
        self.tape[self.head_position] = write_symbol
        self.current_state = new_state
        
        # Move head
        if direction == 'L':
            self.head_position = max(0, self.head_position - 1)
        elif direction == 'R':
            self.head_position = min(len(self.tape) - 1, self.head_position + 1)
            # Extend tape if needed
            if self.head_position >= len(self.tape) - 1:
                self.tape.append('_')
        
        self.step_count += 1
        
        return True
    
    def reset(self):
        """Reset the machine to initial state."""
        self.tape = ['_', '1', '0', '1', '1', '_', '_', '_']
        self.head_position = 1  # Start at first digit
        self.current_state = 'start'
        self.halted = False
        self.step_count = 0


class TuringMachineVisualizer:
    """Visualizes the Turing Machine execution."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Turing Machine - Binary Increment")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        self.machine = TuringMachine()
        self.running = True
        self.paused = False
        self.auto_run = True
    
    def draw_tape(self):
        """Draw the tape cells."""
        tape_start_x = 50
        tape_y = 250
        
        visible_cells = min(15, len(self.machine.tape))
        start_idx = max(0, self.machine.head_position - 7)
        end_idx = min(len(self.machine.tape), start_idx + visible_cells)
        
        for i in range(start_idx, end_idx):
            x = tape_start_x + (i - start_idx) * (CELL_SIZE + CELL_MARGIN)
            
            # Highlight current head position
            if i == self.machine.head_position:
                color = YELLOW
                pygame.draw.rect(self.screen, color, (x, tape_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, tape_y, CELL_SIZE, CELL_SIZE), 3)
            else:
                color = WHITE
                pygame.draw.rect(self.screen, color, (x, tape_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, tape_y, CELL_SIZE, CELL_SIZE), 2)
            
            # Draw symbol
            symbol = self.machine.tape[i]
            text = self.font.render(symbol, True, BLACK)
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, tape_y + CELL_SIZE // 2))
            self.screen.blit(text, text_rect)
            
            # Draw cell index
            idx_text = self.small_font.render(str(i), True, GRAY)
            idx_rect = idx_text.get_rect(center=(x + CELL_SIZE // 2, tape_y + CELL_SIZE + 20))
            self.screen.blit(idx_text, idx_rect)
    
    def draw_head(self):
        """Draw the read/write head indicator."""
        tape_start_x = 50
        tape_y = 250
        
        start_idx = max(0, self.machine.head_position - 7)
        visible_pos = self.machine.head_position - start_idx
        
        x = tape_start_x + visible_pos * (CELL_SIZE + CELL_MARGIN)
        
        # Draw arrow pointing to current cell
        arrow_points = [
            (x + CELL_SIZE // 2, tape_y - 30),
            (x + CELL_SIZE // 2 - 15, tape_y - 10),
            (x + CELL_SIZE // 2 + 15, tape_y - 10)
        ]
        pygame.draw.polygon(self.screen, RED, arrow_points)
        
        # Draw "HEAD" label
        head_text = self.small_font.render("HEAD", True, RED)
        head_rect = head_text.get_rect(center=(x + CELL_SIZE // 2, tape_y - 50))
        self.screen.blit(head_text, head_rect)
    
    def draw_state(self):
        """Draw current state information."""
        state_y = 400
        
        # Current state
        if self.machine.halted:
            state_color = RED
            state_text = f"State: {self.machine.current_state} (HALTED)"
        else:
            state_color = GREEN
            state_text = f"State: {self.machine.current_state}"
        
        text = self.font.render(state_text, True, state_color)
        self.screen.blit(text, (50, state_y))
        
        # Step count
        step_text = self.font.render(f"Steps: {self.machine.step_count}", True, BLACK)
        self.screen.blit(step_text, (50, state_y + 50))
        
        # Current symbol
        symbol = self.machine.tape[self.machine.head_position]
        symbol_text = self.font.render(f"Reading: '{symbol}'", True, BLUE)
        self.screen.blit(symbol_text, (50, state_y + 100))
    
    def draw_title(self):
        """Draw title and description."""
        title = self.title_font.render("Turing Machine Simulator", True, BLACK)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
        
        desc = self.small_font.render("Example: Binary Increment (Input: 1011 → Output: 1100)", True, GRAY)
        self.screen.blit(desc, (WINDOW_WIDTH // 2 - desc.get_width() // 2, 70))
    
    def draw_instructions(self):
        """Draw control instructions."""
        instructions = [
            "Controls:",
            "SPACE - Step forward",
            "R - Reset",
            "P - Pause/Resume auto-run",
            "Q - Quit"
        ]
        
        y_offset = 450
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, BLACK)
            self.screen.blit(text, (WINDOW_WIDTH - 300, y_offset + i * 30))
    
    def draw_transition_table(self):
        """Draw a simplified transition table."""
        table_title = self.small_font.render("State Transitions:", True, BLACK)
        self.screen.blit(table_title, (WINDOW_WIDTH - 550, 450))
        
        transitions_display = [
            "start + (0|1) → stay, move R",
            "start + _ → carry, move L",
            "carry + 0 → write 1, halt",
            "carry + 1 → write 0, move L",
        ]
        
        y_offset = 480
        for i, trans in enumerate(transitions_display):
            text = self.small_font.render(trans, True, GRAY)
            self.screen.blit(text, (WINDOW_WIDTH - 550, y_offset + i * 25))
    
    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if not self.machine.halted:
                        self.machine.step()
                elif event.key == pygame.K_r:
                    self.machine.reset()
                    self.paused = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                    self.auto_run = not self.auto_run
    
    def run(self):
        """Main loop."""
        while self.running:
            self.handle_events()
            
            # Auto-step if not paused
            if self.auto_run and not self.paused and not self.machine.halted:
                self.machine.step()
            
            # Draw everything
            self.screen.fill(LIGHT_BLUE)
            self.draw_title()
            self.draw_tape()
            self.draw_head()
            self.draw_state()
            self.draw_instructions()
            self.draw_transition_table()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    visualizer = TuringMachineVisualizer()
    visualizer.run()


if __name__ == "__main__":
    main()
