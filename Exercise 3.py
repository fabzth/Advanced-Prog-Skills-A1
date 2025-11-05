import tkinter as tk
from tkinter import messagebox, ttk

MAX_TOTAL_SCORE = 160

class Student:
    def __init__(self, code, name, mark1, mark2, mark3, exam_mark):
        self.code = int(code)
        self.name = name
        self.coursework_marks = [int(mark1), int(mark2), int(mark3)]
        self.exam_mark = int(exam_mark)
        self.calculate_scores()

    def calculate_scores(self):
        self.total_coursework = sum(self.coursework_marks)
        self.total_score = self.total_coursework + self.exam_mark
        self.percentage = (self.total_score / MAX_TOTAL_SCORE) * 100
        self.grade = 'A' if self.percentage >= 70 else 'B' if self.percentage >= 60 else \
                    'C' if self.percentage >= 50 else 'D' if self.percentage >= 40 else 'F'

def load_data(filename):
    students = []
    try:
        with open(filename, 'r') as file:
            file.readline(), file.readline()
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5: parts.append('0')
                if len(parts) != 6: continue
                try:
                    if any(int(m) < 0 for m in parts[2:]): continue
                    students.append(Student(*parts))
                except ValueError:
                    continue
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found")
    return students

def save_data(filename, students):
    try:
        with open(filename, 'w') as file:
            file.write(f"{len(students)}\nID,Name,Grade1,Grade2,Grade3,ExamMark\n")
            for s in students:
                file.write(f"{s.code},{s.name},{s.coursework_marks[0]},{s.coursework_marks[1]},{s.coursework_marks[2]},{s.exam_mark}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving data: {e}")

class StudentApp:
    def __init__(self, root, students):
        self.root = root
        self.students = students
        self.root.title("Student Manager")
        self.root.geometry("900x550")
        self.root.configure(bg="#D3C4E3")
        self.setup_ui()
        self.update_student_list()

    def setup_ui(self):
        # Title
        tk.Label(self.root, text="Student Manager", font=("Baskerville", 35, "bold"),
                 bg="#D3C4E3", fg="#4C191B").pack(pady=10)

        # Function buttons
        button_frame = tk.Frame(self.root, bg="#D3C4E3")
        button_frame.pack(pady=5)
        buttons = [
            ("View All Records", self.view_all_records),
            ("Show Highest Score", self.show_highest_score),
            ("Show Lowest Score", self.show_lowest_score),
            ("Sort Records", self.sort_records)
        ]
        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command, width=20, height=2).grid(row=0, column=i, padx=10)

        # Management buttons
        management_frame = tk.Frame(self.root, bg="#D3C4E3")
        management_frame.pack(pady=5)
        mgmt_buttons = [
            ("Add Record", self.add_record),
            ("Delete Record", self.delete_record),
            ("Update Record", self.update_record)
        ]
        for i, (text, command) in enumerate(mgmt_buttons):
            tk.Button(management_frame, text=text, command=command, width=15, height=2).grid(row=0, column=i, padx=10)

        # Student selection
        record_frame = tk.Frame(self.root, bg="#D3C4E3")
        record_frame.pack(pady=10)
        tk.Label(record_frame, text="View Individual Student Record:",
                 font=("Baskerville", 12), bg="#D3C4E3", fg="#4C191B").grid(row=0, column=0, padx=0)
        
        self.selected_student = tk.StringVar()
        self.student_dropdown = ttk.Combobox(record_frame, textvariable=self.selected_student,
                                             state="readonly", width=20)
        self.student_dropdown.grid(row=0, column=1, padx=5)
        tk.Button(record_frame, text="View Record", command=self.view_individual_record).grid(row=0, column=2, padx=5)

        # Output area
        self.output_text = tk.Text(self.root, wrap="word", width=70, height=15,
                                   font=("Lato", 10), bg="#FFFFFF", fg="#4C191B")
        self.output_text.pack(pady=10)
        self.output_text.config(state="disabled")

    def update_student_list(self):
        self.student_names = [student.name for student in self.students]
        if hasattr(self, 'student_dropdown'):
            self.student_dropdown['values'] = self.student_names
            if self.selected_student.get() not in self.student_names:
                self.selected_student.set('')

    def display_student(self, student):
        return (f"--- Student Record ---\n"
                f"Name: {student.name}\n"
                f"Number: {student.code}\n"
                f"Coursework Marks: {student.coursework_marks}\n"
                f"Coursework Total: {student.total_coursework}\n"
                f"Exam Mark: {student.exam_mark}\n"
                f"Total Score: {student.total_score} / {MAX_TOTAL_SCORE}\n"
                f"Overall Percentage: {student.percentage:.2f}%\n"
                f"Final Grade: {student.grade}\n")

    def show_output(self, content):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", content)
        self.output_text.config(state="disabled")

    def view_all_records(self):
        if not self.students:
            self.show_output("No student records to display.")
            return
        output = "--- All Student Records ---\n\n"
        total_percentage = 0
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
            self.show_output(self.display_student(student))

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
        self.students.sort(key=lambda s: s.total_score, reverse=(answer == 'yes'))
        save_data(filename, self.students)
        self.update_student_list()
        self.view_all_records()
        messagebox.showinfo("Success", "Student records sorted successfully.")

    def add_record(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student Record")
        fields = ["Student Code", "Name", "CW Mark 1", "CW Mark 2", "CW Mark 3", "Exam Mark"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(add_window, text=field).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entries[field] = tk.Entry(add_window)
            entries[field].grid(row=i, column=1, padx=5, pady=5)

        def save_new_record():
            try:
                code = int(entries["Student Code"].get())
                name = entries["Name"].get().strip()
                marks = [int(entries[f"CW Mark {i + 1}"].get()) for i in range(3)]
                exam_mark = int(entries["Exam Mark"].get())
                if any(m < 0 for m in marks + [exam_mark]):
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Input Error", f"Student Code {code} already exists.")
                    return
                self.students.append(Student(code, name, *marks, exam_mark))
                save_data(filename, self.students)
                self.update_student_list()
                add_window.destroy()
                messagebox.showinfo("Success", "Student record added successfully.")
            except ValueError:
                messagebox.showerror("Input Error", "Please ensure all fields are valid integers.")

        tk.Button(add_window, text="Save Record", command=save_new_record).grid(
            row=len(fields), column=0, columnspan=2, pady=10)

    def delete_record(self):
        selected_name = self.selected_student.get()
        if not selected_name:
            messagebox.showwarning("Selection Required", "Please select a student to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete record for {selected_name}?"):
            student = next((s for s in self.students if s.name == selected_name), None)
            if student:
                self.students.remove(student)
                save_data(filename, self.students)
                self.update_student_list()
                self.show_output(f"Record for {selected_name} has been deleted.")

    def update_record(self):
        selected_name = self.selected_student.get()
        student = next((s for s in self.students if s.name == selected_name), None)
        if not student:
            messagebox.showwarning("Selection Required", "Please select a student to update.")
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
        tk.Label(update_window, text=f"Updating: {selected_name} (Code: {student.code})").grid(
            row=0, column=0, columnspan=2, pady=10)
        for i, (label, value) in enumerate(fields.items()):
            tk.Label(update_window, text=label).grid(row=i + 1, column=0, padx=5, pady=5, sticky='w')
            entries[label] = tk.Entry(update_window)
            entries[label].insert(0, str(value))
            entries[label].grid(row=i + 1, column=1, padx=5, pady=5)

        def save_updated_record():
            try:
                new_marks = [int(entries[f"Coursework Mark {i + 1}"].get()) for i in range(3)]
                new_exam_mark = int(entries["Exam Mark"].get())
                if any(m < 0 for m in new_marks + [new_exam_mark]):
                    messagebox.showerror("Input Error", "Marks must be non-negative.")
                    return
                student.coursework_marks = new_marks
                student.exam_mark = new_exam_mark
                student.calculate_scores()
                save_data(filename, self.students)
                self.update_student_list()
                update_window.destroy()
                messagebox.showinfo("Success", "Student record updated successfully.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integers for marks.")

        tk.Button(update_window, text="Save Changes", command=save_updated_record).grid(
            row=len(fields) + 1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    filename = "studentsMarks.txt"
    students = load_data(filename)
    root = tk.Tk()
    app = StudentApp(root, students)
    root.mainloop()
