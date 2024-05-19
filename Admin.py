import json
import os

class Admin(UniversitySystem):
    def __init__(self):
        super().__init__()

    def main(self):
        while True:
            print("\033[94mAdmin System (c/g/p/r/s/x): \033[0m")
            choice = input().strip().lower()
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
        confirmation = input("\033[91mAre you sure you want to clear the database (Y/ES/(N)O): \033[0m").lower()
        print("\033[93mClearing students database\033[0")
        if confirmation == 'y':
            self.save_students([])
            print("\033[93mStudents data cleared\033[0m")

    def group_students(self):
        students = self.load_students()
        grouped = {}
        for student in students:
            grade = student['grade']
            if grade not in grouped:
                grouped[grade] = []
            grouped[grade].append(student)
        
        for grade, students in grouped.items():
            print("\033[93mGrade Grouping\033[0m")
            print(f"{grade} --> {student['name']} --> {student['id']} --> GRADE: {grade}")

    def partition_students(self):
        students = self.load_students()
        pass_students = [student for student in students if student['grade'] == 'P']
        fail_students = [student for student in students if student['grade'] == 'F']
        print("\033[93mPASS/FAIL Partition\033[0m")
        print(f"FAIL --> {fail_students}")
        print(f"PASS --> {pass_students}")

    def remove_student(self):
        student_id = input("Remove by ID: ")
        students = self.load_students()
        students = [student for student in students if student['id'] != student_id]
        self.save_students(students)
        print(f"\033[93mRemoving Student {student_id} Account\033[0m")

    def show_students(self):
        students = self.load_students()
        if not students:
            print("< Nothing to Display >")
        for student in students:
            print("\033[93mStudent List\033[0m")
            print(f"{student['name']} :: {student['id']} --> Email: {student['email']}")

