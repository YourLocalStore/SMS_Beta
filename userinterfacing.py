import main
import sqldb
import datetime
import help_module
import time
import pathlib

from prettytable import PrettyTable
from abc import ABC, abstractmethod

class Interface(ABC, main.LoginInterface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)
        self.date_today = datetime.datetime.now()

    def get_fname(self):
        return self._LoginInterface__fname
    
    def set_fname(self, new_fname):
        self._LoginInterface__fname = new_fname
        return self._LoginInterface__fname

    def get_lname(self):
        return self._LoginInterface__lname
    
    def set_fname(self, new_lname):
        self._LoginInterface__fname = new_lname
        return self._LoginInterface__fname
    
    def get_username(self):
        return self.username
    
    def set_username(self, new_username):
        self._LoginInterface__fname = new_username
        return self._LoginInterface__fname
    
    def get_email(self):
        return self._LoginInterface__email
    
    def set_email(self, new_email):
        self._LoginInterface__fname = new_email
        return self._LoginInterface__fname
    
    def get_password(self):
        return self._LoginInterface__password
    
    def set_password(self, new_password):
        self._LoginInterface__fname = new_password
        return self._LoginInterface__fname
    
    def get_teacher_id(self):
        return self._LoginInterface__teacher_id
    
    def get_admin_id(self):
        return self._LoginInterface__administrator_id
    
    def get_table(self, teacher_id, classroom_name):
        table_op = sqldb.UserOperations()
        return table_op.show_students(teacher_id, classroom_name)

    @abstractmethod
    def account_information(self):
        pass

    @abstractmethod
    def class_details(self):
        pass

    @abstractmethod
    def student_details(self):
        pass

class TeacherInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

        self._classroom_name = ""
        self.classroom_year = ""

        while True:
            print("\n------------- Student Management System V1.0.0 ------------- \n" +
              "############################################################")
            print(f"{self.date_today.strftime('%A')}, {self.date_today.strftime('%B')}" +
              f" {self.date_today.strftime('%Y')}\n")
            print(f"Welcome to the SMS, {fname.title()}!\n")

            try:
                self.selection = {
                                1: "Manage and View Classrooms",
                                2: "Account Information",
                                3: "Help",
                                4: "Log-out"
                            }
                
                for k,v in self.selection.items():
                    print(f"\t{k}: {v}")

                self.teacher_selection = int(input("\nEnter an Option: "))

                if self.teacher_selection == 1:
                    self.class_details() 

                elif self.teacher_selection == 2:
                    self.account_information()

                elif self.teacher_selection == 3:
                    help_module.__doc__

                elif self.teacher_selection == 4:
                    while True:
                        try:
                            exit_selection = input("Are you sure you want to log out? (Y/N): ")

                            if exit_selection.lower() == "y":
                                print("Logging out...")
                                return None   
                            elif exit_selection.lower() == "n":
                                break

                        except Exception:
                            print("Please enter a valid value. \n")
                            continue

            except ValueError:
                print("Please enter a valid value. \n")
                continue
    
    def add_classroom(self):
        teacher_uid = int(self.get_teacher_id())

        while True:
            try:
                classrooms = sqldb.RegisterClassrooms()
                assign = sqldb.UserOperations()
                get_id = sqldb.DBOperations()

                cls_name = input("Enter the Course Name: ")
                yr_input = input("Enter the Course Year: ")
                classrooms.create_classroom(cls_name, teacher_uid, yr_input)

                class_id = get_id.get_classroom_id(cls_name, teacher_uid)
                assign.assign_teacher(teacher_uid, class_id)

                break

            except Exception as err:
                print("Something went wrong adding the classroom!")
                print(err)

            return False
    
    def print_student_info(self, student_info):
        student_info = student_info[0:5]
        print("")

        for i in range(len(student_info)):
            fields = ["Student ID", "First Name", "Last Name",
                        "Username", "Student Email"]
            
            print(f"{fields[i]}: {student_info[i]}")

        input("Enter anything to continue... ")
        return True
        
    def class_details(self):
        teacher_uid = self.get_teacher_id()
        class_lst = []
        student_info = []
        table_header = PrettyTable()

        while True:
            try:
                classrooms = sqldb.RegisterClassrooms()
                classroom_check = classrooms.check_classroom_table(teacher_uid)

                if not classroom_check or type(classroom_check) == None:
                    print("You are not assigned to any classroom(s)!")
                    time.sleep(0.5)
                    
                    while True:
                        create_select = input("Would you like to create one? (Y/N): ")

                        if create_select.lower() == "y":
                            self.add_classroom()
                            break
                        elif create_select.lower() == "n":
                            break
                        else:
                            print("Select a valid value! \n")
                            continue
                    break
                
                elif classroom_check:
                    print(f"Found {len(classroom_check)} Course(s). \n")

                    for i in range(len(classroom_check)):
                        class_lst.append(classroom_check[i][3])

                    for num, course in enumerate(class_lst, start=1):
                        print(f"{num} - {course}")

                    add_input = input("\nWould you like to add more classrooms? (Y/N): ")

                    if add_input.lower() == "y":
                        self.add_classroom()

                    elif add_input.lower() == "n":
                        try:
                            course_select = int(input("Select the course to view: "))
                            ind = course_select - 1 # Because the enumeration starts at 1

                            if (course_select > 0) and (course_select <= len(class_lst)):
                                op = sqldb.UserOperations()

                                while True:
                                    table_header.field_names = [class_lst[ind]]
                                    print(f"\n\n{table_header}")

                                    self.get_table(teacher_uid, class_lst[ind])
                                    cls_id = op.get_classroom_id(class_lst[ind], teacher_uid)

                                    try:
                                        class_options = {
                                            1: "View Student Information",
                                            2: "Add Students",
                                            3: "Remove Students",
                                            4: "Save Classroom Information",
                                            5: "Go Back"
                                        }

                                        print("")
                                        for k, v in class_options.items():
                                            print(f"{k} - {v}")
                                        individual_class_select = int(input("\nEnter an option: "))

                                    except ValueError:
                                        print("Please select a valid value. \n")
                                        continue

                                    if individual_class_select == 1:
                                        student_id = input("Enter the student ID: ")
                                        check_existing = op.student_exists_in_class(student_id, cls_id)

                                        if check_existing:
                                            pass
                                        else:
                                            print(f"The student with (ID: {student_id}) is not in this class! \n")
                                            continue

                                        view_info = op.student_id_exists(student_id)

                                        for i in view_info:
                                            student_info.append(i)
                                        self.print_student_info(student_info)
                                        student_info.clear()
                                    
                                    elif individual_class_select == 2:
                                        while True:
                                            add_input = input("Would you like to add more students? (Y/N): ")

                                            if add_input.lower() == "y":
                                                student_id = int(input("Enter the student's ID: "))
                                                op.add_student(student_id, cls_id)

                                                if not op or type(op) == None:
                                                    print(f"Adding Student of (ID: {student_id})" +
                                                            f" to Course of (ID: {cls_id}) was unsuccessful. \n")
                                                else:
                                                    print(f"Adding Student of (ID: {student_id})" +
                                                            f" to Course of (ID: {cls_id}) was successful! \n")

                                            elif add_input.lower() == "n":
                                                break
                                            else:
                                                print("Select a valid option. \n")
                                                continue

                                    elif individual_class_select == 3:
                                        while True:
                                            remove_input = input("\nWould you like to remove students? (Y/N): ")

                                            if remove_input.lower() == "y":
                                                remove_students = sqldb.UserOperations()

                                                student_id = int(input("Enter the student's ID: "))
                                                check_existing = op.student_exists_in_class(student_id, cls_id)

                                                if check_existing:
                                                    pass
                                                else:
                                                    print(f"The student with (ID: {student_id}) is not in this class! \n")
                                                    continue

                                                remove_students.remove_student(student_id, cls_id)

                                                if not remove_students or type(remove_students) == None:
                                                    print(f"Removing Student of (ID: {student_id})" +
                                                            f" from Course of (ID: {cls_id}) was unsuccessful. \n")
                                                else:
                                                    print(f"Removing Student of (ID: {student_id})" +
                                                            f" from Course of (ID: {cls_id}) was successful! \n")

                                            elif remove_input.lower() == "n":
                                                break
                                            else:
                                                print("Select a valid option. \n")
                                                continue

                                    elif individual_class_select == 4:
                                        save_input = input("\nWould you like to save classroom information? (Y/N): ")

                                        if save_input.lower() == "y":
                                            DOWNLOAD_DIRECTORY = pathlib.Path.home()/'Downloads'
                                            save_file = input("Enter a file name: ")

                                            with open(f"{DOWNLOAD_DIRECTORY}\\{save_file}.txt", "w", encoding="utf-8") as userfile:
                                                print("Clearing any data before handling...")
                                                userfile.write("")
                                            
                                            with open(f"{DOWNLOAD_DIRECTORY}\\{save_file}.txt", "w", encoding="utf-8") as userfile:
                                                userfile.write(str(op.show_students(teacher_uid, class_lst[ind])))

                                                print(f"Writing to {pathlib.Path.home()/'Downloads'}...")
                                                time.sleep(1)

                                                print("Write to file successful. \n")
                                                time.sleep(1)
                                                continue

                                        elif save_input.lower() == "n":
                                            pass

                                    elif individual_class_select == 5:
                                        exit_input = input("\nAre you sure you want to exit? (Y/N): ")

                                        if exit_input.lower() == "y":
                                            break
                                        elif exit_input.lower() == "n":
                                            continue

                            else:
                                print("Please select something in range! \n")
                                continue
                    
                        except ValueError as val_err:
                            print("Did you select the right value?")
                            print(val_err)
                            continue

                        except Exception as err:
                            print("Course Selection Error")
                            print(err)
                            break

                    else:
                        print("Please select a valid option. \n")
                        class_lst.clear()
                        continue

            except ValueError:
                print("Are you sure you entered the right values? \n")
                continue

            except Exception as err:
                print(err)
                time.sleep(0.5)

            return False

    def student_details(self):
        pass

    def account_information(self):
        information_table = PrettyTable()

        information_table.field_names = ["First Name", "Last Name", 
                                         "Username", "Email Address", 
                                         "Employee ID", "Password"]
        information_table.add_row([
            self.get_fname(), self.get_lname(),
            self.get_username(), self.get_email(),
            self.get_teacher_id(), self.get_password()
        ])

        print(information_table)
        input("Enter anything to continue... ")
        return
    
    def help_page(self):
        print(help_module.__doc__)
        return None
    
# ----------------------------------------------------------------------------------------------------------------- #

class AdminInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

        while True:
            print("\n------------- Student Management System V1.0.0 ------------- \n" +
              "############################################################")
            print(f"{self.date_today.strftime('%A')}, {self.date_today.strftime('%B')}" +
              f" {self.date_today.strftime('%Y')}\n")
            print(f"Welcome to the SMS, {fname.title()}!\n")

            try:
                self.selection = {
                                1: "Manage and View Classrooms",
                                2: "Manage and View Student Details",
                                3: "Account Information",
                                4: "Help",
                                5: "Log-out"
                            }
                
                for k,v in self.selection.items():
                    print(f"\t{k}: {v}")

                self.admin_selection = int(input("Enter an Option: "))

                if self.admin_selection == 1:
                    class_info = self.class_details()
                elif self.admin_selection == 2:
                    student_info = self.student_details()
                elif self.admin_selection == 3:
                    own_info = self.account_information()
                elif self.admin_selection == 4:
                    get_help = self.help_page()
                elif self.admin_selection == 5:
                    while True:
                        try:
                            exit_selection = input("Are you sure you want to log out? (Y/N): \n")

                            if exit_selection.lower() == "y":
                                print("Logging out...")
                                return
                            
                            elif exit_selection.lower() == "n":
                                break

                        except Exception:
                            print("Please enter a valid value. \n")
                            continue

            except ValueError:
                print("Please enter a valid value. \n")
                continue

    def class_details(self):
        pass

    def student_details(self):
        pass

    def account_information(self):
        print(f"\nFirst Name: {self.get_fname()}")
        print(f"Last Name: {self.get_lname()}")
        print(f"Username: {self.get_username()}")
        print(f"Email Address: {self.get_email()}")
        print(f"Password: {self.get_password()} \n")
        return
    
    def help_page(self):
        print(help_module.__doc__)
        return None
    
# ----------------------------------------------------------------------------------------------------------------- #

class StudentInterface(Interface):
    def __init__(self, fname, lname, username, email, password):
        super().__init__(fname, lname, username, email, password)

        while True:
            print("\n------------- Student Management System V1.0.0 ------------- \n" +
              "############################################################")
            print(f"{self.date_today.strftime('%A')}, {self.date_today.strftime('%B')}" +
              f" {self.date_today.strftime('%Y')}\n")
            print(f"Welcome to the SMS, {fname.title()}!\n")

            try:
                self.selection = {
                                1: "View Classrooms",
                                2: "View Student Details",
                                3: "Account Information",
                                4: "Help",
                                5: "Log-out"
                            }
                
                for k,v in self.selection.items():
                    print(f"\t{k}: {v}")

                self.student_selection = int(input("Enter an Option: "))

                if self.student_selection == 1:
                    class_info = self.class_details()
                elif self.student_selection == 2:
                    student_info = self.student_details()
                elif self.student_selection == 3:
                    own_info = self.account_information()
                elif self.student_selection == 4:
                    get_help = self.help_page()
                elif self.student_selection == 5:
                    while True:
                        try:
                            exit_selection = input("Are you sure you want to log out? (Y/N): \n")

                            if exit_selection.lower() == "y":
                                print("Logging out...")
                                return
                            
                            elif exit_selection.lower() == "n":
                                break

                        except Exception:
                            print("Please enter a valid value. \n")
                            continue

            except ValueError:
                print("Please enter a valid value. \n")
                continue

    def class_details(self):
        pass

    def student_details(self):
        pass

    def account_information(self):
        print(f"\nFirst Name: {self.get_fname()}")
        print(f"Last Name: {self.get_lname()}")
        print(f"Username: {self.get_username()}")
        print(f"Email Address: {self.get_email()}")
        print(f"Password: {self.get_password()} \n")
        return
    
    def help_page(self):
        print(help_module.__doc__)
        return None