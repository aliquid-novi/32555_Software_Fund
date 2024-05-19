import os
import json

class DataBase:
    def __init__(self, filename="student.data"):
        self.filename = filename
        self.check_and_create_file()

    def check_and_create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write(json.dumps({"students": {}, "used_ids": []}))
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
            print("Error: JSON file contains invalid JSON.")
            return {"students": {}, "used_ids": []}
        except FileNotFoundError:
            print(f"File '{self.filename}' does not exist.")
            return {"students": {}, "used_ids": []}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"students": {}, "used_ids": []}

    def list_students(self):
        data = self.read()
        return data['students'].values()

    def get_students_by_grade(self):
        data = self.read()
        grades = {}
        for student in data['students'].values():
            grade = student.get('grade')
            if grade in grades:
                grades[grade].append(student)
            else:
                grades[grade] = [student]
        return grades

    def get_pass_fail(self):
        data = self.read()
        results = {'pass': [], 'fail': []}
        for student in data['students'].values():
            if student.get('mark') >= 60:
                results['pass'].append(student)
            else:
                results['fail'].append(student)
        return results

    def remove_student_by_id(self, student_id):
        data = self.read()
        if student_id in data['students']:
            del data['students'][student_id]
            data['used_ids'].remove(student_id)
            self.write(data)
            return True
        return False

    def clear_all_students(self):
        self.write({"students": {}, "used_ids": []})

class AdminSystem:
    def __init__(self, student_database):
        self.student_database = student_database

    def admin_menu(self):
        admin_running = True
        while admin_running:
            print("\033[96mAdmin System (c/g/p/r/s/x):\033[0m ", end="")
            choice = input().strip().lower()
            if choice == 'c':
                self.clear_students()
            elif choice == 'g':
                self.group_students()
            elif choice == 'p':
                self.partition_students()
            elif choice == 'r':
                self.remove_student()
            elif choice == 's':
                self.show_students()
            elif choice == 'x':
                print("Exiting admin system.")
                admin_running = False
            else:
                print("Invalid option, please try again.")

    def clear_students(self):
        confirmation = input("\033[91mAre you sure you want to clear the database (Y/ES/(N)O): \033[0m").strip().upper()
        print("\033[93mClearing students database\033[0")
        if confirmation == 'Y':
            self.student_database.clear_all_students()
            print("\033[93mStudents data cleared\033[0m")

    def group_students(self):
        grades = self.student_database.get_students_by_grade()
        print("\033[93mGrade Grouping\033[0m")
        if grades:
            for grade, students in grades.items():
                print(f"Grade: {grade} -> {', '.join([str(student) for student in students])}")

    def partition_students(self):
        pass_fail = self.student_database.get_pass_fail()
        print("\033[93mPASS/FAIL Partition\033[0m")
        print(f"PASS -> {pass_fail['pass']}")
        print(f"FAIL -> {pass_fail['fail']}")

    def remove_student(self):
        student_id = input("Remove by ID: ").strip()
        result = self.student_database.remove_student_by_id(student_id)
        if result:
            print(f"\033[93mRemoving Student {student_id} Account\033[0m")
        else:
            print("\033[91mStudent {student_id} does not exist\033[0m")

    def show_students(self):
        students = self.student_database.list_students()
        if students:
            for student in students:
                print("\033[93mStudent List\033[0m")
                print(f"{student['name']} :: {student['id']} --> Email: {student['email']}")
        else:
            print("< Nothing to Display >")

# db = DataBase()
# admin_system = AdminSystem(db)
# admin_system.admin_menu()
