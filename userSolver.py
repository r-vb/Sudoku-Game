import tkinter as tk
from tkinter import messagebox, Toplevel
import random
import copy

# Initialize the main window
root = tk.Tk()
root.title("6x6 Sudoku Solver")
root.geometry("500x750")
root.configure(bg="#F4F5F7")

# Colors and Fonts
PRIMARY_COLOR = "#2D3748"  # Dark blue for text
SECONDARY_COLOR = "#4A90E2"  # Accent blue
BACKGROUND_COLOR = "#FFFFFF"  # White background
GRID_COLOR = "#E2E8F0"  # Light border for grid
HIGHLIGHT_COLOR = "#EDF2F7"  # Subtle highlight
ERROR_COLOR = "#FFB3B3"  # Light red for errors

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_TEXT = ("Segoe UI", 12)
FONT_ENTRY = ("Segoe UI", 18, "bold")

# Heading Title
title_label = tk.Label(root, text="6x6 Sudoku Solver", font=FONT_TITLE, bg="#F4F5F7", fg=PRIMARY_COLOR)
title_label.pack(pady=10)

def create_empty_grid():
    return [[0 for _ in range(6)] for _ in range(6)]

# Game grids and data
grid = create_empty_grid()
solved_grid = create_empty_grid()
entries = []

# Utility functions
def is_valid_move(grid, row, col, num):
    """Check if placing 'num' at grid[row][col] is valid."""
    for i in range(6):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    box_row, box_col = row // 2 * 2, col // 3 * 3
    for i in range(box_row, box_row + 2):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve_sudoku(grid):
    """Solve the Sudoku grid using backtracking."""
    for row in range(6):
        for col in range(6):
            if grid[row][col] == 0:
                for num in range(1, 7):
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def copy_grid(original):
    return [row[:] for row in original]

def validate_grid(grid):
    """Validate grid for rule violations."""
    errors = []
    for row in range(6):
        for col in range(6):
            num = grid[row][col]
            if num != 0:
                grid[row][col] = 0
                if not is_valid_move(grid, row, col, num):
                    errors.append((row, col))
                grid[row][col] = num
    return errors

def highlight_errors(errors):
    """Highlight cells that violate rules."""
    for row in range(6):
        for col in range(6):
            bg_color = BACKGROUND_COLOR if (row // 2 + col // 3) % 2 == 0 else HIGHLIGHT_COLOR
            if (row, col) in errors:
                entries[row][col].config(bg=ERROR_COLOR)
            else:
                entries[row][col].config(bg=bg_color)

def clear_errors():
    """Clear any error highlights."""
    for row in range(6):
        for col in range(6):
            bg_color = BACKGROUND_COLOR if (row // 2 + col // 3) % 2 == 0 else HIGHLIGHT_COLOR
            entries[row][col].config(bg=bg_color)

# Hint System
def provide_hint():
    """Provide a hint by suggesting a correct placement."""
    for row in range(6):
        for col in range(6):
            if grid[row][col] == 0:
                for num in range(1, 7):
                    if is_valid_move(grid, row, col, num):
                        entries[row][col].delete(0, tk.END)
                        entries[row][col].insert(0, num)
                        return
    messagebox.showinfo("No Hint", "No hints available.")

# Puzzle Generation
def generate_puzzle(difficulty):
    """Generate a random puzzle with specified difficulty."""
    global grid, solved_grid
    grid = create_empty_grid()
    solve_sudoku(grid)
    solved_grid = copy_grid(grid)

    attempts = 20 if difficulty == "Easy" else 30 if difficulty == "Medium" else 36

    while attempts > 0:
        row, col = random.randint(0, 5), random.randint(0, 5)
        while grid[row][col] == 0:
            row, col = random.randint(0, 5), random.randint(0, 5)
        grid[row][col] = 0
        attempts -= 1

    display_puzzle(grid)

def display_puzzle(grid):
    """Display a given grid in the UI."""
    clear_errors()
    for row in range(6):
        for col in range(6):
            entries[row][col].config(state="normal")
            entries[row][col].delete(0, tk.END)
            if grid[row][col] != 0:
                entries[row][col].insert(0, grid[row][col])
                entries[row][col].config(state="disabled")

def show_solution():
    """Display the solution to the puzzle."""
    display_puzzle(solved_grid)
    messagebox.showinfo("Solution", "Here is the solution to the puzzle.")

# GUI Setup
frame = tk.Frame(root, bg=GRID_COLOR, bd=2)
frame.pack(pady=20)

for i in range(6):
    row_entries = []
    for j in range(6):
        bg_color = BACKGROUND_COLOR if (i // 2 + j // 3) % 2 == 0 else HIGHLIGHT_COLOR
        entry = tk.Entry(frame, width=2, font=FONT_ENTRY, justify="center", bg=bg_color, relief="flat")
        entry.grid(row=i, column=j, ipadx=10, ipady=10, padx=2, pady=2)
        row_entries.append(entry)
    entries.append(row_entries)

def check_for_errors():
    for row in range(6):
        for col in range(6):
            grid[row][col] = int(entries[row][col].get()) if entries[row][col].get() else 0
    errors = validate_grid(grid)
    if errors:
        highlight_errors(errors)
        messagebox.showerror("Rule Violation", "There are errors in the grid. Please fix them.")
    else:
        clear_errors()
        messagebox.showinfo("Valid Grid", "The grid is valid!")

# Buttons
button_frame = tk.Frame(root, bg="#F4F5F7")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Check Errors", command=check_for_errors, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).pack(side="left", padx=5)
tk.Button(button_frame, text="Hint", command=provide_hint, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).pack(side="left", padx=5)
tk.Button(button_frame, text="Show Solution", command=show_solution, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).pack(side="left", padx=5)

def start_game(difficulty):
    generate_puzzle(difficulty)

menu_frame = tk.Frame(root, bg="#F4F5F7")
menu_frame.pack()

tk.Button(menu_frame, text="Easy", command=lambda: start_game("Easy"), bg=PRIMARY_COLOR, fg="white", font=FONT_TEXT).pack(side="left", padx=5)
tk.Button(menu_frame, text="Medium", command=lambda: start_game("Medium"), bg=PRIMARY_COLOR, fg="white", font=FONT_TEXT).pack(side="left", padx=5)
tk.Button(menu_frame, text="Difficult", command=lambda: start_game("Difficult"), bg=PRIMARY_COLOR, fg="white", font=FONT_TEXT).pack(side="left", padx=5)

root.mainloop()


'''
Add-On Requirements:
>> User(Numbers Placer) Machine(Solver)
   Machine should be able to notify player about errors / violation of rules precisely.
   Once violations are notified, the state of the game should not be resetted.
   Machine should be able to provide hints to the player about the correct placement of numbers.
>> Machine(Numbers Placer) User(Solver)
   Machine should be able to generate random puzzles for the player to solve.
   Machine should be able to provide the solution to the puzzle once the player has solved it.
   User can select the difficlty level. ex. easy or medium or difficult
'''
