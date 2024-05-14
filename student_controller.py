import json
from student import Student

class StudentController:
    def __init__(self):
        self.students = {}
        self.load_students()

    def load_students(self):
        try:
            with open('student.data', 'r') as file:
                self.students = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.students = {}

    def save_students(self):
        with open('student.data', 'w') as file:
            json.dump(self.students, file)

    def register_student(self, first_name, last_name, email, password):
        if email in self.students:
            return False, "Student already registered."
        self.students[email] = Student(first_name, last_name, email, password).__dict__
        self.save_students()
        return True, "Registration successful."

    def login_student(self, email, password):
        student = self.students.get(email)
        if student and student['password'] == password:
            return True
        return False