# GUI model

import random as ran

class Student:
    def __init__(self,mark):
        self.IDF = ran.randint(100,1000)
        self.name = f'Student-{self.IDF:03}'
        self.mark = mark
        self.g = self.grade(mark)
    
    def grade(self,mark):
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
        return grade
    
    def match(self,id):
        return self.ID == id
    
    def __str__(self):
        return self.ID == id
    
    def __str__(self) -> str:
        return f'{self.name:12}: [{self.mark:4} --> {self.g:4}]'
    
class Database:

    def __init__(self):
        self.students = []
        for s in range (0,4):
            self.students.append(Student(ran.randint(0,100)))
    
    def getStudents():
        return self.students
    
    def student(self,id):
        for s in self.students:
            if s.match(id):
                return s
            return None
