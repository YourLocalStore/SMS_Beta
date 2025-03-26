import sqldb
import visuals.titlescreen as titlescreen
import time
import sys, os

import logininterfaces.interfacing as interfacing

from abc import ABC, abstractmethod
from threading import Thread

class LoginInterface():
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        self.__fname = fname
        self.__lname = lname

        self.__email = email
        self.username = username
        self.__password = password

        self.__teacher_id = teacher_id
        self.__administrator_id = administrator_id

    def selection(self):
        while True:
            try:
                print("\n ======== SMS General Login Menu ======== \n")
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
                            print("\n ======== SMS Staff Login Menu ======== \n")
                            for k,v in staff_choice.items():
                                print(f"\t{k}: {v}")

                            staff_selection = int(input("\nSelect an Option: "))

                            if staff_selection == 1:
                                teacher_login = TeacherLoginInterface(self.__fname, self.__lname, 
                                                                      self.username, self.__email,
                                                                      self.__password, self.__teacher_id, 
                                                                      self.__administrator_id)
                                teacher_login.login(username="", pwd="")

                            elif staff_selection == 2:
                                administrator_login = AdminLoginInterface(self.__fname, self.__lname, 
                                                                          self.username, self.__email,
                                                                          self.__password, self.__teacher_id,
                                                                          self.__administrator_id)
                                
                                administrator_login.login(username="", pwd="")

                            elif staff_selection == 3:
                                break

                        except ValueError as err:
                            print("Please select a valid option! \n")
                            continue

                elif user_selection == 2:
                    student_login = StudentLoginInterface(self.__fname, self.__lname, 
                                                          self.username, self.__email,
                                                          self.__password, self.__teacher_id,
                                                          self.__administrator_id)
                    student_login.login(username="", pwd="")

                elif user_selection == 3:
                    print("\n ======== SMS Register Menu ======== \n")
                    register_selection = input("Are you a Teacher (Y/N)? ")

                    if register_selection.lower() == "n":
                        student_register_obj = StudentRegisterInterface()
                        student_register_obj.user_register()

                    elif register_selection.lower() == "y":
                        teacher_register_obj = TeacherRegisterInterface()
                        teacher_register_obj.user_register()

                    else:
                        print("Select between Y or N!")
                        time.sleep(1)
                        break

                elif user_selection == 4:
                    break
            
            except ValueError as err:
                print("\n***************************************")
                print("An exception occurred! Have you tried entering the right values?")
                print(err)
                print("***************************************\n")
                continue

class AdminLoginInterface(LoginInterface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)
    
    def login(self, username, pwd):
        print("\n   < Go Back (Enter 0) \t\t || Administrator Login Page ||" + \
              "\n # ------------------------------------------------------------- # \n ")
        
        login_status = True
        admin_login_obj = sqldb.AdminLoginCheck()

        while login_status:
            try:
                username = input("Enter Your Username: ")
                if username == "0":
                    login_status = False
                    break

                self._LoginInterface__administrator_id = input("Enter your Administrator ID: ")
                if self._LoginInterface__administrator_id == "0":
                    login_status = False
                    break

                pwd = input("Enter Your Password: ")
                if pwd == "0":
                    login_status = False
                    break

                user_valid = admin_login_obj.login_user_exists(username, self._LoginInterface__administrator_id)
                pwd_valid = admin_login_obj.login_pwd_check(username, pwd)

                if (not user_valid) or (not pwd_valid) or (not self._LoginInterface__administrator_id):
                    print("\n=========== Incorrect User Information. ===========\n")
                    continue
                else:
                    print("Logging in...")
                    db_operation = sqldb.DBOperations()
                    tables = db_operation.get_table_names()
                    admin_info = db_operation.get_user_info(tables[0], username)
                    admin_user = interfacing.AdminInterface(
                        admin_info[1], admin_info[2],
                        admin_info[3], admin_info[4],
                        admin_info[5], self._LoginInterface__teacher_id,
                        self._LoginInterface__administrator_id
                    )
                    if type(admin_user) == None:
                        break
                break

            except Exception as err:
                print(err)
        return False

class TeacherLoginInterface(LoginInterface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)
    
    def login(self, username, pwd):
        print("\n   < Go Back (Enter 0) \t\t || Teacher Registration Page ||" + \
              "\n # ------------------------------------------------------------- # \n ")
        
        login_status = True
        teacher_login_obj = sqldb.TeacherLoginCheck()

        while login_status:
            try:
                username = input("Enter Your Username: ")
                if username == "0":
                    login_status = False
                    break

                self._LoginInterface__teacher_id = int(input("Enter your Employee ID: "))
                if self._LoginInterface__teacher_id == "0":
                    login_status = False
                    break

                pwd = input("Enter Your Password: ")
                if pwd == "0":
                    login_status = False
                    break

                user_valid = teacher_login_obj.login_user_exists(username, self._LoginInterface__teacher_id)
                pwd_valid = teacher_login_obj.login_pwd_check(username, pwd)

                if (not user_valid) or (not pwd_valid) or (not self._LoginInterface__teacher_id):
                    print("\n=========== Incorrect User Information. ===========\n")
                    continue
                else:
                    print("Logging in...")

                    db_operation = sqldb.DBOperations()
                    tables = db_operation.get_table_names()
                    teacher_info = db_operation.get_user_info(tables[5], username)
                    teacher_user = interfacing.TeacherInterface(
                        teacher_info[1], teacher_info[2],
                        teacher_info[3], teacher_info[4],
                        teacher_info[5], self._LoginInterface__teacher_id,
                        self._LoginInterface__administrator_id
                    )
                    if type(teacher_user) == None:
                        break
                break

            except Exception as err:
                print(err)
                
        return False

class StudentLoginInterface(LoginInterface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

    def login(self, username, pwd):
        print("\n   < Go Back (Enter 0) \t\t || Student Login Page ||" + \
              "\n # ------------------------------------------------------------- # \n ")
        
        login_status = True
        student_login_obj = sqldb.StudentLoginCheck()

        while login_status:
            try:
                username = input("\nEnter Your Username: ")
                if username == "0":
                    login_status = False
                    break

                pwd = input("Enter Your Password: ")
                if pwd == "0":
                    login_status = False
                    break

                user_valid = student_login_obj.login_user_exists(username)
                pwd_valid = student_login_obj.login_pwd_check(username, pwd)

                if (not user_valid) or (not pwd_valid):
                    print("\n=========== Incorrect User Information. ===========\n")
                    continue
                else:
                    print("Logging in...")

                    db_operation = sqldb.DBOperations()
                    tables = db_operation.get_table_names()
                    student_info = db_operation.get_user_info(tables[3], username)
                    student_user = interfacing.StudentInterface(
                        student_info[1], student_info[2],
                        student_info[3], student_info[4],
                        student_info[5], self._LoginInterface__teacher_id,
                        self._LoginInterface__administrator_id, student_info[0]
                    )
                    if type(student_user) == None:
                        break
                break
                    
            except Exception as err:
                print("\n-- Login Error")
                print(err)

        return False
    
class RegisterInterface(ABC):
    @abstractmethod
    def user_register(self):
        pass
    
class TeacherRegisterInterface(RegisterInterface, LoginInterface):
    def __init__(self, fname = "", lname = "", username = "", email = "", password = "", teacher_id = "", administrator_id = ""):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

    def user_register(self):
        print("\n   < Go Back (Enter 0) \t\t || Teacher Registration Page ||" + \
              "\n # ------------------------------------------------------------- # \n ")
        
        register_condition = True

        while register_condition:
            try:
                self.__fname = input("Enter Your First Name: ")
                if self.__fname == "0":
                    register_condition == False
                    break

                self.__lname = input("Enter Your Last Name: ")
                if self.__lname == "0":
                    register_condition == False
                    break

                self.username = input("Enter Your Username: ")
                if self.username == "0":
                    register_condition == False
                    break

                self.__email = input("Enter Your Email Address: ")
                if self.__email == "0":
                    register_condition == False
                    break

                self.__password = input("Enter your Password: ")
                if self.__password == "0":
                    register_condition == False
                    break
                
                user_registering = sqldb.RegisterPerson(
                    self.__fname, self.__lname, 
                    self.username, self.__email, 
                    self.__password
                )
                check_user = user_registering.register_teacher(
                    self.__fname, self.__lname, 
                    self.username, self.__email, 
                    self.__password
                )
                # If the user is registered
                if check_user:
                    print("Unfortunately, the user already exists. Please try again! \n")
                    continue
                    
                # If the user had not been registered
                elif not check_user:
                    print(f"{self.username} has been successfully registered. \n")
                    register_condition = False
                    break

            except Exception as err:
                print("Something went wrong!")
                print(err)
                return False

            self.selection()
        return False

class StudentRegisterInterface(RegisterInterface, LoginInterface):
    def __init__(self, fname = "", lname = "", username = "", email = "", password = "", teacher_id = "", administrator_id = ""):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

    def user_register(self):
        print("\n   < Go Back (Enter 0) \t\t || Student Registration Page ||" + \
              "\n # ------------------------------------------------------------- # \n ")
        
        register_condition = True

        while register_condition:
            try:
                self.__fname = input("Enter Your First Name: ")
                if self.__fname == "0":
                    register_condition == False
                    break

                self.__lname = input("Enter Your Last Name: ")
                if self.__lname == "0":
                    register_condition == False
                    break

                self.username = input("Enter Your Username (20 Char. Max): ")
                if self.username == "0":
                    register_condition == False
                    break

                self.__email = input("Enter Your Email Address: ")
                if self.__email == "0":
                    register_condition == False
                    break

                self.__password = input("Enter your Password: ")
                if self.__password == "0":
                    register_condition == False
                    break

                user_registering = sqldb.RegisterPerson(
                    self.__fname, self.__lname, 
                    self.username, self.__email, 
                    self.__password
                )
                check_user = user_registering.register_student(
                    self.__fname, self.__lname, 
                    self.username, self.__email, 
                    self.__password
                )

                # If the user is registered
                if check_user:
                    print("Unfortunately, the user already exists. Please try again! \n")
                    continue
                    
                # If the user had not been registered
                elif not check_user:
                    print(f"{self.username} has been successfully registered. \n")
                    register_condition = False
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
            msg = "Connecting to Database"

            self.connection_thread = Thread(target=sqldb.CheckDBState.try_connection)
            self.message_thread = Thread(
                target=Utilities.load_connect_msg, 
                args=(self, msg, self.connection_thread,)
            )

            self.connection_thread.start()
            self.message_thread.start()

            self.connection_thread.join()
            self.message_thread.join()
            return True

        except Exception as err:
            print("Please try again, or contact the developer immediately. \n")
            print(f"Error: {err}")

    def load_connect_msg(self, msg, thread):
        loading = True

        while loading:
            for j in range(4):
                dot_amount = "." * j
                print(f"{msg}{dot_amount}", end='\r', flush=True)
                time.sleep(0.25)

            print(f"{msg}     ", end='\r', flush=True)

            if (not thread.is_alive()):
                print("Connection Successful! \n")
                loading = False
                break

            else:
                print("Something went wrong! ")
                break
    
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
                user_login = LoginInterface(
                    fname="", lname="", 
                    username="", email="", 
                    password="", teacher_id="",
                    administrator_id=""
                )
                user_login.selection()
            elif user_selection == 2:
                raise SystemExit
            
        except ValueError as err:
            print("\n***************************************")
            print("An exception occurred! Have you tried entering the right values?")
            print(err)
            print("***************************************\n")
            continue

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("\nWelcome to the Student Management System (SMS)!")
    time.sleep(1.5)

    print("Please wait while we load the database! \n")
    time.sleep(1.5)

    try:
        util = Utilities()
        connection_attempt = util.connect_to_db()

        if connection_attempt:
            create_tables = sqldb.CreateRegisterTables()
            create_tables.student_register_table()
            create_tables.teacher_register_table()
            create_tables.administrator_register_table()
            create_tables.classroom_table()
            create_tables.student_classroom_tables()
            create_tables.teacher_classroom_tables()

            main()
    
    except Exception as err:
        print("-- Something went wrong! The error is shown below:")
        print(f"{err}\n")
        raise SystemExit



