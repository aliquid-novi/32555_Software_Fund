import os
import json
import sys
# Direct path setting
sys.path.append(r'C:\Users\markp\OneDrive\Documents\GitHub\Uni Work\32555 - Fund._of_Software_Dev\32555_Software_Fund\GUI')
from Student_Course_System import SubjectClass as SC
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
        try:
            with open(self.filename, 'w') as fileHandler:
                json.dump(data, fileHandler, indent=2)
            print(f"Data written to {self.filename}")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    def read(self):
        try:
            with open(self.filename, 'r') as fileHandler:
                return json.load(fileHandler)
        except Exception as e:
            print(f"An error occurred reading the file: {e}")
            return {"students": {}, "used_ids": []}

    def list_students(self):
        data = self.dm.load_data() 
        student_list = []

        for student in data.get('students', {}).values():
            # Format each student's information
            student_info = f"{student['first_name']} {student['last_name']} :: {student['student_id']} ---> Email: {student['email']}"
            student_list.append(student_info)

        student_list.sort()

        return student_list
    
    def group_students_by_grade(self):
        data = self.dm.load_data() 
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

        if 'grade_groups' not in data:
            data['grade_groups'] = {}
        data['grade_groups'] = grade_groups
        self.dm.save_data(data)
    
        return grade_groups

    def get_pass_fail(self):
        data = self.dm.load_data()
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
        
        student_id = str(student_id)

        student_to_remove = None
        for student_email, details in stu_data.items():
            if details['student_id'] == student_id:
                student_to_remove = student_email
                break

        if student_to_remove:
            # Removes student from dictionary
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

class AdminSystem:
    def __init__(self, student_database):
        self.student_database = student_database
        self.db = DataBase()
        
    def partition_students(self):
        try:
            pass_fail = self.student_database.get_pass_fail()
            print("\033[93mPASS/FAIL Partition\033[0m")
            print(f"PASS -> {pass_fail['PASS']}")
            print(f"FAIL -> {pass_fail['FAIL']}")
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
        return True
        
    def clear_students(self):
        try:
            confirmation = input("\033[91mAre you sure you want to clear the database (Y)ES/(N)O: \033[0m").strip().upper()
            if confirmation == 'Y':
                self.student_database.clear_all_students()
                print("\033[93mStudents data cleared\033[0m")
            return True
        except Exception as e:
            print(f"\033[91mError clearing students: {e}\033[0m")
            return False


    def group_students(self):
        grades = self.student_database.group_students_by_grade()
        print("\033[93mGrade Grouping\033[0m")
        if grades:
            for grade, students in grades.items():
                print(f"Grade: {grade} -> {', '.join([str(student) for student in students])}")

    def remove_student(self):
        student_id = input("Remove by ID: ").strip()
        result = self.student_database.remove_student_by_id(student_id)
        
        if result:
            print(f"\033[93mRemoving Student {student_id} Account\033[0m")
        else:
            print(f"\033[91mStudent {student_id} does not exist\033[0m")

    def show_students(self):
        student_list = self.db.list_students()
        print("Student List")
        for student in student_list:
            print(student)

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


if __name__ == "__main__":
    db = DataBase()
    admin_system = AdminSystem(db)
    admin_system.admin_menu()