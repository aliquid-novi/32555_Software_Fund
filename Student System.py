from student_controller import StudentController
import re

def main():
    controller = StudentController()
    
    while True:
        command = input("Student System (l/r/x): ").strip().lower()

        # Exitl
        if command == 'x':
            print("\033[93mThank you!\033[0m")  # Yellow color for "Thank you!"
            break
        
        # Log in
        elif command == 'l':
            print("\033[92mStudent Sign In\033[0m")
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()

            if not re.match(r'^[A-Z][a-zA-Z]{5,}\d{3,}$', password) or not re.match(r'^([a-zA-Z]+)\.([a-zA-Z]+)@university\.com$', email):
                print("\033[91mIncorrect email or password format\033[0m")
            else:
                if controller.login_student(email, password):
                    print("\033[92mLogin successful!\033[0m")

                    student_course_menu()# Adding student_course_menu function HERE for logged in users
                    
                else:
                    print("\033[91mStudent does not exist\033[0m")

        # Register
        elif command == 'r':
            print("\033[92mStudent Sign Up\033[0m")
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()

            if not re.match(r'^[A-Z][a-zA-Z]{5,}\d{3,}$', password) or not re.match(r'^([a-zA-Z]+)\.([a-zA-Z]+)@university\.com$', email):
                print("\033[91mIncorrect email or password format\033[0m")
            else:
                try:
                    firstname, lastname = email.split('@')[0].split('.')
                    success, message = controller.register_student(firstname, lastname, email, password)
                    if success:
                        print("\033[93m{}".format(message), "\033[0m")
                    else:
                        print("\033[91m{}".format(message), "\033[0m")
                except ValueError:
                    print("\033[91mInvalid email format. Please use firstname.lastname@university.com\033[0m")
        else:
            print("\033[91mInvalid command. Please enter 'l' to login, 'r' to register, or 'x' to exit.\033[0m")

if __name__ == '__main__':
    main()