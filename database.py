class DataBase():
    
    def write(self, txt):
        fileHandler = open("students.data.txt", "a")
        fileHandler.write(txt)
        fileHandler.write("\n")
        fileHandler.close()
        
    def read(self):
        fileHandler = open("students.data.txt", "r")
        content = fileHandler.read()
        print(content)
        content_list = fileHandler.readlines()
        print(content_list)
        fileHandler.close()

## Update Database class
class Updated_DataBase():
    def __init__(self):
        self.filename = "students.data.txt"

    def write(self, txt):
        with open(self.filename, "a") as fileHandler:
            fileHandler.write(txt + "\n")

    def read(self):
        with open(self.filename, "r") as fileHandler:
            content_list = fileHandler.readlines()
        return content_list
    