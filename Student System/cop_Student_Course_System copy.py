# Libraries
import random
import os
import json

class SubjectClass():

    def Gen_SubjectID(self):
        
        number = random.randint(1,999)
        formatted_id = f"{number:03d}"
        return(formatted_id)
    
    def Gen_Results(self):
        # Generate Marks + Grade in same function
        mark = random.randint(25,100)
        if mark <= 49:
            grade = 'F'
        elif mark >= 50 and mark <= 64:
            grade = 'P'
        elif mark >= 65 and mark <= 74:
            grade = 'C'
        elif mark >= 75 and mark <= 84:
            grade = 'D'
        elif mark > 85:
            grade = 'HD'
        
        return mark, grade
    
class DataBase:
    def __init__(self, filename="student.data"):
        self.filename = filename
        self.check_and_create_file()

    def check_and_create_file(self):
        print("Checking if 'students.data' exists...")
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write("")  # Create an empty file
            print(f"File '{self.filename}' created.")
        else:
            print(f"File '{self.filename}'exists.")

    def write(self, txt):
        with open(self.filename, 'w') as fileHandler:
            json.dump(txt, fileHandler, indent=2)
        # print(f"Data written to {self.filename}")

    def read(self):
        try:
            with open(self.filename, 'r') as fileHandler:
                if os.stat(self.filename).st_size == 0:  # Check if the file is empty
                    print("File is empty.")
                    return None
                json_obj = json.load(fileHandler)
                # print(json.dumps(json_obj, indent=4))
                return json_obj
        except json.JSONDecodeError:
            print("Error: File contains invalid JSON.")
        except FileNotFoundError:
            print(f"File '{self.filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

class Backend():
    "Needs 'db' DataBase object to perform get_count function"

    def __init__(self, email):
        self.filename = 'students.data'
        self.db = DataBase()
        self.students = self.db.read()
        self.student = email

    @staticmethod
    def print_col(text, colour):
        colours = {
            'blue': '\033[96m',   # Blue
            'yellow': '\033[93m', # Yellow
            'red': '\033[91m',    # Red
            'end': '\033[0m',
        }
        
        colour_code = colours.get(colour, colours['end'])
        print(f"{colour_code}{text}{colours['end']}")

    @staticmethod
    def standard_user_input():
        Backend.print_col("Student Course Menu (c/e/r/s/x):", 'blue') 
        user_input = input()
        return user_input
    
    def check_sub(self):
        data = self.students
        if 'subjects' not in data['students'][self.student]:
            return False

    def get_count(self):
        if self.check_sub() == True:
            return len(self.students['students'][self.student]['subject'])
        else:
            return 0
    
    @staticmethod
    def update_password():
        new_password = input("New Password:")
        confirm_password = input("Confirm Password:")
        
        while confirm_password != new_password:
            Backend.print_col("Password does not match - try again", "red")   
            confirm_password = input("Confirm Password:")
    
    def show(self):
        data = self.students
        subject_count = Backend.get_count(self)
        contents = self.db.read()
        if subject_count > 0:
            Backend.print_col(f"Showing {subject_count} subjects", "yellow")
            subjects = data['students'][self.student]['subjects']  
            for i in range(len(subjects)):
                print(f"  Subject::{subjects[i]['subject']} -- mark = {subjects[i]['mark']} -- grade == {subjects[i]['grade']}")
                
            user_input = Backend.standard_user_input()
            return user_input
        else:
            Backend.print_col("No subjects currently enrolled.", "red") # Error Handling
            user_input = Backend.standard_user_input()
            return user_input
    
    def removal(self):
        while True:
            subject = str(input("Remove Subject by ID: "))
            if subject.lower() == 'b':
                return  # Exit the function and return to the main menu immediately

            data = self.students
            
            # Check if the student exists
            if 'students' in data and self.student in data['students']:
                student_data = data['students'][self.student]

                # Check if the subject is listed
                subjects = student_data.get('subjects', [])
                subject_to_remove = next((s for s in subjects if s['subject'] == subject), None)

                if subject_to_remove:
                    Backend.print_col(f"Dropping Subject-{subject}", "yellow")
                    # Remove the subject
                    subjects.remove(subject_to_remove)

                    # Write updated data back to the file
                    self.db.write(data)
                    Backend.print_col(f"You are now enrolled in {len(subjects)} out of 4 subjects", "yellow")
                    return
                else:
                    Backend.print_col(f"Error: Subject-{subject} is not in subject list. Available subjects are:", "red")
                    for s in subjects:
                        print(f" - Subject: {s['subject']}")
                    Backend.print_col(f"Or press 'b' to go back to menu", "red")
            else:
                Backend.print_col("Error: Student data not found.", "red")
                return

    def enrollment(self):
        subject_count = Backend.get_count(self)
        if subject_count >= 4: # Error Handling
            Backend.print_col("Students are allowed to enrol in 4 subjects only", "red")
            user_input = Backend.standard_user_input()
        else:
            subject_id = SubjectClass.Gen_SubjectID(self)
            mark, grade = SubjectClass.Gen_Results(self)
            Backend.print_col(f"Enrolling in Subject-{subject_id}", "yellow")
            
            # Load student data
            data = self.students

            if 'subjects' not in data['students'][self.student]:
                data['students'][self.student]['subjects'] = []

            subjects = {'subject': subject_id, 'mark': mark, 'grade': grade}
            data['students'][self.student]['subjects'].append(subjects)

            # Write updated data
            self.db.write(data)

            subject_count = Backend.get_count(self)
            Backend.print_col(f"You are now enrolled in {subject_count} out of 4 subjects", "yellow")
            user_input = Backend.standard_user_input()

        return user_input

class StuCourseSys():

    def __init__(self, email):

        self.db = DataBase()
        self.be = Backend(email)
        self.contents = self.db.read()
        self.user_input = self.be.standard_user_input()
        self.correct_inputs = ['x', 'c', 'e', 'r', 's']

    def main(self):

        while self.user_input != 'x':
            
            if self.user_input == 'c': # Changing Subject
                self.be.print_col("Updating Password", "yellow")
                self.be.update_password()
                self.user_input = self.be.standard_user_input()
                
            elif self.user_input == 'e': # Enrollment 
                self.user_input = self.be.enrollment()
                    
            elif self.user_input == 'r':  # Removing Subject
                self.be.removal()
                self.user_input = self.be.standard_user_input()
                    
            elif self.user_input == 's': # Showing subjects
                self.user_input = self.be.show()

            elif self.user_input not in self.correct_inputs: # Error Handling
                be.print_col(f"Input {self.user_input} not a valid input. Try again...", "red") 
                self.user_input = self.be.standard_user_input()

if __name__ == "__main__":
    system = StuCourseSys('mark.paje@university.com')
    system.main()
