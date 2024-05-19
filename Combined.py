import json
import random
import os
import re
from student_controller import StudentController
from student import Student
from database import DataBase
import Student_Course_System

# DATABASE

class DataBase:
    def __init__(self, filename="student.data"):
        self.filename = filename
        self.check_and_create_file()

    def check_and_create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write(json.dumps({"students": {}, "used_ids": []}))  # Initialize with empty data
            print(f"File '{self.filename}' created.")
        else:
            print(f"File '{self.filename}' already exists.")

    def write(self, data):
        with open(self.filename, 'w') as fileHandler:
            json.dump(data, fileHandler, indent=2)
        print(f"Data written to {self.filename}")

    def read(self):
        try:
            with open(self.filename, 'r') as fileHandler:
                return json.load(fileHandler)
        except json.JSONDecodeError:
            print("Error: File contains invalid JSON.")
            return {"students": {}, "used_ids": []}
        except FileNotFoundError:
            print(f"File '{self.filename}' does not exist.")
            return {"students": {}, "used_ids": []}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"students": {}, "used_ids": []}
        
# STUDENT CLASS
class Student:
    def __init__(self, first_name, last_name, email, password, student_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.student_id = student_id


# UNIVERSITY SYSTEM + STUDENT L/R/X MENU + COURSE ENROLLMENT- DONE
## add ADMIN SYSTEM 
class UniversitySystem:
    def __init__(self):
        self.controller = StudentController()
        self.running = True

    def main_menu(self):
        while self.running:
            print("\033[96mUniversity System: (A)dmin, (S)tudent, or (X) :\033[0m ", end="")  # blue color
            choice = input().strip().upper()

            if choice == 'A':
                self.admin_menu()
            elif choice == 'S':
                self.student_menu()
            elif choice == 'X':
                self.running = False
                print("\033[93mThank You\033[0m")  # yellow color
            else:
                print("Invalid choice, please try again.")

    #ADMIN SYSTEM
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

    def student_menu(self):
        student_running = True
        while student_running:
            print("     \033[96mStudent System (l/r/x):\033[0m ", end="")  # blue color + indent
            command = input().strip().lower()

            if command == 'x':
                print("\033[93mThank you\033[0m")  # Yellow color for "Thank you"
                student_running = False

            elif command == 'l':
                print("     \033[92mStudent Sign In\033[0m")
                email = input("     Enter your email: ").strip()
                password = input("     Enter your password: ").strip()

                if not re.match(r'^[A-Z][a-zA-Z]{5,}\d{3,}$', password) or not re.match(r'^([a-zA-Z]+)\.([a-zA-Z]+)@university\.com$', email):
                    print("     \033[91mIncorrect email or password format\033[0m")
                else:
                    success, message = self.controller.login_student(email, password)
                    if success:
                        print("     \033[92mLogin successful!\033[0m")
                        course_sys = Student_Course_System.StuCourseSys(email) 
                        course_sys.main()
                    else:
                        print("     \033[91m" + message + "\033[0m")

            elif command == 'r':
                print("     \033[92mStudent Sign Up\033[0m")
                email = input("     Enter your email: ").strip()
                password = input("     Enter your password: ").strip()

                if not re.match(r'^[A-Z][a-zA-Z]{5,}\d{3,}$', password) or not re.match(r'^([a-zA-Z]+)\.([a-zA-Z]+)@university\.com$', email):
                    print("     \033[91mIncorrect email or password format\033[0m")
                else:
                    try:
                        firstname, lastname = email.split('@')[0].split('.')
                        success, message = self.controller.register_student(firstname, lastname, email, password)
                        if success:
                            print("     \033[93m{}".format(message), "\033[0m")
                        else:
                            print("     \033[91m" + message + "\033[0m")
                    except ValueError:
                        print("     \033[91mIncorrect email or password format\033[0m")
            else:
                print("     \033[91mInvalid command. Please enter 'l' to login, 'r' to register, or 'x' to exit.\033[0m")

if __name__ == "__main__":
    system = UniversitySystem()
    system.main_menu()
           




