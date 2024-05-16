## Update Database class
class DataBase():
    def __init__(self):
        self.filename = "students.data"

    def check_file(self): # Check if file exists, if not, creates it
        pass 
    def write(self, txt): # Write objetcs to the file "students.data"
        with open(self.filename, "a") as fileHandler:
            fileHandler.write(txt + "\n")

    def read(self): # Read objects from the file "students.data"
        with open(self.filename, "r") as fileHandler:
            content_list = fileHandler.readlines()
        return content_list
    
    def clear_file(self): # Clear the objects from the file "students.data"
        pass
    