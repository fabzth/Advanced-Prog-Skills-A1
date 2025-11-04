import tkinter as tk
from tkinter import messagebox, ttk

MAX_TOTAL_SCORE = 160  # Maximum possible score: 60 from coursework (3 assignments × 20) + 100 from exam


class Student:
    """Represents a student with coursework marks, exam mark, and calculated grades"""

    def __init__(self, code, name, mark1, mark2, mark3, exam_mark):
        self.code = int(code)  # Convert student ID to integer
        self.name = name  # Store student name
        self.coursework_marks = [int(mark1), int(mark2), int(mark3)]  # Store coursework marks as integers
        self.exam_mark = int(exam_mark)  # Convert exam mark to integer
        self.calculate_scores()  # Calculate totals and grades immediately

    def calculate_scores(self):
        """Calculate total scores, percentage, and determine grade"""
        self.total_coursework = sum(self.coursework_marks)  # Sum of all coursework marks
        self.total_score = self.total_coursework + self.exam_mark  # Combined coursework and exam score
        self.percentage = (self.total_score / MAX_TOTAL_SCORE) * 100  # Calculate percentage out of maximum
        # Determine letter grade based on percentage using conditional expression
        self.grade = 'A' if self.percentage >= 70 else 'B' if self.percentage >= 60 else \
            'C' if self.percentage >= 50 else 'D' if self.percentage >= 40 else 'F'


def load_data(filename):
    """Load student data from CSV file and create Student objects"""
    students = []  # Initialize empty list to store student objects
    try:
        with open(filename, 'r') as file:  # Open file in read mode
            file.readline(), file.readline()  # Skip first two lines (student count and header)
            for line in file:  # Iterate through remaining lines
                parts = line.strip().split(',')  # Split line by commas and remove whitespace
                if len(parts) == 5: parts.append('0')  # Add default exam mark if missing
                if len(parts) != 6: continue  # Skip lines that don't have exactly 6 parts
                try:
                    # Validate that all marks are non-negative integers
                    if any(int(m) < 0 for m in parts[2:]): continue  # Skip if any mark is negative
                    students.append(Student(*parts))  # Create Student object and add to list
                except ValueError:
                    continue  # Skip lines with invalid data types
    except FileNotFoundError:  # Handle case where file doesn't exist
        messagebox.showerror("Error", f"File '{filename}' not found")  # Show error dialog
    return students  # Return the list of student objects


def save_data(filename, students):
    """Save student data back to CSV file with proper header format"""
    try:
        with open(filename, 'w') as file:  # Open file in write mode (overwrites existing)
            file.write(f"{len(students)}\nID,Name,Grade1,Grade2,Grade3,ExamMark\n")  # Write count and header
            for s in students:  # Iterate through each student
                # Write student data in CSV format with all marks
                file.write(
                    f"{s.code},{s.name},{s.coursework_marks[0]},{s.coursework_marks[1]},{s.coursework_marks[2]},{s.exam_mark}\n")
    except Exception as e:  # Handle any file write errors
        messagebox.showerror("Save Error", f"Error saving data: {e}")  # Show error dialog


class StudentApp:
    """Main GUI application class for student management system"""

    def __init__(self, root, students):
        self.root = root  # Store reference to main window
        self.students = students  # Store list of student objects
        self.root.title("Student Manager")  # Set window title
        self.root.geometry("900x550")  # Set window dimensions
        self.root.configure(bg="#D3C4E3")  # Set background color (light purple)
        self.setup_ui()  # Initialize all UI components
        self.update_student_list()  # Populate student dropdown

    def setup_ui(self):
        """Initialize and arrange all user interface components"""
        # Create main title label with styling
        tk.Label(self.root, text="Student Manager", font=("Baskerville", 35, "bold"),
                 bg="#D3C4E3", fg="#4C191B").pack(pady=10)

        # Create frame for function buttons (View, Sort, etc.)
        button_frame = tk.Frame(self.root, bg="#D3C4E3")
        button_frame.pack(pady=5)
        # Define function buttons with their commands
        buttons = [
            ("View All Records", self.view_all_records),
            ("Show Highest Score", self.show_highest_score),
            ("Show Lowest Score", self.show_lowest_score),
            ("Sort Records", self.sort_records)
        ]
        # Create and grid each function button
        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command, width=20, height=2).grid(row=0, column=i, padx=10)

        # Create frame for management buttons (Add, Delete, Update)
        management_frame = tk.Frame(self.root, bg="#D3C4E3")
        management_frame.pack(pady=5)
        mgmt_buttons = [
            ("Add Record", self.add_record),
            ("Delete Record", self.delete_record),
            ("Update Record", self.update_record)
        ]
        # Create and grid each management button
        for i, (text, command) in enumerate(mgmt_buttons):
            tk.Button(management_frame, text=text, command=command, width=15, height=2).grid(row=0, column=i, padx=10)

        # Create frame for individual student selection
        record_frame = tk.Frame(self.root, bg="#D3C4E3")
        record_frame.pack(pady=10)
        # Label for student dropdown
        tk.Label(record_frame, text="View Individual Student Record:",
                 font=("Baskerville", 12), bg="#D3C4E3", fg="#4C191B").grid(row=0, column=0, padx=0)

        self.selected_student = tk.StringVar()  # Variable to track selected student
        # Create dropdown combobox for student selection
        self.student_dropdown = ttk.Combobox(record_frame, textvariable=self.selected_student,
                                             state="readonly", width=20)
        self.student_dropdown.grid(row=0, column=1, padx=5)
        # Button to view selected student's record
        tk.Button(record_frame, text="View Record", command=self.view_individual_record).grid(row=0, column=2, padx=5)

        # Create main output text area for displaying records
        self.output_text = tk.Text(self.root, wrap="word", width=70, height=15,
                                   font=("Lato", 10), bg="#FFFFFF", fg="#4C191B")
        self.output_text.pack(pady=10)
        self.output_text.config(state="disabled")  # Make text area read-only initially

    def update_student_list(self):
        """Update the dropdown list with current student names"""
        self.student_names = [student.name for student in self.students]  # Extract names from student objects
        if hasattr(self, 'student_dropdown'):  # Check if dropdown widget exists
            self.student_dropdown['values'] = self.student_names  # Update dropdown options
            # Clear selection if selected student no longer exists
            if self.selected_student.get() not in self.student_names:
                self.selected_student.set('')  # Reset selection

    def display_student(self, student):
        """Format a student's data into a readable string for display"""
        return (f"--- Student Record ---\n"
                f"Name: {student.name}\n"  # Display student name
                f"Number: {student.code}\n"  # Display student ID
                f"Coursework Marks: {student.coursework_marks}\n"  # Show list of coursework marks
                f"Coursework Total: {student.total_coursework}\n"  # Show coursework sum
                f"Exam Mark: {student.exam_mark}\n"  # Display exam score
                f"Total Score: {student.total_score} / {MAX_TOTAL_SCORE}\n"  # Show total and maximum
                f"Overall Percentage: {student.percentage:.2f}%\n"  # Display percentage with 2 decimals
                f"Final Grade: {student.grade}\n")  # Show letter grade

    def show_output(self, content):
        """Display content in the output text area"""
        self.output_text.config(state="normal")  # Enable text widget for editing
        self.output_text.delete("1.0", tk.END)  # Clear existing content
        self.output_text.insert("1.0", content)  # Insert new content at beginning
        self.output_text.config(state="disabled")  # Make text area read-only again

    def view_all_records(self):
        """Display all student records with average percentage"""
        if not self.students:  # Check if student list is empty
            self.show_output("No student records to display.")  # Show message
            return

        output = "--- All Student Records ---\n\n"  # Initialize output string
        total_percentage = 0  # Initialize total for average calculation
        for student in self.students:  # Iterate through each student
            output += self.display_student(student) + "\n"  # Add formatted student data
            total_percentage += student.percentage  # Add to percentage total

        # Calculate and display average percentage
        avg_percentage = total_percentage / len(self.students)
        output += f"\nTotal Students: {len(self.students)}\nAverage Percentage: {avg_percentage:.2f}%"
        self.show_output(output)  # Display all content

    def view_individual_record(self):
        """Display record for the selected student"""
        selected_name = self.selected_student.get()  # Get selected student name
        if not selected_name:  # Check if no student is selected
            messagebox.showwarning("Selection Required", "Please select a student from the dropdown.")
            return

        # Find student object by name
        student = next((s for s in self.students if s.name == selected_name), None)
        if student:  # If student found
            self.show_output(self.display_student(student))  # Display their record

    def show_highest_score(self):
        """Find and display student with the highest total score"""
        if not self.students:  # Check if student list is empty
            self.show_output("No student records to check scores.")
            return

        student = max(self.students, key=lambda s: s.total_score)  # Find student with max score
        output = f"--- Student with Highest Score ({student.total_score}) ---\n"
        output += self.display_student(student)  # Add student data to output
        self.show_output(output)  # Display result

    def show_lowest_score(self):
        """Find and display student with the lowest total score"""
        if not self.students:  # Check if student list is empty
            self.show_output("No student records to check scores.")
            return

        student = min(self.students, key=lambda s: s.total_score)  # Find student with min score
        output = f"--- Student with Lowest Score ({student.total_score}) ---\n"
        output += self.display_student(student)  # Add student data to output
        self.show_output(output)  # Display result

    def sort_records(self):
        """Sort student records by total score and save to file"""
        if not self.students:  # Check if student list is empty
            self.show_output("No student records to sort.")
            return

        # Ask user for sort order preference
        answer = messagebox.askquestion("Sort Order", "Sort in descending order (highest score first)?")
        self.students.sort(key=lambda s: s.total_score, reverse=(answer == 'yes'))  # Sort students
        save_data(filename, self.students)  # Save sorted data to file
        self.update_student_list()  # Update dropdown with new order
        self.view_all_records()  # Display sorted records
        messagebox.showinfo("Success", "Student records sorted successfully.")  # Confirm success

    def add_record(self):
        """Open window to add a new student record"""
        add_window = tk.Toplevel(self.root)  # Create new window
        add_window.title("Add Student Record")  # Set window title

        fields = ["Student Code", "Name", "CW Mark 1", "CW Mark 2", "CW Mark 3", "Exam Mark"]  # Field labels
        entries = {}  # Dictionary to store entry widgets

        # Create labels and entry fields for each input
        for i, field in enumerate(fields):
            tk.Label(add_window, text=field).grid(row=i, column=0, padx=5, pady=5, sticky='w')  # Create label
            entries[field] = tk.Entry(add_window)  # Create entry field
            entries[field].grid(row=i, column=1, padx=5, pady=5)  # Position entry

        def save_new_record():
            """Validate and save new student record"""
            try:
                code = int(entries["Student Code"].get())  # Get and convert student code
                name = entries["Name"].get().strip()  # Get and clean student name
                # Get all three coursework marks
                marks = [int(entries[f"CW Mark {i + 1}"].get()) for i in range(3)]
                exam_mark = int(entries["Exam Mark"].get())  # Get exam mark

                # Validate marks are non-negative
                if any(m < 0 for m in marks + [exam_mark]):
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return
                # Check for duplicate student codes
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Input Error", f"Student Code {code} already exists.")
                    return

                self.students.append(Student(code, name, *marks, exam_mark))  # Create and add new student
                save_data(filename, self.students)  # Save updated data to file
                self.update_student_list()  # Refresh dropdown
                add_window.destroy()  # Close add window
                messagebox.showinfo("Success", "Student record added successfully.")  # Confirm success
            except ValueError:  # Handle invalid integer inputs
                messagebox.showerror("Input Error", "Please ensure all fields are valid integers.")

        # Create save button in add window
        tk.Button(add_window, text="Save Record", command=save_new_record).grid(
            row=len(fields), column=0, columnspan=2, pady=10)

    def delete_record(self):
        """Delete the selected student record"""
        selected_name = self.selected_student.get()  # Get selected student name
        if not selected_name:  # Check if no student selected
            messagebox.showwarning("Selection Required", "Please select a student to delete.")
            return

        # Confirm deletion with user
        if messagebox.askyesno("Confirm Delete", f"Delete record for {selected_name}?"):
            # Find student object by name
            student = next((s for s in self.students if s.name == selected_name), None)
            if student:  # If student found
                self.students.remove(student)  # Remove from list
                save_data(filename, self.students)  # Save updated data
                self.update_student_list()  # Refresh dropdown
                self.show_output(f"Record for {selected_name} has been deleted.")  # Confirm deletion

    def update_record(self):
        """Open window to update selected student's marks"""
        selected_name = self.selected_student.get()  # Get selected student name
        # Find student object by name
        student = next((s for s in self.students if s.name == selected_name), None)

        if not student:  # Check if student not found
            messagebox.showwarning("Selection Required", "Please select a student to update.")
            return

        update_window = tk.Toplevel(self.root)  # Create new window
        update_window.title(f"Update Record for {selected_name}")  # Set window title

        # Current field values for pre-population
        fields = {
            "Coursework Mark 1": student.coursework_marks[0],
            "Coursework Mark 2": student.coursework_marks[1],
            "Coursework Mark 3": student.coursework_marks[2],
            "Exam Mark": student.exam_mark
        }
        entries = {}  # Dictionary to store entry widgets

        # Display which student is being updated
        tk.Label(update_window, text=f"Updating: {selected_name} (Code: {student.code})").grid(
            row=0, column=0, columnspan=2, pady=5)

        # Create labels and pre-filled entry fields for each mark
        for i, (label, value) in enumerate(fields.items()):
            tk.Label(update_window, text=label).grid(row=i + 1, column=0, padx=5, pady=5, sticky='w')
            entries[label] = tk.Entry(update_window)  # Create entry field
            entries[label].insert(0, str(value))  # Pre-fill with current value
            entries[label].grid(row=i + 1, column=1, padx=5, pady=5)

        def save_updated_record():
            """Validate and save updated student marks"""
            try:
                # Get new marks from entry fields
                new_marks = [int(entries[f"Coursework Mark {i + 1}"].get()) for i in range(3)]
                new_exam_mark = int(entries["Exam Mark"].get())  # Get new exam mark

                # Validate marks are non-negative
                if any(m < 0 for m in new_marks + [new_exam_mark]):
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return

                student.coursework_marks = new_marks  # Update coursework marks
                student.exam_mark = new_exam_mark  # Update exam mark
                student.calculate_scores()  # Recalculate totals and grade

                save_data(filename, self.students)  # Save updated data
                self.update_student_list()  # Refresh dropdown
                update_window.destroy()  # Close update window
                messagebox.showinfo("Success", "Student record updated successfully.")  # Confirm success
            except ValueError:  # Handle invalid integer inputs
                messagebox.showerror("Input Error", "Please enter valid integers for marks.")

        # Create save button in update window
        tk.Button(update_window, text="Save Changes", command=save_updated_record).grid(
            row=len(fields) + 1, column=0, columnspan=2, pady=10)


# Application entry point
if __name__ == "__main__":
    filename = "/Users/fabiolazeth/Desktop/AP/ADVPROG ASSESSMENT 1/studentsMarks.txt"  # Data file path
    students = load_data(filename)  # Load student data from file
    root = tk.Tk()  # Create main application window
    app = StudentApp(root, students)  # Initialize application
    root.mainloop()
