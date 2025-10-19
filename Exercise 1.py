from tkinter import *  # Import all tkinter classes for GUI components
import tkinter as tk  # Import tkinter with alias for clarity
import random  # Import random module for generating random numbers

# Initialize main application window
root = tk.Tk()
root.title("Arithmetic Math Quiz")  # Set window title
root.geometry("500x500")  # Set window size to 500x500 pixels
# Set a neutral, aesthetic background color (light gray)
root.configure(bg="#E0E0E0")  

# Global variables to track quiz state
score = 0  # User's current score
question_count = 0  # Number of questions asked
current_answer = None  # Correct answer to the current question
attempts = 0  # Number of attempts for current question
difficulty_level = 1  # Selected difficulty level, default is 1 (easy)

# Function to display the difficulty selection menu
def displayMenu():
    global score, question_count, difficulty_level
    score = 0
    question_count = 0

    # Reset labels and input field
    difficulty_label.config(text="Hi! Welcome to Math Quiz.\nPlease select your difficulty level.")
    problem_label.config(text="")
    answer_entry.delete(0, tk.END)
    result_label.config(text="")

    # Show difficulty buttons
    easy_lvl.pack(side=tk.LEFT, padx=10)
    moderate_lvl.pack(side=tk.LEFT, padx=10)
    advance_lvl.pack(side=tk.LEFT, padx=10)
    difficulty_label.pack(pady=10)

    # Hide start and play again buttons during menu
    start_button.pack_forget()
    play_again_button.pack_forget()

# Function to set the difficulty level based on user choice
def set_difficulty(level):
    global difficulty_level
    difficulty_level = level

    # Hide difficulty selection buttons
    easy_lvl.pack_forget()
    moderate_lvl.pack_forget()
    advance_lvl.pack_forget()

    # Show start button to begin the quiz
    start_button.pack(pady=10)
    # Automatically start first problem
    displayProblem()

# Function to generate a random integer depending on difficulty
def randomInt():
    if difficulty_level == 1:
        return random.randint(1, 9)
    elif difficulty_level == 2:
        return random.randint(10, 99)
    elif difficulty_level == 3:
        return random.randint(1000, 9999)

# Function to randomly decide whether the problem is addition or subtraction
def decideOperation():
    return '+' if random.choice([True, False]) else '-'

# Function to display a new arithmetic problem
def displayProblem():
    global current_answer, attempts, question_count
    attempts = 0
    if question_count < 10:
        question_count += 1
        num1 = randomInt()
        num2 = randomInt()
        operation = decideOperation()
        current_answer = num1 + num2 if operation == '+' else num1 - num2
        problem_label.config(text=f"{num1} {operation} {num2} = ?")
        answer_entry.delete(0, tk.END)
        result_label.config(text="")
    else:
        displayResults()

# Function to check if user's answer is correct
def isCorrect():
    global score, attempts
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        result_label.config(text="Please enter a valid number.", bg="#D3D3D3", fg="#FF2828")
        return

    if user_answer == current_answer:
        if attempts == 0:
            score += 10
            result_label.config(text="Excellent! +10 points.", fg="#B045A9")
        else:
            score += 5
            result_label.config(text="Good job! +5 points.", fg="#B045A9")
        answer_entry.delete(0, tk.END)
        displayProblem()
    else:
        attempts += 1
        if attempts < 2:
            result_label.config(text="Keep trying!", fg="#4B4B4B")
        else:
            result_label.config(text=f"The correct answer was {current_answer}.", fg="#8B5E3C")
            answer_entry.delete(0, tk.END)
            displayProblem()

# Function to display final score and grade
def displayResults():
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    # Clear problem display
    problem_label.config(text="")
    # Show final score and grade
    result_label.config(text=f"YAY! You made it! Your Score is: {score}/100. Grade: {grade}")
    # Show button to play again
    play_again_button.pack(pady=10)

# --- Widgets for GUI ---

# Using modern, aesthetic fonts
font_title = ("Helvetica Rounded", 20, "bold")
font_subtitle = ("Helvetica Neue", 14)
font_button = ("Arial Rounded MT Bold", 14)
font_problem = ("Helvetica Neue", 18, "bold")
font_feedback = ("Helvetica", 12)

# Label for difficulty instruction
difficulty_label = tk.Label(root, text="DIFFICULTY LEVEL", font=font_title, bg="#E0E0E0", fg="#333333")
difficulty_label.pack(pady=10)

# Buttons for selecting difficulty
easy_lvl = tk.Button(root, text="Easy", command=lambda: set_difficulty(1),
                     font=font_button, padx=20, bg="#B0B0B0", fg="#222222")
moderate_lvl = tk.Button(root, text="Moderate", command=lambda: set_difficulty(2),
                         font=font_button, padx=20, bg="#B0B0B0", fg="#222222")
advance_lvl = tk.Button(root, text="Advanced", command=lambda: set_difficulty(3),
                        font=font_button, padx=20, bg="#B0B0B0", fg="#222222")

# Label to display current question
problem_label = tk.Label(root, text="", font=font_problem, bg="#E0E0E0", fg="#222222")
problem_label.pack(pady=20)

# Entry widget for user answer input
answer_entry = tk.Entry(root, font=("Helvetica Neue", 16))
answer_entry.pack()

# Label for feedback messages
result_label = tk.Label(root, text="", font=font_feedback, bg="#E0E0E0", fg="#555555")
result_label.pack(pady=10)

# Button to start the quiz
start_button = tk.Button(root, text="Start the Quiz", command=displayProblem,
                         font=font_button, bg="#B0B0B0", fg="#222222")

# Button to submit answer
submit_button = tk.Button(root, text="Submit Answer", command=isCorrect,
                          font=font_button, bg="#B0B0B0", fg="#222222")
submit_button.pack(pady=10)

# Button to play again after finishing quiz
play_again_button = tk.Button(root, text="Play Again", command=displayMenu,
                              font=font_button, bg="#B0B0B0", fg="#FF0000")

# Initialize the menu
displayMenu()

# Run the application
root.mainloop()
