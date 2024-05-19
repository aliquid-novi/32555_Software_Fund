import json
import os

class Admin(UniversitySystem):
    def __init__(self):
        super().__init__()

    def main(self):
        while True:
            choice = input("Admin System (c/g/p/r/s/x): ").lower()
            if choice == 'x':
                break
            elif choice == 'c':
                self.clear_database()
            elif choice == 'g':
                self.group_students()
            elif choice == 'p':
                self.partition_students()
            elif choice == 'r':
                self.remove_student()
            elif choice == 's':
                self.show_students()

    def clear_database(self):
        confirmation = input("Are you sure you want to clear the database (Y/ES/(N)O): ").lower()
        if confirmation == 'y':
            self.save_students([])
            print("Students data cleared")

    def group_students(self):
        students = self.load_students()
        grouped = {}
        for student in students:
            grade = student['grade']
            if grade not in grouped:
                grouped[grade] = []
            grouped[grade].append(student)
        
        for grade, students in grouped.items():
            print(f"{grade} --> {students}")

    def partition_students(self):
        students = self.load_students()
        pass_students = [student for student in students if student['grade'] == 'P']
        fail_students = [student for student in students if student['grade'] == 'F']

        print(f"FAIL --> {fail_students}")
        print(f"PASS --> {pass_students}")

    def remove_student(self):
        student_id = input("Remove by ID: ")
        students = self.load_students()
        students = [student for student in students if student['id'] != student_id]
        self.save_students(students)
        print(f"Removing Student {student_id} Account")

    def show_students(self):
        students = self.load_students()
        if not students:
            print("< Nothing to Display >")
        for student in students:
            print(f"{student['name']} :: {student['id']} --> Email: {student['email']}")

