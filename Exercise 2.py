import tkinter as tk
import random

def load_jokes(filename):
    """Load jokes from text file and parse into setup-punchline pairs"""
    jokes = []  # Initialize empty list to store joke tuples (setup, punchline)
    try:
        with open(filename, 'r', encoding='utf-8') as file:  # Open file with UTF-8 encoding for special characters
            for line in file:  # Iterate through each line in the file
                if '?' in line:  # Check if line contains a question mark (joke separator)
                    setup, punchline = line.strip().split('?', 1)  # Split line at first question mark only
                    jokes.append((setup + '?', punchline))  # Rebuild joke with question mark and add to list
    except FileNotFoundError:  # Handle case where file doesn't exist
        print(f"File not found: {filename}")  # Print error message to console
    return jokes  # Return the list of loaded jokes

# Load and validate jokes from file
jokes = load_jokes("/Users/fabiolazeth/Desktop/AP/ADVPROG ASSESSMENT 1/randomjokes.txt")  # Load jokes from specified file path
if not jokes:  # Check if jokes list is empty (file not found or no valid jokes)
    raise ValueError("No jokes found. Check your file path and format.")  # Raise error with helpful message

current_joke = ()  # Global variable to track currently displayed joke as empty tuple initially

# Initialize main application window
root = tk.Tk()  # Create the main window object
root.title("Alexa, Tell Me a Joke")  # Set window title bar text
root.geometry("500x600")  # Set window size to 500 pixels wide, 600 pixels tall
root.configure(bg="#2E8B57")  # Set background color to sea green

# Create and configure GUI widgets
instruction_label = tk.Label(root, text="Enter your command:", font=("Helvetica", 14),
                             bg="#2E8B57", fg="#FFFFFF")  # Create instruction label with white text on green background
instruction_label.pack(pady=5)  # Add label to window with 5 pixel vertical padding

entry = tk.Entry(root, font=("Helvetica", 14), bg="#FFD700", fg="#000000")  # Create input field with gold background and black text
entry.pack(pady=5)  # Add input field to window with 5 pixel vertical padding

setup_lbl = tk.Label(root, text="", font=("Georgia", 20, "bold"), bg="#2E8B57",
                     fg="#000000", wraplength=460)  # Create label for joke setup with bold Georgia font and word wrapping
setup_lbl.pack(pady=10)  # Add setup label to window with 10 pixel vertical padding

punch_lbl = tk.Label(root, text="", font=("Helvetica Neue", 18, "underline"),
                     bg="#2E8B57", fg="#000000", wraplength=460)  # Create label for punchline with underlined font
punch_lbl.pack(pady=10)  # Add punchline label to window with 10 pixel vertical padding

def process_input(event=None):
    """Process user command to trigger joke delivery"""
    global current_joke  # Access global current_joke variable
    command = entry.get().strip().lower()  # Get user input, remove whitespace, convert to lowercase
    entry.delete(0, tk.END)  # Clear the input field after reading the command

    if command == "alexa tell me a joke":  # Check if user typed the exact activation phrase
        current_joke = random.choice(jokes)  # Randomly select a joke from the loaded jokes list
        setup_lbl.config(text=current_joke[0])  # Display the joke setup (question part)
        punch_lbl.config(text="")  # Clear any previously displayed punchline
        instruction_label.config(text="Press 'Show Punchline' to see the answer.")  # Update instructions
    else:  # If user typed something other than the activation phrase
        instruction_label.config(text="Unknown command. Please type 'Alexa tell me a Joke'.")  # Show error message

def show_punchline():
    """Reveal the punchline of the current joke"""
    if current_joke:  # Check if there is a current joke selected
        punch_lbl.config(text=current_joke[1])  # Display the punchline (answer part)
        instruction_label.config(text="Joke complete! Enter command again.")  # Update instructions

# Create button container
button_frame = tk.Frame(root, bg="#2E8B57")  # Create frame to hold buttons with matching background color
button_frame.pack(pady=10)  # Add button frame to window with 10 pixel vertical padding

# Create control buttons with distinct colors
tk.Button(button_frame, text="Enter", command=process_input, font=("Helvetica", 14),
          bg="#FF6347", fg="#000000").pack(side='left', padx=5)  # Create red Enter button with left positioning
tk.Button(button_frame, text="Show Punchline", command=show_punchline, font=("Helvetica", 14),
          bg="#FFA500", fg="#000000").pack(side='left', padx=5)  # Create orange Show Punchline button
tk.Button(button_frame, text="Quit", command=root.destroy, font=("Helvetica", 14),
          bg="#DC143C", fg="#000000").pack(side='left', padx=5)  # Create crimson Quit button to close application

# Bind Enter key to process input
entry.bind('<Return>', process_input)  # Make Enter key trigger the process_input function

root.mainloop()
