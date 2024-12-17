import tkinter as tk
import subprocess
from tkinter import messagebox, Toplevel

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

# Initialize the main window
root = tk.Tk()
root.title("Sudoku : Chill Game!")
root.configure(bg="#F4F5F7")  # Light grey background for a modern look

width = 500
height = 700

# Center the window on the screen
center_window(root, width, height)

# Modern Colors and Fonts
PRIMARY_COLOR = "#2D3748"  # Dark blue for text
SECONDARY_COLOR = "#4A90E2"  # Accent blue
BACKGROUND_COLOR = "#FFFFFF"  # White background
GRID_COLOR = "#E2E8F0"  # Light border for grid
HIGHLIGHT_COLOR = "#EDF2F7"  # Subtle highlight

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_TEXT = ("Segoe UI", 12)
FONT_ENTRY = ("Segoe UI", 18, "bold")

# Create the Sudoku Grid
def create_empty_grid():
    return [[0 for _ in range(6)] for _ in range(6)]

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

def validate_entry(value):
    """Ensure the entry contains only numbers from 0 to 6."""
    return value == "" or (value.isdigit() and 0 <= int(value) <= 6)

validate_command = root.register(validate_entry)

# Premium Title Label
title_label = tk.Label(
    root,
    text="6x6 Sudoku Solver",
    font=FONT_TITLE,
    bg="#F4F5F7",
    fg=PRIMARY_COLOR
)
title_label.pack(pady=20)

instructions_label = tk.Label(
    root,
    text="Enter numbers (1-6) in the grid and click 'Solve'.",
    font=FONT_TEXT,
    bg="#F4F5F7",
    fg=PRIMARY_COLOR
)
instructions_label.pack()

# Sudoku Grid
entries = []
grid = create_empty_grid()

frame = tk.Frame(root, bg=GRID_COLOR, bd=2, relief="flat")
frame.pack(pady=20)

for i in range(6):
    row_entries = []
    for j in range(6):
        bg_color = BACKGROUND_COLOR if (i // 2 + j // 3) % 2 == 0 else HIGHLIGHT_COLOR
        entry = tk.Entry(
            frame,
            width=2,
            font=FONT_ENTRY,
            justify="center",
            bg=bg_color,
            fg=PRIMARY_COLOR,
            relief="flat",
            validate="key",
            validatecommand=(validate_command, "%P")
        )
        entry.grid(row=i, column=j, ipadx=10, ipady=10, padx=2, pady=2)
        row_entries.append(entry)
    entries.append(row_entries)

# Solve Functionality
def display_solution():
    """Solve and display the solution in the GUI."""
    for row in range(6):
        for col in range(6):
            try:
                grid[row][col] = int(entries[row][col].get()) if entries[row][col].get() else 0
            except ValueError:
                messagebox.showerror("Invalid Input", "Only numbers from 1-6 are allowed!")
                return

    if solve_sudoku(grid):
        for row in range(6):
            for col in range(6):
                entries[row][col].delete(0, tk.END)
                entries[row][col].insert(0, grid[row][col])
                entries[row][col].config(state="disabled", disabledbackground=HIGHLIGHT_COLOR, disabledforeground=PRIMARY_COLOR)
        
        # Show success message and reset the game when OK is clicked
        messagebox.showinfo("Success", "Sudoku solved successfully!")
        reset_game()
    else:
        messagebox.showerror("No Solution", "This Sudoku puzzle cannot be solved.")

def reset_game():
    """Reset the Sudoku grid and clear all entries."""
    for row in range(6):
        for col in range(6):
            entries[row][col].config(state="normal", bg=BACKGROUND_COLOR if (row // 2 + col // 3) % 2 == 0 else HIGHLIGHT_COLOR)
            entries[row][col].delete(0, tk.END)
            grid[row][col] = 0

# Solve Button with Hover Effect
def on_enter(e):
    solve_button.config(bg=SECONDARY_COLOR, fg="white")

def on_leave(e):
    solve_button.config(bg=PRIMARY_COLOR, fg="white")

solve_button = tk.Button(
    root,
    text="Solve",
    command=display_solution,
    font=("Segoe UI", 16, "bold"),
    bg=PRIMARY_COLOR,
    fg="white",
    relief="flat",
    padx=10,
    pady=5
)
solve_button.bind("<Enter>", on_enter)
solve_button.bind("<Leave>", on_leave)
solve_button.pack(pady=10)

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

instructions_button = tk.Button(
    root,
    text="Instructions",
    command=show_instructions,
    font=("Segoe UI", 14, "bold"),
    bg=SECONDARY_COLOR,
    fg="white",
    relief="flat",
    padx=10,
    pady=5
)
instructions_button.pack()

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