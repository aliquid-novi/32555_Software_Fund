# Student Course System Criteria # 

# Tracking Subject enrolment is tracked - DOUBLE CHECK THIS
# Error Handling Exceptions, errors, logical scenarios are handled - DOUBLE CHECK THIS 
import random

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

class DataBase(): 
    def __init__(self):
        self.filename = "students.data.txt"

    def write(self, txt):
        with open(self.filename, "a") as fileHandler:
            fileHandler.write(txt + "\n")

    def read(self):
        with open(self.filename, "r") as fileHandler:
            content_list = fileHandler.readlines()
        return content_list

class Backend():
    "Needs 'db' DataBase object to perform get_count function"

    def __init__(self, database):
        self.filename = 'students.data.txt'
        self.db = database

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
    
    def get_count(self):
        contents = self.db.read()
        return len(contents)  
    
    @staticmethod
    def update_password():
        new_password = input("New Password:")
        confirm_password = input("Confirm Password:")
        
        while confirm_password != new_password:
            Backend.print_col("Password does not match - try again", "red")   
            confirm_password = input("Confirm Password:")
    
    def show(self):
        subject_count = Backend.get_count(self)
        contents = self.db.read()
        if subject_count > 0:
            Backend.print_col(f"Showing {subject_count} subjects", "yellow")

            for line in contents:
                subject_id, mark, grade = line.strip().split(',')
                print(f"Subject::{subject_id} -- mark = {mark} -- grade = {grade}")
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

            contents = self.db.read()
            # Check if the subject is listed
            if any(line.startswith(subject + ",") for line in contents):
                Backend.print_col(f"Dropping Subject-{subject}", "yellow")
                # Remove subject line from file
                new_contents = [line for line in contents if not line.strip().startswith(subject + ",")]
            
                with open(self.db.filename, 'w') as file:
                    for line in new_contents:
                        file.writelines(line)
                Backend.print_col(f"You are now enrolled in {len(new_contents)} out of 4 subjects", "yellow")
                return
            else:
                Backend.print_col(f"Error: Subject-{subject} is not in subject list. Available subjects are:", "red")
                for line in contents:
                    subject_id = line.split(',')[0]
                    print(f" - Subject: {subject_id}")
                Backend.print_col(f"Or press 'b' to go back to menu", "red")
    
    def enrollment(self):
        subject_count = Backend.get_count(self)
        if subject_count >= 4: # Error Handling
            Backend.print_col("Students are allowed to enrol in 4 subjects only", "red")
            user_input = Backend.standard_user_input()
        else:
            subject_id = SubjectClass.Gen_SubjectID(self)
            mark, grade = SubjectClass.Gen_Results(self)
            Backend.print_col(f"Enrolling in Subject-{subject_id}", "yellow")

            self.db.write(f"{subject_id},{mark},{grade}")

            subject_count = Backend.get_count(self)
            Backend.print_col(f"You are now enrolled in {subject_count} out of 4 subjects", "yellow")
            user_input = Backend.standard_user_input()

        return user_input

class StuCourseSys():

    def __init__(self):
        self.db = DataBase()
        self.be = Backend(self.db)
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
    system = StuCourseSys()
    system.main()