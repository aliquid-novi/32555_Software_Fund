### GUI application (AB)

## Login view

# Importing libraries
import tkinter as tk
from tkinter import ttk

# from student_controller import StudentController

# Setting up size, title, background colour

root = tk.Tk()
root.geometry("500x500")
root.title("University Application (GUI System)")
root.configure(bg='#121212')  
root.resizable(False, False)

# controller = StudentController(root)
# listVar = tk.Variable(value=StudentController.students())
# studentList = tk.Listbox(root, listvariable == listVar)

# studentList.pack(fill=tk.BOTH, expand=True, padx=20,pady=40)
# Setting up button formatting 

style = ttk.Style()
style.theme_use('default')

style.configure('TButton', bg='#3C4A82', fg='#FFFFFF', 
                font='Arial 12 bold', borderwidth=2, relief='solid')

style.map('TButton',
          bg=[('active', '#667292'), ('disabled', '#3C4A82')],
          fg=[('active', '#FFFFFF'), ('disabled', '#D3D3D3')])

selectButton = ttk.Button(root, text='Login', style='TButton') 
                        #   command=lambda: controller.select_student(studentList))

selectButton.pack(padx=8, pady=8, side='bottom')


root.mainloop()




