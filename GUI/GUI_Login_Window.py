# ### GUI application (AB)

# ## Login view

# # Importing libraries
# import tkinter as tk
# from tkinter import ttk

# # from student_controller import StudentController

# # Setting up size, title, background colour

# root = tk.Tk()
# root.geometry("500x500")
# root.title("University Application (GUI System)")
# root.configure(bg='#121212')  
# root.resizable(False, False)

# # controller = StudentController(root)
# # listVar = tk.Variable(value=StudentController.students())
# # studentList = tk.Listbox(root, listvariable == listVar)

# # studentList.pack(fill=tk.BOTH, expand=True, padx=20,pady=40)
# # Setting up button formatting 

# style = ttk.Style()
# style.theme_use('default')

# style.configure('TButton', bg='#3C4A82', fg='#FFFFFF', 
#                 font='Arial 12 bold', borderwidth=2, relief='solid')

# style.map('TButton',
#           bg=[('active', '#667292'), ('disabled', '#3C4A82')],
#           fg=[('active', '#FFFFFF'), ('disabled', '#D3D3D3')])

# selectButton = ttk.Button(root, text='Login', style='TButton') 
#                         #   command=lambda: controller.select_student(studentList))

# selectButton.pack(padx=8, pady=8, side='bottom')


# root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json

class GUIUniApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x400')
        self.root.title('University Application - Student Login')
        self.root.configure(bg='#252934')  # Dark gray background similar to the image
        
        # Load student data
        self.load_student_data()

        # Creating the login interface with adapted colors
        tk.Label(self.root, text='Please enter your credentials', font=('Arial', 14), bg='#252934', fg='#FFFFFF').pack(pady=20)
        
        tk.Label(self.root, text='Email:', bg='#252934', fg='#FFFFFF').pack()
        self.email_entry = tk.Entry(self.root, width=30, bg='#333B47', fg='#FFFFFF')
        self.email_entry.pack()
        
        tk.Label(self.root, text='Password:', bg='#252934', fg='#FFFFFF').pack()
        self.password_entry = tk.Entry(self.root, show='*', width=30, bg='#333B47', fg='#FFFFFF')
        self.password_entry.pack(pady=10)
        
        login_button = tk.Button(self.root, text='Login', command=self.login, bg='#4A5664', fg='#FFFFFF', relief='flat')
        login_button.pack(pady=20)

    def load_student_data(self):
        # Simulate loading data from a file (replace this with actual file reading)
        self.student_data = json.loads('{"students": {"jialing.huang@university.com": {"first_name": "jialing", "last_name": "huang", "email": "jialing.huang@university.com", "password": "Helloworld123", "student_id": "787244"}, "john.smith@university.com": {"first_name": "john", "last_name": "smith", "email": "john.smith@university.com", "password": "Helloworld123", "student_id": "227569"}, "alen.jones@university.com": {"first_name": "alen", "last_name": "jones", "email": "alen.jones@university.com", "password": "Helloworld123", "student_id": "713228"}}, "used_ids": [227569, 787244, 713228]}')

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if self.authenticate(email, password):
            self.open_enrollment_window()
        else:
            messagebox.showerror('Login failed', 'Invalid credentials', parent=self.root)

    def authenticate(self, email, password):
        # Check if the email exists in the student data and the password matches
        student_info = self.student_data.get('students', {}).get(email)
        if student_info and student_info['password'] == password:
            return True
        return False

    def open_enrollment_window(self):
        self.enrollment_window = tk.Toplevel(self.root)
        self.enrollment_window.title('Enrollment Window')
        self.enrollment_window.geometry('500x400')
        self.enrollment_window.configure(bg='#252934')
        
        tk.Label(self.enrollment_window, text='Select Subjects to Enroll', font=('Arial', 14), bg='#252934', fg='#FFFFFF').pack(pady=20)
        
        enroll_button = tk.Button(self.enrollment_window, text='Enroll in Subject', command=self.enroll_subject, bg='#4A5664', fg='#FFFFFF', relief='flat')
        enroll_button.pack(pady=20)
        
        self.root.withdraw()

    def enroll_subject(self):
        messagebox.showinfo('Enrollment', 'Subject has been added successfully!', parent=self.enrollment_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()

