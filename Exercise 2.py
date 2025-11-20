import tkinter as tk
import random

# Load jokes from file

def load_jokes(filename):
    jokes = []  # List to store jokes as (setup, punchline) pairs
    try:
        # Open the file in read mode
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Only process lines that contain a question mark
                if '?' in line:
                    # Split joke into setup and punchline at the first '?'
                    setup, punchline = line.strip().split('?', 1)

                    # Add the '?' back to the setup, create tuple, store it
                    jokes.append((setup + '?', punchline))
    except FileNotFoundError:
        # Print error if file is missing
        print(f"File not found: {filename}")

    return jokes  # Return list of jokes


# LOAD AND VALIDATE JOKES

jokes = load_jokes("randomjokes.txt")  # load jokes from text

# If no jokes are found, stop program with error message
if not jokes:
    raise ValueError("No jokes found. Check your file path and format.")

current_joke = ()  # Variable to store the currently selected joke


root = tk.Tk()  # Create main window
root.title("Alexa, Tell Me a Joke")  # Window title
root.geometry("500x600")  # Set window size (width x height)
root.configure(bg="#2E8B57")  # Set background color (forest green)


# CREATE GUI WIDGETS

instruction_label = tk.Label(root, text="Enter your command:",
                             font=("Helvetica", 14), bg="#2E8B57", fg="#FFFFFF")
instruction_label.pack(pady=5)

entry = tk.Entry(root, font=("Helvetica", 14), bg="#FFD700", fg="green")  # Command input field
entry.pack(pady=5)

# Label to display the setup of the joke (question)
setup_lbl = tk.Label(root, text="", font=("Georgia", 20, "bold"),
                     bg="#2E8B57", fg="#000000", wraplength=460) # ensures long text wraps within the specified pixel width
setup_lbl.pack(pady=10)

# Label to display the punchline (answer) later
punch_lbl = tk.Label(root, text="", font=("Helvetica Neue", 18, "underline"),
                     bg="#2E8B57", fg="#000000", wraplength=460)
punch_lbl.pack(pady=10)


# FUNCTION: Process user input
# Triggered when user presses Enter or clicks Enter button

def process_input(event=None):
    global current_joke

    # Get text from input box and convert to lowercase (for uniform comparison)
    command = entry.get().strip().lower() # making it case-insensitive
    entry.delete(0, tk.END)  # Clear input box

    # Check if user typed the trigger phrase
    if command == "alexa tell me a joke":
        current_joke = random.choice(jokes)  # Pick a random joke
        setup_lbl.config(text=current_joke[0])  # Display the setup (question)
        punch_lbl.config(text="")  # Hide punchline until button press
        instruction_label.config(text="Press 'Show Punchline' to see the answer.")
    else:
        # If user types something different, show hint
        instruction_label.config(text="Unknown command. Please type 'Alexa tell me a Joke'.")



# FUNCTION: Show the punchline

def show_punchline():
    if current_joke:  # Ensure a joke has been selected
        punch_lbl.config(text=current_joke[1])  # Show punchline (answer)
        instruction_label.config(text="Joke complete! Enter command again.")


# BUTTONS SECTION

button_frame = tk.Frame(root, bg="#2E8B57")  # A frame to hold buttons in one row
button_frame.pack(pady=10)

# Button to process input command
tk.Button(button_frame, text="Enter", command=process_input,
          font=("Helvetica", 14), bg="#FF6347", fg="#000000").pack(side='left', padx=5)

# Button to show punchline
tk.Button(button_frame, text="Show Punchline", command=show_punchline,
          font=("Helvetica", 14), bg="#FFA500", fg="#000000").pack(side='left', padx=5)

# Button to quit the program
tk.Button(button_frame, text="Quit", command=root.destroy,
          font=("Helvetica", 14), bg="#DC143C", fg="#000000").pack(side='left', padx=5)

entry.bind('<Return>', process_input) # binds the enter key to call the process_input function

root.mainloop()
