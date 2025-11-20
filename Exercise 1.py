from tkinter import *
import random # to pick random numbers

# main window of the app
root = Tk()
root.title("Arithmetic Math Quiz")
root.geometry("500x500")
root.configure(bg="#E0E0E0")

# global variables
# score = total points earned
# question_count = number of questions asked so far (out of 10)
# attempts = number of tries for the current question
# difficulty_level = 1 means Easy, 2 means Moderate, 3 means Advanced
score = question_count = attempts = difficulty_level = 1 # all four variables are being set to 1 at the same time.
current_answer = None  # stores the correct answer of the current math problem


def displayMenu():
    """Show the main menu for choosing the difficulty level."""
    global score, question_count          # global so we can reset values
    score = question_count = 0            # reset score and question count
    difficulty_label.config(text="Hi! Welcome to Math Quiz.\nPlease select your difficulty level.")
    problem_label.config(text="")         # Clear problem text
    answer_entry.delete(0, END)      # Clear answer input
    result_label.config(text="")          # Clear feedback text

    # Show difficulty buttons again
    for btn in [easy_lvl, moderate_lvl, advance_lvl]:
        btn.pack(side=LEFT, padx=10)

    difficulty_label.pack(pady=10)
    start_button.pack_forget()            # Hide start button if shown before
    play_again_button.pack_forget()       # Hide play again button until needed


def set_difficulty(level):
    """Set the difficulty level and get ready to start the quiz."""
    global difficulty_level
    difficulty_level = level              # Store selected difficulty level

    # Hide difficulty buttons
    for btn in [easy_lvl, moderate_lvl, advance_lvl]:
        btn.pack_forget()

    start_button.pack(pady=10)            # Show start quiz button
    displayProblem()                      # Immediately display the first problem


def randomInt():
    """Return a random integer depending on difficulty level."""
    # Ranges for each difficulty
    ranges = {1: (1, 9), 2: (10, 99), 3: (1000, 9999)}
    # Pick numbers between the range of selected difficulty
    return random.randint(*ranges[difficulty_level])


def displayProblem():
    """Generate and display a new math problem."""
    global current_answer, attempts, question_count
    attempts = 0                          # Reset attempts for new question

    if question_count < 10:               # Only ask 10 questions maximum
        question_count += 1               # Increase question count

        num1, num2 = randomInt(), randomInt()     # Generate two random numbers
        operation = random.choice(['+', '-'])     # Choose + or - randomly

        # Calculate correct answer depending on operation
        current_answer = num1 + num2 if operation == '+' else num1 - num2

        # Display formatted problem to user
        problem_label.config(text=f"{num1} {operation} {num2} = ?")
        answer_entry.delete(0, END)       # Clear answer input box
        result_label.config(text="")      # Clear any previous feedback

    else:
        displayResults()                  # If 10 questions done, show results


def isCorrect():
    """Check if the user's answer is correct and give feedback."""
    global score, attempts

    try:
        user_answer = int(answer_entry.get())     # Convert input to integer
    except ValueError:
        result_label.config(text="Please enter a valid number.", fg="#FF2828")
        return                                    # Stop function if input is not a number

    if user_answer == current_answer:             # Check if answer is correct
        # Score system: first try earns 10 points, second try earns 5 points
        score += 10 if attempts == 0 else 5
        feedback = "Excellent! +10 points." if attempts == 0 else "Good job! +5 points."
        result_label.config(text=feedback, fg="#B045A9")
        answer_entry.delete(0, END)
        displayProblem()                          # Show next question

    else:
        attempts += 1                             # Increase attempt count
        if attempts < 2:                          # If first mistake
            result_label.config(text="Keep trying!", fg="#4B4B4B")
        else:
            result_label.config(text=f"The correct answer was {current_answer}.", fg="#8B5E3C")
            answer_entry.delete(0, END)
            displayProblem()                      # Move to next question after 2 tries


def displayResults():
    """Show the final score and grade after all questions are answered."""
    grade_scale = [(90,100, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]
    # Choose grade from grade scale based on score
    grade = next((g for min_score, g in grade_scale if score >= min_score), "F")

    problem_label.config(text="")   # Clear question text
    result_label.config(text=f"YAY! You made it! Your Score is: {score}/100. Grade: {grade}")
    play_again_button.pack(pady=10) # Show play again button


# GUI WIDGET SETUP

# Fonts used for styling
font_title = ("Helvetica Rounded", 20, "bold")
font_button = ("Arial Rounded MT Bold", 14)
font_problem = ("Helvetica Neue", 18, "bold")

# Labels and input box
difficulty_label = Label(root, text="DIFFICULTY LEVEL", font=font_title, bg="#E0E0E0", fg="#333333")
problem_label = Label(root, text="", font=font_problem, bg="#E0E0E0", fg="#222222")
answer_entry = Entry(root, font=("Helvetica Neue", 16))
result_label = Label(root, text="", font=("Helvetica", 12), bg="#E0E0E0", fg="#555555")

# Difficulty selection buttons
easy_lvl = Button(root, text="Easy", command=lambda: set_difficulty(1), font=font_button, padx=20, bg="#B0B0B0")
moderate_lvl = Button(root, text="Moderate", command=lambda: set_difficulty(2), font=font_button, padx=20, bg="#B0B0B0")
advance_lvl = Button(root, text="Advanced", command=lambda: set_difficulty(3), font=font_button, padx=20, bg="#B0B0B0")

# Gameplay control buttons
start_button = Button(root, text="Start the Quiz", command=displayProblem, font=font_button, bg="#B0B0B0")
submit_button = Button(root, text="Submit Answer", command=isCorrect, font=font_button, bg="#B0B0B0")
play_again_button = Button(root, text="Play Again", command=displayMenu, font=font_button, bg="#B0B0B0", fg="#FF0000")

# Place widgets on screen
difficulty_label.pack(pady=10)
problem_label.pack(pady=20)
answer_entry.pack()
result_label.pack(pady=10)
submit_button.pack(pady=10)

# Display main menu when program starts
displayMenu()

root.mainloop()
