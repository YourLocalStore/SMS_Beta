import main
import sqldb
import datetime

from abc import ABC, abstractmethod

class Interface(ABC, main.LoginInterface):
    def __init__(self, fname, lname, username, email, password):
        super().__init__(fname, lname, username, email, password)
        self.date_today = datetime.datetime.now()

        print("\n------------- Student Management System V1.0.0 ------------- \n" +
              "############################################################")

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
    def __init__(self, fname, lname, username, email, password):
        super().__init__(fname, lname, username, email, password)

        while True:
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

                self.teacher_selection = int(input("\nEnter an Option: "))

                if self.teacher_selection == 1:
                    class_info = self.class_details() 
                elif self.teacher_selection == 2:
                    student_info = self.student_details()
                elif self.teacher_selection == 3:
                    own_info = self.account_information()
                elif self.teacher_selection == 4:
                    pass
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

    def account_information(self):
        print(f"\nFirst Name: {self.get_fname()}")
        print(f"Last Name: {self.get_lname()}")
        print(f"Username: {self.get_username()}")
        print(f"Email Address: {self.get_email()}")
        print(f"Password: {self.get_password()} \n")
        return

    def student_details(self):
        pass
    def class_details(self):
        pass

class AdminInterface(Interface):
    def __init__(self, fname, lname, username, email, password):
        super().__init__(fname, lname, username, email, password)

        while True:
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
                    pass
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

    def account_information(self):
        print(f"\nFirst Name: {self.get_fname()}")
        print(f"Last Name: {self.get_lname()}")
        print(f"Username: {self.get_username()}")
        print(f"Email Address: {self.get_email()}")
        print(f"Password: {self.get_password()} \n")
        return
    
    def student_details(self):
        pass
    def class_details(self):
        pass

class StudentInterface(Interface):
    def __init__(self, fname, lname, username, email, password):
        super().__init__(fname, lname, username, email, password)

        while True:
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
                    pass
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

    def account_information(self):
        print(f"\nFirst Name: {self.get_fname()}")
        print(f"Last Name: {self.get_lname()}")
        print(f"Username: {self.get_username()}")
        print(f"Email Address: {self.get_email()}")
        print(f"Password: {self.get_password()} \n")
        return
    
    def class_details(self):
        pass
    def student_details(self):
        pass
