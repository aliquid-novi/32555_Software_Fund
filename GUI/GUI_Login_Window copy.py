import tkinter as tk
from tkinter import messagebox
import json
import re
import sys
from data_manager import DataManager

# # module_dir = r'C:/Users/danie/32555_Software_Fund-1/Student System/Student_Course_System_copy.py' # Anna's relative path?

import sys
import os

# Navigate up one directory from the current file's directory to access the 32555_Software_Fund folder
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
sys.path.append(module_dir)

import Student_Course_System as controller

class GUIUniApp:

    def __init__(self, root):
        self.root = root
        self.root.geometry('600x600')
        self.root.title('University Application - Student Login')
        self.root.configure(bg='#252934')  # Dark theme
        # abs file path. maybe change to a common one later?
        self.filepath = r'C:\Users\markp\OneDrive\Documents\GitHub\Uni Work\32555 - Fund._of_Software_Dev\32555_Software_Fund\student.data'
        self.data_controller = DataManager(self.filepath)
        # Load student data
        self.student_data = self.data_controller.get_student_data()
        self.logged_in_student = None
        self.subjects = controller.SubjectClass()
        self.db = controller.DataBase(self.filepath)

        # GUI Login window
        tk.Label(self.root, text='Enter your login details', font=('Arial', 14), bg='#252934', fg='#FFFFFF').pack(pady=20)
        
        tk.Label(self.root, text='Email:', bg='#252934', fg='#FFFFFF').pack()
        self.email_entry = tk.Entry(self.root, width=30, bg='#333B47', fg='#FFFFFF')
        self.email_entry.pack()
        
        tk.Label(self.root, text='Password:', bg='#252934', fg='#FFFFFF').pack()
        self.password_entry = tk.Entry(self.root, show='*', width=30, bg='#333B47', fg='#FFFFFF')
        self.password_entry.pack(pady=10)
        
        login_button = tk.Button(self.root, text='Login', command=self.login, bg='#4A5664', fg='#FFFFFF', relief='flat')
        login_button.pack(pady=20)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        self.backend = controller.Backend(email, self.filepath)
        self.email = email
        # Email not entered / password not entered
        if not email or not password:
            messagebox.showerror('Login Error', 'Email and password cannot be empty')
            return
        
        # Check email format
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            messagebox.showerror('Login Error', 'Invalid email format')
            return
        
        if self.authenticate(email, password):
            self.logged_in_student = email
            self.open_enrollment_window()
        else:
            messagebox.showerror('Login Error', 'Invalid credentials')

    def authenticate(self, email, password):
        student = self.student_data.get(email) 
        return student and student['password'] == password

    def open_enrollment_window(self):
        self.enrollment_window = tk.Toplevel(self.root)
        self.enrollment_window.title('Courses enrolled')
        self.enrollment_window.geometry('600x600')
        self.enrollment_window.configure(bg='#252934')
        
        tk.Label(self.enrollment_window, text='Select Subject to Enroll:', font=('Arial', 14), bg='#252934', fg='#FFFFFF').pack(pady=20)
        
        # Subjects list
        self.subjects_list = [] # init list
        for i in range(10):
            self.subjects_list.append(self.subjects.Gen_SubjectID())
        
        self.enrolled_subjects = [] # change to current subjects already
        students = self.data_controller.get_student_data()

        if 'subjects' not in students[self.email]:
            students[self.email]['subjects'] = []
        
        for i in range(len(students[self.email]['subjects'])):
            self.enrolled_subjects.append(students[self.email]['subjects'][i]['subject'])

        for subject in self.subjects_list:
            button = tk.Button(self.enrollment_window, text=f'Enroll in {subject}', command=lambda subj=subject: self.enroll_subject(subj), bg='#4A5664', fg='#FFFFFF', relief='flat')
            button.pack(pady=5)
        
        # Button to manage enrolled subjects
        tk.Button(self.enrollment_window, text='Manage Enrolled Subjects', command=self.manage_enrollment, bg='#6272A4', fg='#FFFFFF', relief='flat').pack(pady=20)

        self.root.withdraw()

    def save_data(self, data=None):
        if data is not None:
            self.data = data
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=2)
            print("Data saved to file.")
    
    def update_student_data(self, student_data):
        self.data['students'] = student_data
        self.save_data()

    def enroll_subject(self, subject):

        students = self.db.read()
        # Retrieve the entire student data
        all_students_data = self.db.read()
        # gets specific student
        student_data = all_students_data['students'][self.email]

    
        if 'subjects' not in student_data:
            student_data['subjects'] = []

        # Read current amount of subjects already enrolled
        if len(self.enrolled_subjects) >= 4:
            messagebox.showerror('Enrollment Error', 'Cannot enroll in more than 4 subjects')
            return
        if subject in self.enrolled_subjects:
            messagebox.showinfo('Enrollment Info', 'Already enrolled in this subject')
            return

        self.enrolled_subjects.append(subject)
        student_data['subjects'].append(subject)
        all_students_data[self.email] = student_data
        mark, grade = self.subjects.Gen_Results()
        
        # issue with subjects not being a key, don't tihnk the if 'subjects' loop above is working as intended
        students['students'][self.email]['subjects'].append({'subject': subject, 'mark': mark, 'grade': grade})

        self.db.write(students)
        # main issue was that after writing into the file, it would modify the entire file 
        # structure and remove 'students' key which other functions depend on.
        
        messagebox.showinfo('Enrollment Success', f'Successfully enrolled in {subject}')

    def manage_enrollment(self):
        # Window to manage enrolled subjects
        self.manage_window = tk.Toplevel(self.enrollment_window)
        self.manage_window.title('Manage Enrolled Subjects')
        self.manage_window.geometry('600x600')
        self.manage_window.configure(bg='#252934')
        
        tk.Label(self.manage_window, text='Your Enrolled Subjects:', font=('Arial', 14), bg='#252934', fg='#FFFFFF').pack(pady=20)
        
        for subject in self.enrolled_subjects:
            frame = tk.Frame(self.manage_window, bg='#333B47')
            frame.pack(pady=5, fill='x', padx=50)
            tk.Label(frame, text=subject, bg='#333B47', fg='#FFFFFF').pack(side='left')
            remove_button = tk.Button(frame, text='Remove', command=lambda subj=subject: self.remove_subject(subj), bg='#FF5555', fg='#FFFFFF', relief='flat')
            remove_button.pack(side='right')

    def remove_subject(self, subject):
        if subject in self.enrolled_subjects:
            self.enrolled_subjects.remove(subject)
            messagebox.showinfo('Update', f'{subject} has been removed from your enrollment list')
            self.manage_window.destroy()  # Refresh the manage enrollment window
            self.manage_enrollment()  # Reopen to update the list

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()
