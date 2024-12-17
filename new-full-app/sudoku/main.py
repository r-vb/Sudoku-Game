import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y position of the window to center it
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the position of the window
    window.geometry(f'{width}x{height}+{x}+{y}')

def run_sudoku_app_part_1():
    """Launch the second app (Sudoku solver) and close the current window"""
    root.destroy()  # Close the current window
    subprocess.run(["python", "first_app/first_app.py"])  # Run Sudoku app

def run_sudoku_app_part_2():
    """Launch the second app (Sudoku solver) and close the current window"""
    root.destroy()  # Close the current window
    subprocess.run(["python", "second_app/second_app.py"])  # Run Sudoku app

def main():
    """Main GUI with greeting message and options to play Sudoku or ask a question."""
    # Initialize the root window
    global root
    root = tk.Tk()
    root.title("Game of Sudoku")
    root.configure(bg="#F4F5F7")

    width = 600
    height = 240

    # Center the window on the screen
    center_window(root, width, height)
    
    # Define fonts and colors
    PRIMARY_COLOR = "#2D3748"
    FONT_TITLE = ("Segoe UI", 26, "bold")
    FONT_TEXT = ("Segoe UI", 12)
    
    # Greeting Label
    greeting_label = tk.Label(
        root,
        text="Welcome To the Game of Sudoku",
        font=FONT_TITLE,
        bg="#F4F5F7",
        fg=PRIMARY_COLOR
    )
    greeting_label.pack(pady=30)

    # Create a frame to contain the buttons side by side
    button_frame = tk.Frame(root, bg="#F4F5F7")
    button_frame.pack(pady=20)

    # Button to make the machine play
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

    # Button to play as a player
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

    # Exit button
    exit_button = tk.Button(
        button_frame,
        text="Exit",
        font=FONT_TEXT,
        bg="red",  # You can use any color for the exit button
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=root.quit  # Close the application when clicked
    )
    exit_button.pack(side="left", padx=10)


    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()