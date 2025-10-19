import tkinter as tk
from tkinter import messagebox, ttk

# Define the maximum possible score for correct calculation
MAX_TOTAL_SCORE = 160

# Student class to define and manage student records
class Student:
    def __init__(self, code, name, mark1, mark2, mark3, exam_mark):
        # Ensure all numerical data is stored as integers
        self.code = int(code)
        self.name = name
        self.coursework_marks = [int(mark1), int(mark2), int(mark3)]
        self.exam_mark = int(exam_mark)
        self.calculate_scores()

    def calculate_scores(self):
        self.total_coursework = sum(self.coursework_marks)
        self.total_score = self.total_coursework + self.exam_mark
        
        # Calculate percentage using the defined max score
        self.percentage = (self.total_score / MAX_TOTAL_SCORE) * 100
        self.grade = self.get_grade()

    def get_grade(self): #Determines the letter grade
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

# Data I/O functions
def load_data(filename):
    students = []
    try:
        with open(filename, 'r') as file:
            # Skip the first two lines: student count and header line
            file.readline()
            file.readline()
                
            for line_num, line in enumerate(file, start=3):
                parts = line.strip().split(',')
                
                if len(parts) == 5:
                    parts.append('0')
                elif len(parts) != 6:
                    print(f"Warning: Line {line_num} malformed: {line.strip()} (expected 5 or 6 parts, got {len(parts)})")
                    continue

                code, name, mark1, mark2, mark3, exam_mark = parts
                
                try:
                    # Basic validation: ensure marks are non-negative
                    if any(int(m) < 0 for m in [mark1, mark2, mark3, exam_mark]):
                         print(f"Warning: Line {line_num} has negative mark and was skipped.")
                         continue
                        
                    students.append(Student(code, name, mark1, mark2, mark3, exam_mark))
                except ValueError:
                    print(f"Warning: Line {line_num} has invalid data types and was skipped.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"Data file '{filename}' not found. Please check the path.")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading data: {e}")
    return students

def save_data(filename, students): #Saves data back to the file with student count and header
    try:
        with open(filename, 'w') as file:
            # Re-write the correct header lines
            file.write(f"{len(students)}\n")
            file.write("ID,Name,Grade1,Grade2,Grade3,ExamMark\n")
            
            for student in students:
                # Ensure the saved data matches the expected 6-part format
                line = f"{student.code},{student.name},{student.coursework_marks[0]},{student.coursework_marks[1]},{student.coursework_marks[2]},{student.exam_mark}\n"
                file.write(line)
        print("Data saved successfully.")
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving data: {e}")

# Main Tkinter Application Class
class StudentApp:
    def __init__(self, root, students):
        self.root = root
        self.students = students
        self.root.title("Student Manager")
        self.root.geometry("900x550")
        self.root.configure(bg="#D3C4E3")

        tk.Label(self.root, text="Student Manager", font=("Baskerville", 35, "bold"), bg="#D3C4E3", fg="#4C191B").pack(pady=10)

        # Buttons Frame (Row 0 & 1)
        button_frame = tk.Frame(self.root, bg="#D3C4E3")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="View All Records", command=self.view_all_records, width=20, height=2).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Show Highest Score", command=self.show_highest_score, width=20, height=2).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Show Lowest Score", command=self.show_lowest_score, width=20, height=2).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Sort Records", command=self.sort_records, width=20, height=2).grid(row=0, column=3, padx=10)
        
        # Management Buttons Frame (Row 2)
        management_frame = tk.Frame(self.root, bg="#D3C4E3")
        management_frame.pack(pady=5)
        
        tk.Button(management_frame, text="Add Record", command=self.add_record, width=15, height=2).grid(row=0, column=0, padx=10)
        tk.Button(management_frame, text="Delete Record", command=self.delete_record, width=15, height=2).grid(row=0, column=1, padx=10)
        tk.Button(management_frame, text="Update Record", command=self.update_record, width=15, height=2).grid(row=0, column=2, padx=10)


        # Dropdown for individual student view
        record_frame = tk.Frame(self.root, bg="#D3C4E3")
        record_frame.pack(pady=10)
        tk.Label(record_frame, text="View Individual Student Record:", font=("Baskerville", 12), bg="#D3C4E3", fg="#4C191B").grid(row=0, column=0, padx=0)

        self.selected_student = tk.StringVar()
        self.update_student_list()
        # Student dropdown setup
        self.student_dropdown = ttk.Combobox(record_frame, textvariable=self.selected_student, values=self.student_names, state="readonly", width=20)
        self.student_dropdown.grid(row=0, column=1, padx=5)

        tk.Button(record_frame, text="View Record", command=self.view_individual_record).grid(row=0, column=2, padx=5)

        # Text area for output
        self.output_text = tk.Text(self.root, wrap="word", width=70, height=15, font=("Lato", 10))
        self.output_text.pack(pady=10)
        self.output_text.config(state="disabled", bg="#FFFFFF", fg="#4C191B")

    def update_student_list(self): #Updates the internal list of student names and synchronizes the dropdown widget
        self.student_names = [student.name for student in self.students]
        
        # Synchronization fix: Update the dropdown's values
        if hasattr(self, 'student_dropdown'):
            self.student_dropdown['values'] = self.student_names
            # Clear selection if the student is no longer in the list
            if self.selected_student.get() and self.selected_student.get() not in self.student_names:
                self.selected_student.set('')

    def display_student(self, student):
        return (
            f"--- Student Record ---\n"
            f"Name: {student.name}\n"
            f"Number: {student.code}\n"
            f"Coursework Marks: {student.coursework_marks}\n"
            f"Coursework Total: {student.total_coursework}\n"
            f"Exam Mark: {student.exam_mark}\n"
            f"Total Score: {student.total_score} / {MAX_TOTAL_SCORE}\n"
            f"Overall Percentage: {student.percentage:.2f}%\n"
            f"Final Grade: {student.grade}\n"
        )

    # --- Core Functionality Methods ---

    def view_all_records(self):
        if not self.students:
            self.show_output("No student records to display.")
            return

        total_percentage = 0
        output = "--- All Student Records ---\n\n"
        for student in self.students:
            output += self.display_student(student) + "\n"
            total_percentage += student.percentage
            
        avg_percentage = total_percentage / len(self.students)
        output += f"\nTotal Students: {len(self.students)}\nAverage Percentage: {avg_percentage:.2f}%"
        self.show_output(output)

    def view_individual_record(self):
        selected_name = self.selected_student.get()
        if not selected_name:
            messagebox.showwarning("Selection Required", "Please select a student from the dropdown.")
            return

        student = next((s for s in self.students if s.name == selected_name), None)
        if student:
            output = self.display_student(student)
            self.show_output(output)

    def show_highest_score(self):
        if not self.students:
            self.show_output("No student records to check scores.")
            return
            
        student = max(self.students, key=lambda s: s.total_score)
        output = f"--- Student with Highest Score ({student.total_score}) ---\n"
        output += self.display_student(student)
        self.show_output(output)

    def show_lowest_score(self):
        if not self.students:
            self.show_output("No student records to check scores.")
            return
            
        student = min(self.students, key=lambda s: s.total_score)
        output = f"--- Student with Lowest Score ({student.total_score}) ---\n"
        output += self.display_student(student)
        self.show_output(output)

    def sort_records(self):
        if not self.students:
            self.show_output("No student records to sort.")
            return
            
        answer = messagebox.askquestion("Sort Order", "Sort in descending order (highest score first)?")
        reverse_order = True if answer == 'yes' else False
        
        self.students.sort(key=lambda s: s.total_score, reverse=reverse_order)
        save_data(filename, self.students) # Save the new order
        
        self.update_student_list()
        self.view_all_records()
        messagebox.showinfo("Success", "Student records sorted successfully.")

    # --- Management Methods ---
    
    def add_record(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student Record")
        fields = ["Student Code (int)", "Name", "CW Mark 1 (int)", "CW Mark 2 (int)", "CW Mark 3 (int)", "Exam Mark (int)"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(add_window, text=field).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entries[field] = tk.Entry(add_window)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def save_new_record():
            try:
                code = int(entries["Student Code (int)"].get())
                name = entries["Name"].get().strip()
                marks = [int(entries[f"CW Mark {i+1} (int)"].get()) for i in range(3)]
                exam_mark = int(entries["Exam Mark (int)"].get())
                
                # Check for negative marks or duplicate codes
                if any(m < 0 for m in marks) or exam_mark < 0:
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Input Error", f"Student Code {code} already exists.")
                    return
                    
                new_student = Student(code, name, *marks, exam_mark)
                self.students.append(new_student)
                save_data(filename, self.students)
                self.update_student_list()
                add_window.destroy()
                messagebox.showinfo("Success", "Student record added successfully.")
            except ValueError:
                messagebox.showerror("Input Error", "Please ensure all numerical fields are valid integers.")

        tk.Button(add_window, text="Save Record", command=save_new_record).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_record(self):
        selected_name = self.selected_student.get()
        if not selected_name:
            messagebox.showwarning("Selection Required", "Please select a student from the dropdown to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the record for {selected_name}?")
        if confirm:
            student = next((s for s in self.students if s.name == selected_name), None)
            if student:
                self.students.remove(student)
                save_data(filename, self.students)
                self.update_student_list()
                self.show_output(f"Record for {selected_name} has been deleted.")
            else:
                messagebox.showerror("Error", "Student not found in list.")

    def update_record(self):
        selected_name = self.selected_student.get()
        student = next((s for s in self.students if s.name == selected_name), None)
        
        if not student:
            messagebox.showwarning("Selection Required", "Please select a student from the dropdown to update.")
            return
            
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Record for {selected_name}")
        
        fields = {
            "Coursework Mark 1": student.coursework_marks[0],
            "Coursework Mark 2": student.coursework_marks[1],
            "Coursework Mark 3": student.coursework_marks[2],
            "Exam Mark": student.exam_mark
        }
        entries = {}
        row_start = 1
        tk.Label(update_window, text=f"Updating: {selected_name} (Code: {student.code})").grid(row=0, column=0, columnspan=2, pady=5)
        
        for i, (label, value) in enumerate(fields.items()):
            tk.Label(update_window, text=label).grid(row=row_start + i, column=0, padx=5, pady=5, sticky='w')
            entry = tk.Entry(update_window)
            entry.insert(0, str(value))
            entry.grid(row=row_start + i, column=1, padx=5, pady=5)
            entries[label] = entry

        def save_updated_record():
            try:
                new_marks = [int(entries[f"Coursework Mark {i+1}"].get()) for i in range(3)]
                new_exam_mark = int(entries["Exam Mark"].get())

                if any(m < 0 for m in new_marks) or new_exam_mark < 0:
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return

                # Update the existing student object's attributes and recalculate scores
                student.coursework_marks = new_marks
                student.exam_mark = new_exam_mark
                student.calculate_scores()

                save_data(filename, self.students)
                self.update_student_list()
                self.view_all_records()
                update_window.destroy()
                messagebox.showinfo("Success", "Student record updated successfully.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integers for the marks.")

        tk.Button(update_window, text="Save Changes", command=save_updated_record).grid(row=row_start + len(fields), column=0, columnspan=2, pady=10)

    # --- Utility Methods ---

    def show_output(self, content):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", content)
        self.output_text.config(state="disabled")

# --- Application Entry Point ---
if __name__ == "__main__":
    filename = "/Users/fabiolazeth/Desktop/ADVPROG/ADVPROG ASSESSMENT 1/studentMarks.txt"

    students = load_data(filename)
    root = tk.Tk()
    app = StudentApp(root, students)
    root.mainloop()