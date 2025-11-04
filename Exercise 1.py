from tkinter import *
import tkinter as tk
import random

# Initialize main application window
root = tk.Tk()  # Create the main window object
root.title("Arithmetic Math Quiz")  # Set window title bar text
root.geometry("500x500")  # Set window size to 500x500 pixels
root.configure(bg="#E0E0E0")  # Set background color to light gray

# Global variables to track quiz state
score = 0  # Track user's current score throughout the quiz
question_count = 0  # Count number of questions asked so far
current_answer = None  # Store correct answer for the current question
attempts = 0  # Track number of attempts for current question
difficulty_level = 1  # Store selected difficulty level, default is 1 (easy)

def displayMenu():
    """Display the main menu with difficulty selection options"""
    global score, question_count  # Access global variables for modification
    score = question_count = 0  # Reset game state for new session

    # Clear previous game displays and show menu interface
    difficulty_label.config(text="Hi! Welcome to Math Quiz.\nPlease select your difficulty level.")  # Update welcome message
    problem_label.config(text="")  # Clear any displayed problem
    answer_entry.delete(0, tk.END)  # Clear the answer input field
    result_label.config(text="")  # Clear any previous feedback

    # Show difficulty selection buttons in a horizontal layout
    for btn in [easy_lvl, moderate_lvl, advance_lvl]:  # Iterate through all difficulty buttons
        btn.pack(side=tk.LEFT, padx=10)  # Pack each button to the left with padding
    difficulty_label.pack(pady=10)  # Display the difficulty label with vertical padding
    start_button.pack_forget()  # Hide the start button during menu display
    play_again_button.pack_forget()  # Hide the play again button during menu display

def set_difficulty(level):
    """Set the difficulty level and prepare quiz start"""
    global difficulty_level  # Access global difficulty variable
    difficulty_level = level  # Update difficulty level based on user selection

    # Hide difficulty buttons after selection
    for btn in [easy_lvl, moderate_lvl, advance_lvl]:  # Iterate through difficulty buttons
        btn.pack_forget()  # Remove each button from display
    start_button.pack(pady=10)  # Show the start button with vertical padding
    displayProblem()  # Automatically start the first problem

def randomInt():
    """Generate random numbers based on selected difficulty level"""
    difficulty_ranges = {  # Define number ranges for each difficulty level
        1: (1, 9),    # Easy: single-digit numbers from 1 to 9
        2: (10, 99),  # Moderate: two-digit numbers from 10 to 99
        3: (1000, 9999)  # Advanced: four-digit numbers from 1000 to 9999
    }
    return random.randint(*difficulty_ranges[difficulty_level])  # Return random number from selected range

def displayProblem():
    """Generate and display a new arithmetic problem"""
    global current_answer, attempts, question_count  # Access global variables
    attempts = 0  # Reset attempts counter for new question

    if question_count < 10:  # Check if we haven't reached 10 questions yet
        question_count += 1  # Increment question counter
        num1, num2 = randomInt(), randomInt()  # Generate two random numbers
        operation = random.choice(['+', '-'])  # Randomly choose addition or subtraction operation

        # Calculate correct answer based on selected operation
        current_answer = num1 + num2 if operation == '+' else num1 - num2

        # Display the arithmetic problem to user
        problem_label.config(text=f"{num1} {operation} {num2} = ?")  # Update problem display
        answer_entry.delete(0, tk.END)  # Clear previous answer from input field
        result_label.config(text="")  # Clear any previous feedback
    else:  # If 10 questions have been completed
        displayResults()  # Show final results

def isCorrect():
    """Check if user's answer is correct and provide feedback"""
    global score, attempts  # Access global score and attempts variables
    try:
        user_answer = int(answer_entry.get())  # Get user input and convert to integer
    except ValueError:  # Handle case where input is not a valid number
        result_label.config(text="Please enter a valid number.", fg="#FF2828")  # Show error message in red
        return  # Exit function early

    if user_answer == current_answer:  # Check if answer is correct
        # Award points based on number of attempts
        score += 10 if attempts == 0 else 5  # 10 points for first try, 5 for second
        feedback = "Excellent! +10 points." if attempts == 0 else "Good job! +5 points."  # Set feedback message
        result_label.config(text=feedback, fg="#B045A9")  # Show feedback in purple
        answer_entry.delete(0, tk.END)  # Clear input field
        displayProblem()  # Load next question
    else:  # If answer is incorrect
        attempts += 1  # Increment attempts counter
        if attempts < 2:  # If user still has attempts remaining
            result_label.config(text="Keep trying!", fg="#4B4B4B")  # Show encouragement in dark gray
        else:  # If user has used all attempts
            result_label.config(text=f"The correct answer was {current_answer}.", fg="#8B5E3C")  # Reveal answer in brown
            answer_entry.delete(0, tk.END)  # Clear input field
            displayProblem()  # Move to next question

def displayResults():
    """Display final score and grade after completing all questions"""
    # Define grading scale with minimum scores and corresponding grades
    grade_scale = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]
    # Find the appropriate grade based on score, default to "F" if below 50
    grade = next((g for min_score, g in grade_scale if score >= min_score), "F")

    # Show final results to user
    problem_label.config(text="")  # Clear the problem display
    result_label.config(text=f"YAY! You made it! Your Score is: {score}/100. Grade: {grade}")  # Show score and grade
    play_again_button.pack(pady=10)  # Display play again button with padding

# Create and configure GUI widgets with modern styling
font_title = ("Helvetica Rounded", 20, "bold")  # Define font for titles
font_button = ("Arial Rounded MT Bold", 14)  # Define font for buttons
font_problem = ("Helvetica Neue", 18, "bold")  # Define font for problems

# Difficulty selection label
difficulty_label = tk.Label(root, text="DIFFICULTY LEVEL", font=font_title, bg="#E0E0E0", fg="#333333")

# Problem display label - shows the arithmetic problem
problem_label = tk.Label(root, text="", font=font_problem, bg="#E0E0E0", fg="#222222")

# User input field - where user enters their answer
answer_entry = tk.Entry(root, font=("Helvetica Neue", 16))

# Feedback message label - shows results and encouragement
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#E0E0E0", fg="#555555")

# Difficulty level buttons with different commands for each level
easy_lvl = tk.Button(root, text="Easy", command=lambda: set_difficulty(1),
                     font=font_button, padx=20, bg="#B0B0B0")  # Light gray button for easy level
moderate_lvl = tk.Button(root, text="Moderate", command=lambda: set_difficulty(2),
                         font=font_button, padx=20, bg="#B0B0B0")  # Light gray button for moderate level
advance_lvl = tk.Button(root, text="Advanced", command=lambda: set_difficulty(3),
                        font=font_button, padx=20, bg="#B0B0B0")  # Light gray button for advanced level

# Game control buttons
start_button = tk.Button(root, text="Start the Quiz", command=displayProblem,
                         font=font_button, bg="#B0B0B0")  # Button to start the quiz
submit_button = tk.Button(root, text="Submit Answer", command=isCorrect,
                          font=font_button, bg="#B0B0B0")  # Button to submit answer
play_again_button = tk.Button(root, text="Play Again", command=displayMenu,
                              font=font_button, bg="#B0B0B0", fg="#FF0000")  # Red text for play again button

# Arrange widgets in the window using pack geometry manager
difficulty_label.pack(pady=10)  # Pack difficulty label with vertical padding
problem_label.pack(pady=20)  # Pack problem label with larger vertical padding
answer_entry.pack()  # Pack answer entry field
result_label.pack(pady=10)  # Pack result label with vertical padding
submit_button.pack(pady=10)  # Pack submit button with vertical padding

# Initialize the application with main menu
displayMenu()  # Call function to show the initial menu

root.mainloop()
