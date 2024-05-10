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
    