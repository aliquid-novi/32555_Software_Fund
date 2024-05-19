import json
import os

class DataManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filepath):
            print(f"{self.filepath} not found, creating new file.")
            self.save_data({'students': {}, 'used_ids': [], 'results': {'PASS': [], 'FAIL': []}})
            return {}
        with open(self.filepath, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Empty or corrupted file, creating a new one.")
                self.save_data({'students': {}, 'used_ids': [], 'results': {'PASS': [], 'FAIL': []}})
                return {}

    def save_data(self, data):
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=2)
            print("Data saved to file.")

    def get_student_data(self):
        return self.data.get('students', {})

    def update_student_data(self, student_data):
        self.data['students'] = student_data
        self.save_data(self.data)
        
    def update_results(self, pass_results, fail_results):
        # Ensure the 'results' key exists in the data dictionary
        if 'results' not in self.data:
            self.data['results'] = {'PASS': [], 'FAIL': []}  # Initialize both PASS and FAIL lists

        # Now safely assign the results
        self.data['results']['PASS'] = pass_results
        self.data['results']['FAIL'] = fail_results

        # Save the updated data back to the file
        self.save_data(self.data)
