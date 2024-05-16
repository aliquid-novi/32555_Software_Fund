# GUI controller

from GUI_Student_Window import StudentView
from GUI_model import Database

class StudentController:
    def __init__(self, master):
        self.master = master
        self.model = Database
    
    def select_student_(self, studentList):
        selections = studentList.curselection()
        print('Student: ',studentList)
        index = selections[0]
        info = studentList.get(index)
        StudentView(self.master,info)

def students(self):
    return self.model.getStudents()



