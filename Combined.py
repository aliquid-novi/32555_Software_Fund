import json
import random
import os
import re
from student_controller import StudentController
from database import DataBase
import Student_Course_System
from Student_Course_System import SubjectClass as SC
import Admin
# DATABASE
import sys

# Direct path setting
sys.path.append(r'C:\Users\markp\OneDrive\Documents\GitHub\Uni Work\32555 - Fund._of_Software_Dev\32555_Software_Fund\GUI')

from data_manager import DataManager

class DataBase:
    def __init__(self, filename="student.data"):
        self.filename = filename
        self.dm = DataManager(filename)
        self.ensure_file_ready(silent=True)  # Call with a silent flag to avoid repetitive prints

    def ensure_file_ready(self, silent=False):
        if not os.path.exists(self.filename):
            self.initialize_file()
        elif not silent:
            print(f"File '{self.filename}' ready.")

    def initialize_file(self):
        with open(self.filename, 'w') as file:
            file.write(json.dumps({"students": {}, "used_ids": []}))
            print(f"File '{self.filename}' created.")

    def write(self, data):
        with open(self.filename, 'w') as fileHandler:
            json.dump(data, fileHandler, indent=2)
            print(f"Data written to {self.filename}")

    def read(self):
        try:
            with open(self.filename, 'r') as fileHandler:
                return json.load(fileHandler)
        except json.JSONDecodeError:
            print("Error: JSON file contains invalid JSON.")
            return {"students": {}, "used_ids": []}
        except FileNotFoundError:
            print(f"File '{self.filename}' does not exist.")
            return {"students": {}, "used_ids": []}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"students": {}, "used_ids": []}

    def list_students(self):
        data = self.dm.load_data()  # Load the most recent student data
        student_list = []

        for student in data.get('students', {}).values():
            # Format each student's information
            student_info = f"{student['first_name']} {student['last_name']} :: {student['student_id']} ---> Email: {student['email']}"
            student_list.append(student_info)

        # Optionally, sort the student list alphabetically by name
        student_list.sort()

        # Print or return the formatted student list
        return student_list
    
    def group_students_by_grade(self):
        data = self.dm.load_data()  # Ensures you are working with the latest data
        grade_groups = {'HD': [], 'D': [], 'C': [], 'P': [], 'F': []}

        for student in data.get('students', {}).values():
            if 'subjects' not in student:
                continue
            total_marks = sum(int(subject['mark']) for subject in student.get('subjects', []))
            average_mark = round(total_marks / len(student['subjects'])) if student['subjects'] else 0
            grade = SubjectClass.Classify_Results(average_mark)
            name = f"{student['first_name']} {student['last_name']}"
            stu_id = student['student_id']
            student_info = f"{name} : {stu_id} --> GRADE: {grade} - MARK: {average_mark}"

            if grade in grade_groups:
                grade_groups[grade].append(student_info)

        # Update the data with new grade groups
        if 'grade_groups' not in data:
            data['grade_groups'] = {}
        data['grade_groups'] = grade_groups
        self.dm.save_data(data)  # Saving the updated data
    
        return grade_groups

    def get_pass_fail(self):
        data = self.dm.load_data()  # Ensures you are working with the latest data
        pass_results = []
        fail_results = []

        for student in data.get('students', {}).values():
            if 'subjects' not in student:
                continue
            total_marks = sum(int(subject['mark']) for subject in student.get('subjects', []))
            average_mark = round(total_marks / len(student['subjects']))
            grade = SC.Classify_Results(average_mark)
            name = f"{student['first_name']} {student['last_name']}"
            stu_id = student['student_id']
            result_entry = f"{name} :: {stu_id} --> GRADE:  {grade} - MARK: {average_mark}"
            
            if average_mark >= 50:
                pass_results.append(result_entry)
            else:
                fail_results.append(result_entry)

        # Update the data with new results
        if 'results' not in data:
            data['results'] = {}
        data['results']['PASS'] = pass_results
        data['results']['FAIL'] = fail_results
        self.dm.save_data(data)  # Saving the updated data
        
        return data['results']
    
    def remove_student_by_id(self, student_id):
        data = self.read()
        stu_data = data['students']
        stu_ids = data['used_ids']
        
        # Ensure student_id is a string for consistent handling
        student_id = str(student_id)

        # Check and remove the student from students dictionary
        student_to_remove = None
        for student_email, details in stu_data.items():
            if details['student_id'] == student_id:
                student_to_remove = student_email
                break

        if student_to_remove:
            # Remove the student from the dictionary
            del stu_data[student_to_remove]
            # Try to remove student_id from used_ids
            try:
                
                stu_ids = [str(id) for id in stu_ids] # List comprehension 
                stu_ids.remove(student_id)
                data['students'] = stu_data  
                data['used_ids'] = [int(id) for id in stu_ids]  # List comprehension 
                db.write(data)  # Write data back to file
                return True
            except ValueError:
                print(f"Error: ID {student_id} not found in the used_ids list.")
        return False

    def clear_all_students(self):
        self.write({"students": {}, "used_ids": []})

        
# STUDENT CLASS
class Student:
    def __init__(self, first_name, last_name, email, password, student_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.student_id = student_id

# University Class (main)
class UniversitySystem:
    def __init__(self):
        self.db = DataBase()
        self.controller = StudentController()
        self.admin_system = Admin.AdminSystem(self.db)
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
            print("\033[96mAdmin System (c/g/p/r/s/x):\033[0m ", end="")
            choice = input().strip().lower()
            if choice == 'c':
                self.admin_system.clear_students()
            elif choice == 'g':
                self.admin_system.group_students()
            elif choice == 'p':
                self.admin_system.partition_students()
            elif choice == 'r':
                self.admin_system.remove_student()
            elif choice == 's':
                self.admin_system.show_students()
            elif choice == 'x':
                print("Exiting admin system.")
                admin_running = False
            else:
                print("Invalid option, please try again.")

    def invalid_command(self):
        print("Invalid option, please try again.")

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
                print(email, password)
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
           




