import json
import random
import os
import re
from student_controller import StudentController
from student import Student
from database import DataBase

# DATABASE

class DataBase:
    def __init__(self, filename="students.data"):
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


# UNIVERSITY SYSTEM + STUDENT L/R/X MENU - DONE
## add ADMIN SYSTEM + COURSE ENROLLMENT
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

    def admin_menu(self):
        admin_running = True
        while admin_running:
            print("     \033[96mAdmin System (c/g/p/r/s/x):\033[0m ", end="")  # blue color + indent
            choice = input().strip().lower()
            if choice == 'x':
                admin_running = False

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
                        # student_course_menu()  # Future integration point for course management
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
           




