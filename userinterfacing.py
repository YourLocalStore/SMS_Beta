import main
import sqldb
import datetime
import help_module
import time

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
                    break

                elif self.teacher_selection == 5:
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
        
    def class_details(self):
        teacher_uid = self.get_teacher_id()
        class_lst = []

        while True:
            try:
                classrooms = sqldb.RegisterClassrooms()
                classroom_check = classrooms.check_classroom_table(teacher_uid)

                if not classroom_check or type(classroom_check) == None:
                    print("You are not assigned to any classroom(s)!")
                    time.sleep(0.5)

                    self.add_classroom()
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
                                show = op.show_students(teacher_uid, class_lst[ind])

                                if show or not show:
                                    add_input = input("\nWould you like to add more students? (Y/N): ")

                                    if add_input.lower() == "y":
                                        add_students = sqldb.UserOperations()

                                        student_id = int(input("Enter the student's ID: "))
                                        course_id = int(input("Enter the course ID: "))

                                        add_students.add_student(student_id, course_id)

                                        if not add_students or type(add_students) == None:
                                            print(f"Adding Student of (UID: {student_id})" +
                                                    " to Course of (ID: {course_id}) was unsuccessful. \n")
                                        else:
                                            print(f"Adding Student of (UID: {student_id})" +
                                                    f" to Course of (ID: {course_id}) was successful! \n")
                                            
                                    elif add_input.lower() == "n":
                                        break

                                elif type(show) == None:
                                    print("Unfortunately, trying to view the student table went wrong!")
                                    break

                            else:
                                print("Please select something in range! \n")
                                continue
                    
                        except ValueError as val_err:
                            print("Did you select the right value?")
                            print(err)
                            continue
                        except Exception as err:
                            print("Course Selection Error")
                            print(err)
                            break

            except ValueError:
                print("Are you sure you entered the right values? \n")
                continue
            except Exception as err:
                print("MAN")
                print(err)
                time.sleep(0.5)

            return False

    def student_details(self):
        pass

    def account_information(self):
        print("----------- Account Information -----------")
        print(f"\nFirst Name: {self.get_fname()}")
        print(f"Last Name: {self.get_lname()}\n")

        print(f"Username: {self.get_username()}")
        print(f"Email Address: {self.get_email()}")
        print(f"Employee ID: {self.get_teacher_id()}")
        print(f"Password: {self.get_password()} \n")

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