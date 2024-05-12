# The University System

class UniversitySystem:
    def __init__(self):
        self.running = True

    def main_menu(self):
        while self.running:
            print("\nUniversity System: (A)dmin, (S)tudent, or (X): ", end="")
            choice = input().strip().upper()
            
            if choice == 'A':
                self.admin_menu()
            elif choice == 'S':
                self.student_menu()
            elif choice == 'X':
                self.running = False
                print("Thank You")
            else:
                print("Invalid choice, please try again.")

    def admin_menu(self):
        print("Admin System")

    def student_menu(self):
        print("Student System")

if __name__ == "__main__":
    system = UniversitySystem()
    system.main_menu()
