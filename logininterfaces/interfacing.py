import datetime
import time
import pathlib
import sqldb

from logininterfaces import help_module
from logininterfaces.interface_struct import Interface
from classroom_util.add_class import AddClassroom
from classroom_util.print_student_info import PrintInformation
from classroom_util.download_class_info import DownloadClass
from classroom_util.add_students import AddStudent
from classroom_util.remove_students import RemoveStudents
from account_util.get_account_info import GetUserInformation
from prettytable import PrettyTable


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
                            ind = course_select - 1 # Since the enumeration starts at 1, the index must be
                                                    # n - 1, otherwise the index will be out of range.

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
                                            4: "Download Classroom Information",
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
                                                student_op = AddStudent(student_id, cls_id)
                                                student_op.add_person()
                                            elif add_input.lower() == "n":
                                                break
                                            else:
                                                print("Select a valid option. \n")
                                                continue

                                    elif individual_class_select == 3:
                                        while True:
                                            remove_input = input("\nWould you like to remove students? (Y/N): ")

                                            if remove_input.lower() == "y":
                                                student_id = int(input("Enter the student's ID: "))
                                                remove_students = RemoveStudents(student_id, cls_id)
                                                remove_students.remove_person()
                                            elif remove_input.lower() == "n":
                                                break
                                            else:
                                                print("Select a valid option. \n")
                                                continue

                                    elif individual_class_select == 4:
                                        save_input = input("\nWould you like to save classroom information? (Y/N): ")

                                        if save_input.lower() == "y":
                                            download_op = DownloadClass(teacher_uid, class_lst[ind])
                                            download_op.download_file()
                                            break 
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

    def add_classroom(self):
        teacher_uid = int(self.get_teacher_id())
        add_op = AddClassroom(teacher_uid)
        add_op.create_class()
    
    def print_student_info(self, student_info):
        student_info = student_info[0:5]
        student_info_op = PrintInformation(student_info)
        student_info_op.print_student()
        
    def student_details(self):
        pass

    def account_information(self):
        account_info = GetUserInformation(self.getfname(), self.getlname(),
                                          self.get_username(), self.get_teacher_id(),
                                          self.get_password())
        print(account_info)
        input("Enter anything to continue... ")
        return
    
    def help_page(self):
        print(help_module.__doc__)
        return None

class AdminInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

class StudentInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super(self.Interface, self).__init__(fname, lname, username, email, password, teacher_id, administrator_id)

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

    def account_information(self):
        account_info = GetUserInformation(self.getfname(), self.getlname(),
                                          self.get_username(), self.get_teacher_id(),
                                          self.get_password())
        print(account_info)
        input("Enter anything to continue... ")
        return
    
    def student_details(self):
        pass
    
    def help_page(self):
        print(help_module.__doc__)
        return None
