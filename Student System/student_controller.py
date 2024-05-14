import json
import random
from student import Student

class StudentController:
    def __init__(self):
        self.students = {}
        self.used_ids = set()
        self.load_students()

    def load_students(self):
        try:
            with open('student.data', 'r') as file:
                data = json.load(file)
                # 确保数据包含所需的键
                self.students = data.get("students", {})
                self.used_ids = set(data.get("used_ids", []))
        except FileNotFoundError:
            # 文件不存在时，初始化空字典和集合
            self.students = {}
            self.used_ids = set()
        except json.JSONDecodeError:
            # 文件不是有效的JSON格式时，也进行相同的初始化
            self.students = {}
            self.used_ids = set()

    def save_students(self):
        with open('student.data', 'w') as file:
            data = {"students": self.students, "used_ids": list(self.used_ids)}
            json.dump(data, file)

    def generate_student_id(self):
        while True:
            student_id = random.randint(100000, 999999)
            if student_id not in self.used_ids:
                self.used_ids.add(student_id)
                return f"{student_id:06d}"

    def register_student(self, first_name, last_name, email, password):
        if email in self.students:
            return False, "Student already registered."
        student_id = self.generate_student_id()
        self.students[email] = Student(first_name, last_name, email, password, student_id).__dict__
        self.save_students()
        return True, f"Registration successful. Your student ID is {student_id}."

    def login_student(self, email, password):
        student = self.students.get(email)
        if student and student['password'] == password:
            return True, "Login successful."
        return False, "Invalid email or password."