from tkinter import *
import random

# Main application window
root = Tk()
root.title("Arithmetic Math Quiz")
root.geometry("500x500")
root.configure(bg="#E0E0E0")

# Game state variables
score = question_count = attempts = difficulty_level = 1
current_answer = None

def displayMenu():
    # Display main menu with difficulty selection options
    global score, question_count
    score = question_count = 0
    difficulty_label.config(text="Hi! Welcome to Math Quiz.\nPlease select your difficulty level.")
    problem_label.config(text="")
    answer_entry.delete(0, END)
    result_label.config(text="")
    for btn in [easy_lvl, moderate_lvl, advance_lvl]:
        btn.pack(side=LEFT, padx=10)
    difficulty_label.pack(pady=10)
    start_button.pack_forget()
    play_again_button.pack_forget()

def set_difficulty(level):
    # Set difficulty level and prepare quiz start
    global difficulty_level
    difficulty_level = level
    for btn in [easy_lvl, moderate_lvl, advance_lvl]:
        btn.pack_forget()
    start_button.pack(pady=10)
    displayProblem()

def randomInt():
    # Generate random numbers based on selected difficulty level
    ranges = {1: (1, 9), 2: (10, 99), 3: (1000, 9999)}
    return random.randint(*ranges[difficulty_level])

def displayProblem():
    # Generate and display a new arithmetic problem
    global current_answer, attempts, question_count
    attempts = 0
    if question_count < 10:
        question_count += 1
        num1, num2 = randomInt(), randomInt()
        operation = random.choice(['+', '-'])
        current_answer = num1 + num2 if operation == '+' else num1 - num2
        problem_label.config(text=f"{num1} {operation} {num2} = ?")
        answer_entry.delete(0, END)
        result_label.config(text="")
    else:
        displayResults()

def isCorrect():
    # Check if user's answer is correct and provide feedback
    global score, attempts
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        result_label.config(text="Please enter a valid number.", fg="#FF2828")
        return
    if user_answer == current_answer:
        score += 10 if attempts == 0 else 5
        feedback = "Excellent! +10 points." if attempts == 0 else "Good job! +5 points."
        result_label.config(text=feedback, fg="#B045A9")
        answer_entry.delete(0, END)
        displayProblem()
    else:
        attempts += 1
        if attempts < 2:
            result_label.config(text="Keep trying!", fg="#4B4B4B")
        else:
            result_label.config(text=f"The correct answer was {current_answer}.", fg="#8B5E3C")
            answer_entry.delete(0, END)
            displayProblem()

def displayResults():
    # Display final score and grade after completing all questions
    grade_scale = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]
    grade = next((g for min_score, g in grade_scale if score >= min_score), "F")
    problem_label.config(text="")
    result_label.config(text=f"YAY! You made it! Your Score is: {score}/100. Grade: {grade}")
    play_again_button.pack(pady=10)

# Create GUI widgets
font_title = ("Helvetica Rounded", 20, "bold")
font_button = ("Arial Rounded MT Bold", 14)
font_problem = ("Helvetica Neue", 18, "bold")

difficulty_label = Label(root, text="DIFFICULTY LEVEL", font=font_title, bg="#E0E0E0", fg="#333333")
problem_label = Label(root, text="", font=font_problem, bg="#E0E0E0", fg="#222222")
answer_entry = Entry(root, font=("Helvetica Neue", 16))
result_label = Label(root, text="", font=("Helvetica", 12), bg="#E0E0E0", fg="#555555")

# Difficulty buttons
easy_lvl = Button(root, text="Easy", command=lambda: set_difficulty(1), font=font_button, padx=20, bg="#B0B0B0")
moderate_lvl = Button(root, text="Moderate", command=lambda: set_difficulty(2), font=font_button, padx=20, bg="#B0B0B0")
advance_lvl = Button(root, text="Advanced", command=lambda: set_difficulty(3), font=font_button, padx=20, bg="#B0B0B0")

# Control buttons
start_button = Button(root, text="Start the Quiz", command=displayProblem, font=font_button, bg="#B0B0B0")
submit_button = Button(root, text="Submit Answer", command=isCorrect, font=font_button, bg="#B0B0B0")
play_again_button = Button(root, text="Play Again", command=displayMenu, font=font_button, bg="#B0B0B0", fg="#FF0000")

# Arrange widgets
difficulty_label.pack(pady=10)
problem_label.pack(pady=20)
answer_entry.pack()
result_label.pack(pady=10)
submit_button.pack(pady=10)

# Initialize application
displayMenu()
root.mainloop()
