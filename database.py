import os
import json

class DataBase:
    def __init__(self, filename="student.data"):
        self.filename = filename
        self.check_and_create_file()

    def check_and_create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write("")  # Create an empty file
            print(f"File '{self.filename}' created.")
        else:
            print(f"File '{self.filename}' already exists.")

    def write(self, txt):
        with open(self.filename, 'w') as fileHandler:
            json.dump(txt, fileHandler, indent=2)
        print(f"Data written to {self.filename}")

    def read(self):
        try:
            with open(self.filename, 'r') as fileHandler:
                if os.stat(self.filename).st_size == 0:  # Check if the file is empty
                    print("File is empty.")
                    return None
                json_obj = json.load(fileHandler)
                print(json.dumps(json_obj, indent=4))
                return json_obj
        except json.JSONDecodeError:
            print("Error: File contains invalid JSON.")
        except FileNotFoundError:
            print(f"File '{self.filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")