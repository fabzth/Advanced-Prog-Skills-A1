import tkinter as tk
import random

# Load jokes
def load_jokes(filename):
    jokes = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if '?' in line:
                    parts = line.strip().split('?', 1)
                    if len(parts) == 2:
                        setup = parts[0] + '?'
                        punchline = parts[1]
                        jokes.append((setup, punchline))
    except FileNotFoundError:
        print(f"File not found: {filename}")
    return jokes

jokes = load_jokes("/Users/fabiolazeth/Desktop/ADVPROG/ADVPROG ASSESSMENT 1/randomjokes.txt")
if not jokes:
    raise ValueError("No jokes found. Check your file path and format.")

current_joke = ()

# Initialize main window with vibrant colors
root = tk.Tk()
root.title("Alexa, Tell Me a Joke")
root.geometry("500x600")
root.configure(bg="#2E8B57")  # Dark Cyan background

# Widgets with standout colors
instruction_label = tk.Label(root, text="Enter your command:", font=("Helvetica", 14), bg="#2E8B57", fg="#FFFFFF")
instruction_label.pack(pady=5)

entry = tk.Entry(root, font=("Helvetica", 14), bg="#FFD700", fg="#000000")  
entry.pack(pady=5)

setup_lbl = tk.Label(root, text="", font=("Georgia", 20, "bold"), bg="#2E8B57", fg="#000000", wraplength=460)  
setup_lbl.pack(pady=10)

punch_lbl = tk.Label(root, text="", font=("Helvetica Neue", 18, "underline"), bg="#2E8B57", fg="#000000", wraplength=460)  
punch_lbl.pack(pady=10)

def process_input(event=None):
    global current_joke
    command = entry.get().strip().lower()
    entry.delete(0, tk.END)
    if command == "alexa tell me a joke":
        current_joke = random.choice(jokes)
        setup_lbl.config(text=current_joke[0])
        punch_lbl.config(text="")
        instruction_label.config(text="Press 'Show Punchline' to see the answer.")
    else:
        instruction_label.config(text="Unknown command. Please type 'Alexa tell me a Joke'.")

def show_punchline():
    if current_joke:
        punch_lbl.config(text=current_joke[1])
        instruction_label.config(text="Joke complete! Enter command again.")

# Buttons with standout colors
button_frame = tk.Frame(root, bg="#2E8B57")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Enter", command=process_input, font=("Helvetica", 14), bg="#FF6347", fg="#000000").pack(side='left', padx=5)
tk.Button(button_frame, text="Show Punchline", command=show_punchline, font=("Helvetica", 14), bg="#FFA500", fg="#000000").pack(side='left', padx=5)
tk.Button(button_frame, text="Quit", command=root.destroy, font=("Helvetica", 14), bg="#DC143C", fg="#000000").pack(side='left', padx=5)

# Bind Enter key
entry.bind('<Return>', process_input)

root.mainloop()
