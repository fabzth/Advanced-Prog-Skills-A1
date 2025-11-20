import tkinter as tk
from tkinter import messagebox, ttk  # Import GUI components and dialog boxes

MAX_TOTAL_SCORE = 160  # Maximum possible score for grading calculation
# coursework (60) and exam (100) scores

class Student:
    """Represents a student with marks and calculates grades"""

    def __init__(self, code, name, mark1, mark2, mark3, exam_mark):
        self.code = int(code)  # Convert student ID to integer
        self.name = name  # Store student name
        self.coursework_marks = [int(mark1), int(mark2), int(mark3)]  # Store coursework marks as list
        self.exam_mark = int(exam_mark)  # Convert exam mark to integer
        self.calculate_scores()  # Auto-calculate totals and grade on creation

    def calculate_scores(self):
        """Calculate total scores, percentage and determine letter grade"""
        self.total_coursework = sum(self.coursework_marks)  # Sum all coursework marks
        self.total_score = self.total_coursework + self.exam_mark  # Calculate total score
        self.percentage = (self.total_score / MAX_TOTAL_SCORE) * 100  # Calculate percentage
        # Determine grade based on percentage ranges
        self.grade = 'A' if self.percentage >= 70 else 'B' if self.percentage >= 60 else 'C' if self.percentage >= 50 else 'D' if self.percentage >= 40 else 'F'

# ensures only valid students are loaded
def load_data(filename):
    """Load student data from CSV file and create Student objects"""
    students = []  # Initialize empty list for student objects
    try:
        with open(filename, 'r') as file:  # Open file for reading
            file.readline(), file.readline()  # Skip header lines
            for line in file:  # Process each data line
                parts = line.strip().split(',')  # Split line into components
                if len(parts) == 5: parts.append('0')  # Add default exam mark if missing
                if len(parts) != 6: continue  # Skip invalid lines
                try:
                    if any(int(m) < 0 for m in parts[2:]): continue  # Skip negative marks
                    students.append(Student(*parts))  # Create and add student object
                except ValueError:  # Handle invalid number format
                    continue
    except FileNotFoundError:  # Handle missing file error
        messagebox.showerror("Error", f"File '{filename}' not found") # user-friendly error messages
    return students  # Return list of student objects


def save_data(filename, students):
    """Save student data back to CSV file"""
    try:
        with open(filename, 'w') as file:  # Open file for writing
            file.write(f"{len(students)}\nID,Name,Grade1,Grade2,Grade3,ExamMark\n")  # Write header
            for s in students:  # Write each student's data
                file.write(
                    f"{s.code},{s.name},{s.coursework_marks[0]},{s.coursework_marks[1]},{s.coursework_marks[2]},{s.exam_mark}\n")
    except Exception as e:  # Handle file write errors
        messagebox.showerror("Save Error", f"Error saving data: {e}")


class StudentApp:
    """Main GUI app for student management"""
    def __init__(self, root, students):
        self.root = root  # Store main window reference
        self.students = students  # Store student data
        self.root.title("Student Manager")  # Set window title
        self.root.geometry("900x550")  # Set window size
        self.root.configure(bg="#D3C4E3")  # Set background color
        self.setup_ui()  # Initialize user interface
        self.update_student_list()  # Populate student dropdown

    def setup_ui(self):
        """Initialize and arrange all UI components"""
        # Create main title label
        tk.Label(self.root, text="Student Manager", font=("Baskerville", 35, "bold"), bg="#D3C4E3", fg="#4C191B").pack(
            pady=10)

        # Create function buttons frame
        button_frame = tk.Frame(self.root, bg="#D3C4E3")
        button_frame.pack(pady=5)
        # Add function buttons
        buttons = [("View All Records", self.view_all_records), ("Show Highest Score", self.show_highest_score),
                   ("Show Lowest Score", self.show_lowest_score), ("Sort Records", self.sort_records)]
        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command, width=20, height=2).grid(row=0, column=i, padx=10)

        # Create management buttons frame
        management_frame = tk.Frame(self.root, bg="#D3C4E3")
        management_frame.pack(pady=5)
        mgmt_buttons = [("Add Record", self.add_record), ("Delete Record", self.delete_record),
                        ("Update Record", self.update_record)]
        for i, (text, command) in enumerate(mgmt_buttons):
            tk.Button(management_frame, text=text, command=command, width=15, height=2).grid(row=0, column=i, padx=10)

        # Create student selection frame
        record_frame = tk.Frame(self.root, bg="#D3C4E3")
        record_frame.pack(pady=10)
        tk.Label(record_frame, text="View Individual Student Record:", font=("Baskerville", 12), bg="#D3C4E3",
                 fg="#4C191B").grid(row=0, column=0, padx=0)

        self.selected_student = tk.StringVar()  # Variable for selected student
        self.student_dropdown = ttk.Combobox(record_frame, textvariable=self.selected_student, state="readonly",
                                             width=20)  # Student dropdown
        self.student_dropdown.grid(row=0, column=1, padx=5)
        tk.Button(record_frame, text="View Record", command=self.view_individual_record).grid(row=0, column=2,
                                                                                              padx=5)  # View button

        # Create main output text area
        self.output_text = tk.Text(self.root, wrap="word", width=70, height=15, font=("Lato", 10), bg="#FFFFFF",
                                   fg="#4C191B")
        self.output_text.pack(pady=10)
        self.output_text.config(state="disabled")  # Make read-only

    def update_student_list(self):
        """Update the dropdown list with current student names"""
        self.student_names = [student.name for student in self.students]  # Extract names
        if hasattr(self, 'student_dropdown'):
            self.student_dropdown['values'] = self.student_names  # Update dropdown
            if self.selected_student.get() not in self.student_names:
                self.selected_student.set('')  # Clear invalid selection

    def display_student(self, student):
        """Format student data for display"""
        return (f"--- Student Record ---\nName: {student.name}\nNumber: {student.code}\n"
                f"Coursework Marks: {student.coursework_marks}\nCoursework Total: {student.total_coursework}\n"
                f"Exam Mark: {student.exam_mark}\nTotal Score: {student.total_score} / {MAX_TOTAL_SCORE}\n"
                f"Overall Percentage: {student.percentage:.2f}%\nFinal Grade: {student.grade}\n")

    def show_output(self, content):
        """Display content in output text area"""
        self.output_text.config(state="normal")  # Enable editing
        self.output_text.delete("1.0", tk.END)  # Clear current content
        self.output_text.insert("1.0", content)  # Insert new content
        self.output_text.config(state="disabled")  # Make read-only again to prevent user editing

    def view_all_records(self):
        """Display all student records with average percentage"""
        if not self.students:  # Check for empty list
            self.show_output("No student records to display.")
            return
        output = "--- All Student Records ---\n\n"  # Initialize output
        total_percentage = 0  # Initialize total
        for student in self.students:  # Process each student
            output += self.display_student(student) + "\n"  # Add student data
            total_percentage += student.percentage  # Accumulate percentage
        # Calculate and display average
        avg_percentage = total_percentage / len(self.students)
        output += f"\nTotal Students: {len(self.students)}\nAverage Percentage: {avg_percentage:.2f}%"
        self.show_output(output)  # Display all content

    def view_individual_record(self):
        """Display record for selected student"""
        selected_name = self.selected_student.get()  # Get selected name
        if not selected_name:  # Check if selection exists
            messagebox.showwarning("Selection Required", "Please select a student from the dropdown.")
            return
        # Find student by name
        student = next((s for s in self.students if s.name == selected_name), None)
        if student:
            self.show_output(self.display_student(student))  # Display record

    def show_highest_score(self):
        """Find and display student with highest total score"""
        if not self.students:  # Check for empty list
            self.show_output("No student records to check scores.")
            return
        student = max(self.students, key=lambda s: s.total_score)  # Find max score
        output = f"--- Student with Highest Score ({student.total_score}) ---\n"
        output += self.display_student(student)  # Add student data
        self.show_output(output)  # Display result

    def show_lowest_score(self):
        """Find and display student with lowest total score"""
        if not self.students:  # Check for empty list
            self.show_output("No student records to check scores.")
            return
        student = min(self.students, key=lambda s: s.total_score)  # Find min score
        output = f"--- Student with Lowest Score ({student.total_score}) ---\n"
        output += self.display_student(student)  # Add student data
        self.show_output(output)  # Display result

    def sort_records(self):
        """Sort student records by total score and save to file"""
        if not self.students:  # Check for empty list
            self.show_output("No student records to sort.")
            return
        # Ask for sort order preference
        answer = messagebox.askquestion("Sort Order", "Sort in descending order (highest score first)?")
        self.students.sort(key=lambda s: s.total_score, reverse=(answer == 'yes'))  # Sort students
        save_data(filename, self.students)  # Save sorted data
        self.update_student_list()  # Update dropdown
        self.view_all_records()  # Display sorted records
        messagebox.showinfo("Success", "Student records sorted successfully.")  # Confirm

    def add_record(self):
        """Open window to add new student record"""
        add_window = tk.Toplevel(self.root)  # Create new window
        add_window.title("Add Student Record")  # Set window title
        fields = ["Student Code", "Name", "CW Mark 1", "CW Mark 2", "CW Mark 3", "Exam Mark"]  # Field labels
        entries = {}  # Dictionary for entry widgets

        for i, field in enumerate(fields):  # Create input fields
            tk.Label(add_window, text=field).grid(row=i, column=0, padx=5, pady=5, sticky='w')  # Label
            entries[field] = tk.Entry(add_window)  # Entry field
            entries[field].grid(row=i, column=1, padx=5, pady=5)  # Position field

        def save_new_record():
            """Validate and save new student record"""
            try:
                code = int(entries["Student Code"].get())  # Get student code
                name = entries["Name"].get().strip()  # Get student name
                marks = [int(entries[f"CW Mark {i + 1}"].get()) for i in range(3)]  # Get coursework marks
                exam_mark = int(entries["Exam Mark"].get())  # Get exam mark
                if any(m < 0 for m in marks + [exam_mark]):  # Validate non-negative marks
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return
                if any(s.code == code for s in self.students):  # Check for duplicate codes
                    messagebox.showerror("Input Error", f"Student Code {code} already exists.")
                    return
                self.students.append(Student(code, name, *marks, exam_mark))  # Add new student
                save_data(filename, self.students)  # Save data
                self.update_student_list()  # Refresh dropdown
                add_window.destroy()  # Close window
                messagebox.showinfo("Success", "Student record added successfully.")  # Confirm
            except ValueError:  # Handle invalid inputs
                messagebox.showerror("Input Error", "Please ensure all fields are valid integers.")

        tk.Button(add_window, text="Save Record", command=save_new_record).grid(  # Save button
            row=len(fields), column=0, columnspan=2, pady=10)

    def delete_record(self):
        """Delete selected student record"""
        selected_name = self.selected_student.get()  # Get selected name
        if not selected_name:  # Check selection
            messagebox.showwarning("Selection Required", "Please select a student to delete.")
            return
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Delete record for {selected_name}?"):
            student = next((s for s in self.students if s.name == selected_name), None)  # Find student
            if student:
                self.students.remove(student)  # Remove from list
                save_data(filename, self.students)  # Save data
                self.update_student_list()  # Refresh dropdown
                self.show_output(f"Record for {selected_name} has been deleted.")  # Confirm

    def update_record(self):
        """Open window to update selected student's marks"""
        selected_name = self.selected_student.get()  # Get selected name
        student = next((s for s in self.students if s.name == selected_name), None)  # Find student
        if not student:  # Check if student exists
            messagebox.showwarning("Selection Required", "Please select a student to update.")
            return

        update_window = tk.Toplevel(self.root)  # Create update window
        update_window.title(f"Update Record for {selected_name}")  # Set title
        # Current field values
        fields = {"Coursework Mark 1": student.coursework_marks[0], "Coursework Mark 2": student.coursework_marks[1],
                  "Coursework Mark 3": student.coursework_marks[2], "Exam Mark": student.exam_mark}
        entries = {}  # Dictionary for entry widgets

        tk.Label(update_window, text=f"Updating: {selected_name} (Code: {student.code})").grid(  # Display info
            row=0, column=0, columnspan=2, pady=10)

        for i, (label, value) in enumerate(fields.items()):  # Create input fields
            tk.Label(update_window, text=label).grid(row=i + 1, column=0, padx=5, pady=5, sticky='w')  # Label
            entries[label] = tk.Entry(update_window)  # Entry field
            entries[label].insert(0, str(value))  # Pre-fill with current value
            entries[label].grid(row=i + 1, column=1, padx=5, pady=5)  # Position field

        def save_updated_record():
            """Validate and save updated student marks"""
            try:
                new_marks = [int(entries[f"Coursework Mark {i + 1}"].get()) for i in range(3)]  # Get new marks
                new_exam_mark = int(entries["Exam Mark"].get())  # Get new exam mark
                if any(m < 0 for m in new_marks + [new_exam_mark]):  # Validate non-negative
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return
                student.coursework_marks = new_marks  # Update coursework marks
                student.exam_mark = new_exam_mark  # Update exam mark
                student.calculate_scores()  # Recalculate scores
                save_data(filename, self.students)  # Save data
                self.update_student_list()  # Refresh dropdown
                update_window.destroy()  # Close window
                messagebox.showinfo("Success", "Student record updated successfully.")  # Confirm
            except ValueError:  # Handle invalid inputs
                messagebox.showerror("Input Error", "Please enter valid integers for marks.")

        tk.Button(update_window, text="Save Changes", command=save_updated_record).grid(  # Save button
            row=len(fields) + 1, column=0, columnspan=2, pady=10)


# PROGRAM STARTUP- app entry point
if __name__ == "__main__":
    filename = "studentsMarks.txt"  # Data file path
    students = load_data(filename)  # Load student data
    root = tk.Tk()  # Create main window
    app = StudentApp(root, students)  # Initialize application
    root.mainloop()
