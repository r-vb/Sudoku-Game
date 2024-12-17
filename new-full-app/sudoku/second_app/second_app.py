import tkinter as tk
import subprocess
from tkinter import messagebox, Toplevel
import random
import copy
import time

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y position of the window to center it
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the position of the window
    window.geometry(f'{width}x{height}+{x}+{y}')

def restart_app():
    # Restart the main script after closing the current window
    root.destroy()  # Close the current window
    subprocess.run(["python", "main.py"])

'''Initialize the main window'''
root = tk.Tk()
root.title("6x6 Sudoku: Solve it, Rock it!")
root.configure(bg="#F4F5F7")

width = 500
height = 770

# Center the window on the screen
center_window(root, width, height)

'''Colors and Fonts'''
PRIMARY_COLOR = "#2D3748"  # Dark blue for text
SECONDARY_COLOR = "#4A90E2"  # Accent blue
BACKGROUND_COLOR = "#FFFFFF"  # White background
GRID_COLOR = "#E2E8F0"  # Light border for grid
HIGHLIGHT_COLOR = "#EDF2F7"  # Subtle highlight
ERROR_COLOR = "#FFB3B3"  # Light red for errors

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_TEXT = ("Segoe UI", 12)
FONT_ENTRY = ("Segoe UI", 18, "bold")

'''Heading Title'''
title_label = tk.Label(root, text="6x6 Sudoku", font=FONT_TITLE, bg="#F4F5F7", fg=PRIMARY_COLOR)
title_label.pack(pady=10)

def create_empty_grid():
    return [[0 for _ in range(6)] for _ in range(6)]

'''Game grids and data'''
grid = create_empty_grid()
solved_grid = create_empty_grid()
entries = []

'''Timer variables'''
start_time = None
elapsed_time = 0
timer_running = False

'''Utility functions'''
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

'''Hint System'''
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

'''Puzzle Generation'''
def generate_puzzle(difficulty):
    """Generate a random puzzle with specified difficulty."""
    global grid, solved_grid
    grid = create_empty_grid()
    solve_sudoku(grid)  # Solve the grid first to generate a valid solution
    solved_grid = copy_grid(grid)  # Keep a copy of the solved grid

    # Set number of attempts based on difficulty
    if difficulty == "Easy":
        attempts = 18
    elif difficulty == "Medium":
        attempts = 27
    elif difficulty == "Difficult":
        attempts = 31
    else:
        attempts = 18  # Default to Easy if an invalid difficulty is provided

    # Remove numbers to create the puzzle
    while attempts > 0:
        row, col = random.randint(0, 5), random.randint(0, 5)

        # Skip cells that are already empty
        while grid[row][col] == 0:
            row, col = random.randint(0, 5), random.randint(0, 5)

        # Remove the number from the grid (make the cell empty)
        grid[row][col] = 0
        attempts -= 1

    display_puzzle(grid)  # Display the puzzle grid


def display_puzzle(grid):
    """Display the puzzle grid on the UI."""
    clear_errors()  # Clear any previous error highlights
    for row in range(6):
        for col in range(6):
            entries[row][col].config(state="normal")  # Make the cell editable
            entries[row][col].delete(0, tk.END)  # Clear the current entry
            if grid[row][col] != 0:
                entries[row][col].insert(0, grid[row][col])  # Insert the pre-filled number
                entries[row][col].config(state="disabled")  # Disable pre-filled cell
            else:
                entries[row][col].config(state="normal")  # Keep empty cells editable

def show_solution():
    """Display the solution to the puzzle."""
    display_puzzle(solved_grid)
    messagebox.showinfo("Solution", "Here is the solution to the puzzle.")

def start_pause_reset_timer(action):
    global start_time, elapsed_time, timer_running

    if action == "start":
        if not timer_running:
            start_time = time.time() - elapsed_time
            timer_running = True
            update_timer()
    elif action == "pause":
        if timer_running:
            elapsed_time = time.time() - start_time
            timer_running = False
    elif action == "reset":
        elapsed_time = 0
        start_time = None
        timer_running = False
        timer_label.config(text="Time: 00:00")

def update_timer():
    if timer_running:
        elapsed_time = time.time() - start_time
        formatted_time = format_time(elapsed_time)
        timer_label.config(text=f"Time: {formatted_time}")
        root.after(100, update_timer)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

'''GUI Setup'''
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

'''Timer Label'''
timer_label = tk.Label(root, text="Time: 00:00", font=FONT_TEXT, bg="#F4F5F7", fg=PRIMARY_COLOR)
timer_label.pack(pady=10)

'''Define the function to check for errors'''
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

# Instructions Button
def show_instructions():
    """Display Sudoku rules and instructions in a pop-up window."""
    instructions_window = Toplevel(root)
    instructions_window.title("Instructions")
    instructions_window.geometry("500x400")
    instructions_window.configure(bg="#F4F5F7")

    instructions_text = (
        "Welcome to the 6x6 Sudoku Solver!\n\n"
        "Game Rules:\n"
        "1. Each row must contain the numbers 1-6 without repetition.\n"
        "2. Each column must contain the numbers 1-6 without repetition.\n"
        "3. Each 2x3 sub-grid must also contain the numbers 1-6 without repetition.\n\n"
        "How to Use:\n"
        "1. Enter the known numbers (1-6) in the grid.\n"
        "2. Leave empty cells blank or enter 0.\n"
        "3. Click 'Solve' to find the solution.\n\n"
        "Enjoy solving your puzzle!"
    )

    tk.Label(
        instructions_window,
        text=instructions_text,
        font=FONT_TEXT,
        justify="left",
        wraplength=400,
        bg="#F4F5F7",
        fg=PRIMARY_COLOR
    ).pack(padx=20, pady=20)

'''Buttons'''
button_frame = tk.Frame(root, bg="#F4F5F7")
button_frame.pack(pady=10)

'''(Difficulty Selection)'''
tk.Button(button_frame, text="Easy", command=lambda: generate_puzzle("Easy"), bg=PRIMARY_COLOR, fg="white", font=FONT_TEXT).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
tk.Button(button_frame, text="Medium", command=lambda: generate_puzzle("Medium"), bg=PRIMARY_COLOR, fg="white", font=FONT_TEXT).grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
tk.Button(button_frame, text="Difficult", command=lambda: generate_puzzle("Difficult"), bg=PRIMARY_COLOR, fg="white", font=FONT_TEXT).grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

'''(Timer Options)'''
tk.Button(button_frame, text="Strt/Rsm Timer", command=lambda: start_pause_reset_timer("start"), bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
tk.Button(button_frame, text="Pause Timer", command=lambda: start_pause_reset_timer("pause"), bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
tk.Button(button_frame, text="Reset Timer", command=lambda: start_pause_reset_timer("reset"), bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

'''(Gameplay Action Buttons)'''
tk.Button(button_frame, text="Show Solution", command=show_solution, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
tk.Button(button_frame, text="Check Errors", command=check_for_errors, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
tk.Button(button_frame, text="Hint", command=provide_hint, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

tk.Button(button_frame, text="Instructions", command=show_instructions, bg=SECONDARY_COLOR, fg="white", font=FONT_TEXT).grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

'''Makes rows and columns expandable'''
for i in range(3):  # 3 rows of buttons
    button_frame.grid_rowconfigure(i, weight=1)

for i in range(3):  # 3 columns of buttons
    button_frame.grid_columnconfigure(i, weight=1)

# Footer Label
footer_label = tk.Label(
    root,
    text="Created by Batch B5",
    font=("Segoe UI", 10, "italic"),
    bg="#F4F5F7",
    fg="#718096"
)
footer_label.pack(pady=10)

# Bind the close button of the window to restart the app
root.protocol("WM_DELETE_WINDOW", restart_app)

root.mainloop()