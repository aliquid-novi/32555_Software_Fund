# The University System

class UniversitySystem:
    def __init__(self):
        self.running = True

    def main_menu(self):
        while self.running:
            print("\033[96mUniversity System: (A)dmin, (S)tudent, or (X) :\033[0m ", end="") #blue color
            choice = input().strip().upper()
            
            if choice == 'A':
                self.admin_menu()
            elif choice == 'S':
                self.student_menu()
            elif choice == 'X':
                self.running = False
                print("\033[93mThank You\033[0m") #yellow color
            else:
                print("Invalid choice, please try again.")

    def admin_menu(self):
        admin_running = True
        while admin_running:
            print("     \033[96mAdmin System (c/g/p/r/s/x):\033[0m ", end="") #blue color + indent
            choice = input().strip().lower()
            if choice == 'x':
                admin_running = False  
            #else:
            #    print("Function not implemented.")

    def student_menu(self):
        student_running = True
        while student_running:
            print("     \033[96mStudent System (l/r/x):\033[0m ", end="") #blue color + indent
            choice = input().strip().lower()
            if choice == 'x':
                student_running = False 
            #else:
            #    print("Function not implemented.")

if __name__ == "__main__":
    system = UniversitySystem()
    system.main_menu()
