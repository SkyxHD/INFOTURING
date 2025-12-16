#!/usr/bin/env python3
"""
Demo script that runs the Turing machine and takes screenshots
"""

import sys
import os

# Set display for headless mode
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Import pygame after setting display
import pygame

# Import TuringMachine from main module
from turing_machine import TuringMachine

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CELL_SIZE = 60
CELL_MARGIN = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 255)
GREEN = (50, 205, 50)
RED = (255, 69, 69)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 255)
YELLOW = (255, 255, 150)


def draw_visualization(screen, machine, step_num):
    """Draw the complete visualization."""
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)
    
    # Background
    screen.fill(LIGHT_BLUE)
    
    # Title
    title = title_font.render("Turing Machine Simulator", True, BLACK)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
    
    desc = small_font.render("Example: Binary Increment (Input: 1011 → Output: 1100)", True, GRAY)
    screen.blit(desc, (WINDOW_WIDTH // 2 - desc.get_width() // 2, 70))
    
    # Draw tape
    tape_start_x = 50
    tape_y = 250
    
    visible_cells = min(15, len(machine.tape))
    start_idx = max(0, machine.head_position - 7)
    end_idx = min(len(machine.tape), start_idx + visible_cells)
    
    for i in range(start_idx, end_idx):
        x = tape_start_x + (i - start_idx) * (CELL_SIZE + CELL_MARGIN)
        
        if i == machine.head_position:
            color = YELLOW
            pygame.draw.rect(screen, color, (x, tape_y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, tape_y, CELL_SIZE, CELL_SIZE), 3)
        else:
            color = WHITE
            pygame.draw.rect(screen, color, (x, tape_y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, tape_y, CELL_SIZE, CELL_SIZE), 2)
        
        symbol = machine.tape[i]
        text = font.render(symbol, True, BLACK)
        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, tape_y + CELL_SIZE // 2))
        screen.blit(text, text_rect)
        
        idx_text = small_font.render(str(i), True, GRAY)
        idx_rect = idx_text.get_rect(center=(x + CELL_SIZE // 2, tape_y + CELL_SIZE + 20))
        screen.blit(idx_text, idx_rect)
    
    # Draw head arrow
    visible_pos = machine.head_position - start_idx
    x = tape_start_x + visible_pos * (CELL_SIZE + CELL_MARGIN)
    
    arrow_points = [
        (x + CELL_SIZE // 2, tape_y - 30),
        (x + CELL_SIZE // 2 - 15, tape_y - 10),
        (x + CELL_SIZE // 2 + 15, tape_y - 10)
    ]
    pygame.draw.polygon(screen, RED, arrow_points)
    
    head_text = small_font.render("HEAD", True, RED)
    head_rect = head_text.get_rect(center=(x + CELL_SIZE // 2, tape_y - 50))
    screen.blit(head_text, head_rect)
    
    # Draw state
    state_y = 400
    
    if machine.halted:
        state_color = RED
        state_text = f"State: {machine.current_state} (HALTED)"
    else:
        state_color = GREEN
        state_text = f"State: {machine.current_state}"
    
    text = font.render(state_text, True, state_color)
    screen.blit(text, (50, state_y))
    
    step_text = font.render(f"Steps: {machine.step_count}", True, BLACK)
    screen.blit(step_text, (50, state_y + 50))
    
    symbol = machine.tape[machine.head_position]
    symbol_text = font.render(f"Reading: '{symbol}'", True, BLUE)
    screen.blit(symbol_text, (50, state_y + 100))
    
    # Instructions
    instructions = [
        "Controls:",
        "SPACE - Step forward",
        "R - Reset",
        "P - Pause/Resume",
        "Q - Quit"
    ]
    
    y_offset = 450
    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, BLACK)
        screen.blit(text, (WINDOW_WIDTH - 300, y_offset + i * 30))
    
    # Transition table
    table_title = small_font.render("State Transitions:", True, BLACK)
    screen.blit(table_title, (WINDOW_WIDTH - 550, 450))
    
    transitions_display = [
        "start + (0|1) → stay, move R",
        "start + _ → carry, move L",
        "carry + 0 → write 1, halt",
        "carry + 1 → write 0, move L",
    ]
    
    y_offset = 480
    for i, trans in enumerate(transitions_display):
        text = small_font.render(trans, True, GRAY)
        screen.blit(text, (WINDOW_WIDTH - 550, y_offset + i * 25))


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Turing Machine - Binary Increment")
    
    machine = TuringMachine()
    
    # Take screenshots at different stages
    screenshots = []
    
    # Initial state
    draw_visualization(screen, machine, 0)
    pygame.image.save(screen, "/tmp/tm_initial.png")
    print("✓ Saved initial state screenshot")
    screenshots.append("Initial state (Input: 1011)")
    
    # Step through a few times
    for i in range(4):
        machine.step()
        draw_visualization(screen, machine, i + 1)
        pygame.image.save(screen, f"/tmp/tm_step{i+1}.png")
        print(f"✓ Saved step {i+1} screenshot (State: {machine.current_state})")
        screenshots.append(f"Step {i+1} (State: {machine.current_state})")
    
    # Run until halt
    step_num = 5
    while machine.step() and step_num < 20:
        step_num += 1
    
    # Final state
    draw_visualization(screen, machine, step_num)
    pygame.image.save(screen, "/tmp/tm_final.png")
    print(f"✓ Saved final state screenshot (Output: {''.join(machine.tape[1:5])})")
    screenshots.append(f"Final state (Output: {''.join(machine.tape[1:5])})")
    
    print("\nScreenshots saved:")
    for ss in screenshots:
        print(f"  - {ss}")
    
    pygame.quit()


if __name__ == "__main__":
    main()
