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
from account_util.update_account_info import UpdateInfo
from classroom_util.update_classroom import UpdateClass
from prettytable import PrettyTable

class TeacherInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

        while True:
            print("\n============= Student Management System V1.0.0 ============= \n" +
              "############################################################")
            print(f"\n{self.date_today.strftime('%A')}, {self.date_today.strftime('%B')}" +
              f" {self.date_today.strftime('%Y')}\n")
            print(f"Welcome to the SMS, {fname.title()}!\n")

            try:
                self.selection = {
                                1: ("Manage and View Courses", self.class_details),
                                2: ("View Account Information", self.account_information),
                                3: ("Update Account Information", self.update_account_information),
                                4: ("Log-out", None)
                            }
                
                for k, v in self.selection.items():
                    print(f"\t{k}: " + f"{v[0]}".strip("'"))

                print("")
                self.teacher_selection = int(input("Enter an Option: "))

                if self.teacher_selection == 4:
                    log = self.exit_interface()
                    if not log:
                        break
                elif (self.teacher_selection >= 1 and self.teacher_selection <= 3):
                    self.selection[self.teacher_selection][1]()
                else:
                    print("Please enter a valid value. \n")
                    continue                

            except ValueError:
                print("Please enter a valid value. \n")
                continue
        
    def class_details(self):
        teacher_uid = self.get_teacher_id()

        class_lst = []
        section_lst = []
        class_id_lst = []
        student_info = []

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
                        class_id_lst.append(classroom_check[i][0])
                        class_lst.append(classroom_check[i][3])
                        section_lst.append(classroom_check[i][4])

                    for num, course in enumerate(class_lst, start=1):
                        print(f"{num} - {course} (Section {section_lst[num - 1]}) (ID {class_id_lst[num - 1]})")

                    add_input = input("\nWould you like to add more classrooms? (Y/N): ")

                    if add_input.lower() == "y":
                        self.add_classroom()
                    elif add_input.lower() == "n":
                        try:
                            course_select = int(input("\nSelect the course to view: "))
                            ind = course_select - 1 # Since the enumeration starts at 1, the index must be
                                                    # n - 1, otherwise the index will be out of range.

                            if (course_select > 0) and (course_select <= len(class_lst)):
                                op = sqldb.UserOperations()

                                while True:
                                    self.get_table(teacher_uid, class_lst[ind], class_id_lst[ind])
                                    cls_id = op.get_classroom_id(class_lst[ind], teacher_uid, section_lst[ind])

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
                                            print(f"\t{k}: {v}")
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
                                        while True:
                                            exit_input = input("\nAre you sure you want to exit? (Y/N): ")

                                            if exit_input.lower() == "y":
                                                break
                                            elif exit_input.lower() == "n":
                                                continue
                                            else:
                                                print("Enter a valid value. \n")
                                                continue
                                        break
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

            break

    def add_classroom(self):
        teacher_uid = int(self.get_teacher_id())
        add_op = AddClassroom(teacher_uid)
        add_op.create_class()
    
    def print_student_info(self, student_info):
        student_info = student_info[0:5]
        student_info_op = PrintInformation(student_info)
        student_info_op.print_student()

    def account_information(self):
        print("\nViewing account details...\n")
        account_info = GetUserInformation(self.get_fname(), self.get_lname(),
                                          self.get_username(), self.get_email(),
                                          self.get_teacher_id(), self.get_password())
        print(account_info)
        input("\nEnter anything to continue... ")
        return
    
    def update_account_information(self):
        upd_info = UpdateInfo(self.get_teacher_id(), self.get_username(),
                              self.get_email(), self.get_password(), 
                              role="Teacher")
        upd_info.update_menu()

    def student_details(self):
        pass

    @staticmethod
    def exit_interface():
        while True:
            try:
                exit_selection = input("\nAre you sure? (Y/N): ")

                if exit_selection.lower() == "y":
                    print("Exiting...")
                    return False
                elif exit_selection.lower() == "n":
                    break

            except Exception:
                print("Please enter a valid value. \n")
                continue

class AdminInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)

        while True:
            print("\n------------- Student Management System V1.0.0 ------------- \n" +
              "############################################################")
            print(f"\n{self.date_today.strftime('%A')}, {self.date_today.strftime('%B')}" +
              f" {self.date_today.strftime('%Y')}\n")
            print(f"Welcome to the SMS, {fname.title()}!\n")

            try:
                self.selection = {
                                1: ("View and Edit Courses", self.view_all_courses),
                                2: ("View Account Information", self.account_information),
                                3: ("Update Account Information", self.update_account_information),
                                4: ("Log-out", None)
                            }
                
                for k, v in self.selection.items():
                    print(f"\t{k}: " + f"{v[0]}".strip("'"))

                print("")
                self.admin_selection = int(input("Enter an Option: "))

                if self.admin_selection == 4:
                    log = self.exit_interface()
                    if not log:
                        break
                elif (self.admin_selection >= 1 and self.admin_selection <= 4):
                    self.selection[self.admin_selection][1]()
                else:
                    print("Please enter a valid value. \n")
                    continue

            except ValueError:
                print("Please enter a valid value. \n")
                continue

    def view_all_courses(self):
        classroom_op = sqldb.DBOperations()
        classroom_op.get_all_classrooms()

        while True:
            class_edit_opt = input("\nWould you like to view a specific class? (Y/N): ")

            if class_edit_opt.lower() == "y":
                self.view_individual_class()
                break
            elif class_edit_opt.lower() == "n":
                break
            else:
                print("Select a valid option. \n")
                continue

        while True:
            class_edit_opt = input("\nWould you like to edit a class? (Y/N): ")

            if class_edit_opt.lower() == "y":
                self.edit_courses()
                break
            elif class_edit_opt.lower() == "n":
                return None
            else:
                print("Select a valid option. \n")
                continue

    def edit_courses(self):
        classroom_op = sqldb.DBOperations()

        class_id = int(input("Enter the classroom by ID: "))
        check_details = classroom_op.get_classroom_from_id(class_id)

        if check_details:
            print("\nUpdating course details...\n")
            upd_info = UpdateClass(class_id, check_details[1],
                                  check_details[2], check_details[3], 
                                  check_details[4])
            upd_info.update_menu()
        else:
            print("This class does not exist!")
            print("Are you sure you selected the right ID? \n")
        
        input("Enter anything to continue... ")
        return True
    
    def view_individual_class(self):
        pass
    
    def account_information(self):
        account_op = sqldb.UserOperations()
        while True:
            try:
                print("\n======== Account Information ======== ")
                self.selection = {
                                1: ("Students", None),
                                2: ("Teachers", None),
                                3: ("Current Account (You)", None),
                                4: ("Go Back", None)
                            }
                for k, v in self.selection.items():
                    print(f"\t{k}: " + f"{v[0]}".strip("'"))    
                print("") 
                account_selection = int(input("Enter an option: "))  

            except ValueError:
                print("Please select a valid option. \n")
                continue

            if account_selection == 1:
                account_op.show_all_students()
                input("Enter anything to continue... ")
                continue

            elif account_selection == 2:
                account_op.show_all_teachers()
                input("Enter anything to continue... ")
                continue

            elif account_selection == 3:
                print("\nViewing account details...\n")
                account_info = GetUserInformation(self.get_fname(), self.get_lname(),
                                                  self.get_username(), self.get_email(),
                                                  self.get_admin_id(), self.get_password())
                print(account_info)
                input("\nEnter anything to continue... ")
                return
            
            elif account_selection == 4:
                get_exit_select = self.exit_interface()
                if not get_exit_select:
                    break
            else:
                print("Please select a valid option. \n")
                continue

    def update_account_information(self):
        account_op = sqldb.UserOperations()
        account_db_op = sqldb.DBOperations()
        while True:
            try:
                print("\n======== Update Account Information ======== ")
                self.selection = {
                                1: ("Students", None),
                                2: ("Teachers", None),
                                3: ("Current Account (You)", None),
                                4: ("Go Back", None)
                            }
                print("") 
                for k, v in self.selection.items():
                    print(f"\t{k}: " + f"{v[0]}".strip("'"))    
                account_selection = int(input("\nEnter an option: "))

            except ValueError:
                print("Please enter a valid value.")
                continue

            if account_selection == 1:
                account_op.show_all_students()

                student_selection_id = int(input("\nEnter a student based on ID: "))
                check_details = account_db_op.get_student_from_id(student_selection_id)

                if check_details:
                    print("\nUpdating account details...\n")
                    upd_info = UpdateInfo(student_selection_id, check_details[3],
                                          check_details[4], check_details[5], 
                                          role="Student")
                    upd_info.update_menu()
                else:
                    print("This user does not exist!")
                    print("Are you sure you selected the right ID? \n")

                input("Enter anything to continue... ")
                continue

            elif account_selection == 2:
                account_op.show_all_teachers()

                teacher_selection_id = int(input("\nEnter a teacher based on ID: "))
                check_details = account_db_op.get_student_from_id(teacher_selection_id)

                if check_details:
                    print("\nUpdating account details...\n")
                    upd_info = UpdateInfo(teacher_selection_id, check_details[3],
                                          check_details[4], check_details[5], 
                                          role="Teacher")
                    upd_info.update_menu()
                else:
                    print("This user does not exist!")
                    print("Are you sure you selected the right ID? \n")

                input("Enter anything to continue... ")
                continue

            elif account_selection == 3:
                print("\nUpdating own account details...\n")
                upd_info = UpdateInfo(self.get_admin_id(), self.get_username(),
                                      self.get_email(), self.get_password(), 
                                      role="Administrator")
                upd_info.update_menu()
                continue
            
            elif account_selection == 4:
                get_exit_select = self.exit_interface()
                if not get_exit_select:
                    break
            else:
                print("Please select a valid option. \n")
                continue
    
    def student_details(self):
        pass

    def class_details(self):
        pass

    @staticmethod
    def exit_interface():
        while True:
            try:
                exit_selection = input("\nAre you sure? (Y/N): ")

                if exit_selection.lower() == "y":
                    print("Exiting...")
                    return False
                elif exit_selection.lower() == "n":
                    break

            except Exception:
                print("Please enter a valid value. \n")
                continue

class StudentInterface(Interface):
    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id, student_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)
        self._student_id = student_id

        while True:
            print("\n------------- Student Management System V1.0.0 ------------- \n" +
              "############################################################")
            print(f"\n{self.date_today.strftime('%A')}, {self.date_today.strftime('%B')}" +
              f" {self.date_today.strftime('%Y')}\n")
            print(f"Welcome to the SMS, {fname.title()}!\n")

            try:
                self.selection = {
                                1: ("View Your Courses", self.class_details),
                                2: ("View Account Information", self.account_information),
                                3: ("Update Account Information", self.update_account_information),
                                4: ("Log-out", None)
                            }
                
                for k, v in self.selection.items():
                    print(f"\t{k}: " + f"{v[0]}".strip("'"))

                print("")
                self.student_selection = int(input("Enter an Option: "))

                if self.student_selection == 4:
                    log = self.exit_interface()
                    if not log:
                        break
                elif (self.student_selection >= 1 and self.student_selection <= 3):
                    self.selection[self.student_selection][1]()
                else:
                    print("Please enter a valid value. \n")
                    continue

            except ValueError:
                print("Please enter a valid value. \n")
                continue

    @staticmethod
    def exit_interface():
        while True:
            try:
                exit_selection = input("\nAre you sure you want to log out? (Y/N): ")

                if exit_selection.lower() == "y":
                    print("Logging out...")
                    return False
                elif exit_selection.lower() == "n":
                    break

            except Exception:
                print("Please enter a valid value. \n")
                continue

    def class_details(self):
        class_check_op = sqldb.DBOperations()
        result = class_check_op.get_student_classnames(self._student_id)

        if not result or type(result) == None:
            return "You are not assigned to any classrooms yet. \n"
        
        elif result:
            while True:
                print(f"Found {len(result)} Course(s). \n")
                for i in range(len(result)):
                    result[i] = result[i][0][0]
                for num, course in enumerate(result, start=1):
                    print(f"{num} - {course}")

                while True:
                    try:
                        course_select = int(input("\nSelect the course to view: "))
                        ind = course_select - 1 
                    
                        if (course_select > 0) and (course_select <= len(result)):
                            teacher_id = class_check_op.get_class_teacher_id(self._student_id, result[ind])
                            class_id = class_check_op.get_student_class_id(self._student_id, result[ind])
                            self.view_classroom(teacher_id, result[ind], class_id)

                            input("\nEnter anything to continue... ")
                            break

                    except ValueError:
                        print("Are you sure you picked a valid value?\n")
                        continue

                break
            return False
    
    def view_classroom(self, teacher_id, class_name, class_id):
        return self.get_students_table(teacher_id, class_name, class_id)

    def account_information(self):
        print("\nViewing account details...\n")
        account_info = GetUserInformation(self.get_fname(), self.get_lname(),
                                          self.get_username(), self.get_email(),
                                          self._student_id, self.get_password())
        print(account_info)
        input("\nEnter anything to continue... ")
        return
    
    def update_account_information(self):
        upd_info = UpdateInfo(self._student_id, self.get_username(),
                              self.get_email(), self.get_password(), 
                              role="Student")
        upd_info.update_menu()
    
    def student_details(self):
        pass
