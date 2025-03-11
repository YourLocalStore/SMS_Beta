import sqldb
import visuals.titlescreen as titlescreen
import time
import threading

from abc import ABC, abstractmethod
from threading import Thread

class StaffInterface(ABC):
    @abstractmethod
    def class_details(self):
        pass

    @abstractmethod
    def student_details(self):
        pass

class TeacherInterface(StaffInterface):
    def account_information(self):
        pass
    def class_details(self):
        pass

class AdminInterface(StaffInterface):
    def student_details(self):
        pass
    def class_details(self):
        pass

class StudentInterface:
    def account_information(self):
        pass

class LoginInterface:
    def __init__(self, fname, lname, username, email, password):
        self.__fname = fname
        self.__lname = lname
        self.__email = email
        self.username = username
        self.__password = password

    def get_username(self):
        return self.username
    
    def get_fname(self):
        return self.__fname
    
    def get_lname(self):
        return self.__lname
    
    def selection(self):
        while True:
            try:
                print("\n -------- SMS Login Menu -------- \n")
                selection = {
                        1: "Staff Log-in",
                        2: "Student Log-in",
                        3: "Register",
                        4: "Exit"
                    }

                for k,v in selection.items():
                    print(f"\t{k}: {v}")

                user_selection = int(input("\nEnter a selection: "))

                if user_selection == 1:
                    while True:
                        try:
                            staff_choice = {
                                1: "Teacher",
                                2: "Administrator",
                                3: "Go Back"
                            }
                            for k,v in staff_choice.items():
                                print(f"\t{k}: {v}")

                            staff_selection = int(input("\nSelect an Option: "))

                            if staff_selection == 1:
                                pass
                            elif staff_selection == 2:
                                pass
                            elif staff_selection == 3:
                                break

                        except ValueError as err:
                            print("Please select a valid option! \n")
                            continue

                elif user_selection == 2:
                    self.student_login(username="", pwd="")

                elif user_selection == 3:
                    self.user_register()
                elif user_selection == 4:
                    break
            
            except ValueError as err:
                print("\n***************************************")
                print("An exception occurred! Have you tried entering the right values?")
                print(err)
                print("***************************************\n")
                continue

    def teacher_login(self, username, pwd, employee_id):
        login = True
        teacher_login_obj = sqldb.TeacherLoginCheck()

    def student_login(self, username, pwd):
        login = True
        login_obj = sqldb.StudentLoginCheck()

        while login:
            try:
                username = input("Enter Your Username: ")
                if username == "0":
                    login = False
                    break

                pwd = input("Enter Your Password: ")
                if pwd == "0":
                    login = False
                    break

                user_valid = login_obj.login_user_exists(username)
                pwd_valid = login_obj.login_pwd_check(username, pwd)

                if (not user_valid) or (not pwd_valid):
                    print("Username or Password is Incorrect.")
                    continue

                else:
                    print("Logging in...")

                    """

                    here, we must get the role of the person logging in
                    check it and go into the correct interface

                    """

                    break
                    
            except Exception as err:
                print(err)

        return False

    def user_register(self):
        print("""
                 < Go Back (Enter 0)
                # ----------------------------------------------------- # \n """)
        
        register_condition = True

        while register_condition:
            try:
                self.__fname = input("Enter Your First Name: ")
                if self.__fname == "0":
                    register == False
                    break

                self.__lname = input("Enter Your Last Name: ")
                if self.__lname == "0":
                    register == False
                    break

                self.username = input("Enter Your Username: ")
                if self.username == "0":
                    register == False
                    break

                self.__email = input("Enter Your Email Address: ")
                if self.__email == "0":
                    register == False
                    break

                self.__password = input("Enter your Password: ")
                if self.__password == "0":
                    register == False
                    break
                
                user_registering = sqldb.RegisterPerson(self.__fname, self.__lname, 
                                                        self.username, self.__email, 
                                                        self.__password)
                user_registering.register_table() # Check if the table exists
                check_user = user_registering.register_user(self.__fname, self.__lname, 
                                                            self.username, self.__email, 
                                                            self.__password)
                # If the user is registered
                if check_user:
                    print("Unfortunately, the user already exists. Please try again! \n")
                    continue
                    
                # If the user had not been registered
                elif not check_user:
                    print("User has Successfully Registered. \n")
                    register = False
                    break

            except Exception as err:
                print("Something went wrong!")
                print(err)
                return False

            self.selection()
        return False

class Utilities:
    def connect_to_db(self):
        try:
            self.connection_thread = Thread(target=sqldb.CheckDBState.try_connection)
            self.message_thread = Thread(target=Utilities.load_msg, 
                                         args=(self, self.connection_thread,))

            self.connection_thread.start()
            self.message_thread.start()

            self.connection_thread.join()
            self.message_thread.join()

        except Exception as err:
            print("Please try again, or contact the developer immediately. \n")
            print(f"Error: {err}")

    def load_msg(self, connection_thread):
        loading = True
        msg = "Connecting to Database"

        while loading:
            for j in range(4):
                dot_amount = "." * j
                print(f"{msg}{dot_amount}", end='\r', flush=True)
                time.sleep(0.25)

            print(f"{msg}     ", end='\r', flush=True)

            if (not connection_thread.is_alive()):
                print("Connection Successful!")
                loading = False
                main()

            else:
                print("Something went wrong! ")
                break

        return False
    
def main():
    while True:
        try:
            print(titlescreen.title)
            selection = {
                1: "Enter",
                2: "Exit"
            }

            for k,v in selection.items():
                print(f"{k}: {v}")

            user_selection = int(input("\nEnter a selection: "))

            if user_selection == 1:
                login = LoginInterface(fname="", lname="", username="", email="", password="")
                login.selection()
            elif user_selection == 2:
                break
            
        except ValueError as err:
            print("\n***************************************")
            print("An exception occurred! Have you tried entering the right values?")
            print(err)
            print("***************************************\n")
            continue

    return False

if __name__ == "__main__":
    print("\nWelcome to the Student Management System (SMS)!")
    time.sleep(1.5)

    print("Please wait while we load the database... \n")
    time.sleep(1.5)

    try:
        util = Utilities()
        connection_attempt = util.connect_to_db()

        if connection_attempt:
            main()

    except Exception as err:
        print(err)
        
