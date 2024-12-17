import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def run_sudoku_app_part_1():
    root.destroy()
    subprocess.run(["python", "first_app.py"])

def run_sudoku_app_part_2():
    root.destroy()
    subprocess.run(["python", "second_app.py"])

def show_credits():
    credits_window = tk.Toplevel(root)
    credits_window.title("Credits")
    credits_window.configure(bg="black")
    
    width, height = 400, 250
    center_window(credits_window, width, height)

    # Canvas for credits text
    canvas = tk.Canvas(credits_window, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Credits content
    credits_text = """
🎰🎮
Game of Sudoku

Developed By:
Rahul V B - Game Logic
Sairohitha Balam - Frontend Developer
Sumedha Bhat - Backend Developer
Vaishnavi Kulkarni - UI/UX Designer

Tools & Technologies:
Python, Tkinter, Subprocess

Algorithm Used:
Backtracking

© 2024 Sudoku Development Team
Thank you for playing!
    """

    FONT_CREDITS = ("Segoe UI", 14, "bold")
    text_lines = credits_text.strip().split("\n")

    # Create the text on canvas
    text_y_position = 170  # Start position for bottom of the window
    text_items = []
    for line in text_lines:
        item = canvas.create_text(
            200, text_y_position,  # x=200 centers horizontally on a 400px wide canvas
            text=line,
            font=FONT_CREDITS,
            fill="white",
            anchor="center"  # Centers the text horizontally
        )
        text_items.append(item)
        text_y_position += 30  # Space between lines

    # Function to scroll credits upward
    def scroll_credits():
        nonlocal text_items
        for item in text_items:
            canvas.move(item, 0, -1)  # Move text upward by 1 pixel
        # Check if the last line has completely moved out of the window
        if canvas.bbox(text_items[-1])[3] > 0:  # If the bottommost text is still visible
            credits_window.after(20, scroll_credits)
        else:
            credits_window.destroy()  # Close window when scrolling finishes

    # Start scrolling
    credits_window.after(1000, scroll_credits)

def main():
    global root
    root = tk.Tk()
    root.title("Game of Sudoku")
    root.configure(bg="#F4F5F7")
    width = 600
    height = 270
    center_window(root, width, height)
    
    PRIMARY_COLOR = "#2D3748"
    FONT_TITLE = ("Segoe UI", 26, "bold")
    FONT_TEXT = ("Segoe UI", 12)
    
    greeting_label = tk.Label(
        root,
        text="Hello! 👋🏻\nWelcome To the Game of Sudoku",
        font=FONT_TITLE,
        bg="#F4F5F7",
        fg=PRIMARY_COLOR
    )
    greeting_label.pack(pady=30)

    button_frame = tk.Frame(root, bg="#F4F5F7")
    button_frame.pack(pady=20)

    play_sudoku_button_1 = tk.Button(
        button_frame,
        text="Make Machine Play",
        font=FONT_TEXT,
        bg=PRIMARY_COLOR,
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=run_sudoku_app_part_1
    )
    play_sudoku_button_1.pack(side="left", padx=10)

    play_sudoku_button_2 = tk.Button(
        button_frame,
        text="Play as Player",
        font=FONT_TEXT,
        bg=PRIMARY_COLOR,
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=run_sudoku_app_part_2
    )
    play_sudoku_button_2.pack(side="left", padx=10)

    credits_button = tk.Button(
        button_frame,
        text="Credits",
        font=FONT_TEXT,
        bg="#6B46C1",  # Purple color
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=show_credits
    )
    credits_button.pack(side="left", padx=10)

    exit_button = tk.Button(
        button_frame,
        text="Exit",
        font=FONT_TEXT,
        bg="red",
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=root.quit
    )
    exit_button.pack(side="left", padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
