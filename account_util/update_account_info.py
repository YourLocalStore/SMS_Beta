import sqldb

class UpdateInfo:
    def __init__(self, uid, user, email, password, role):
        self.__uid = uid
        self.user = user
        self.__email = email
        self.__password = password
        self.role = role # This is to know which table to update
        self.db_op = sqldb.DBOperations()

    def update_menu(self):
        while True:
            try:
                update_choices = {
                    1: "Change Username",
                    2: "Change Email",
                    3: "Change Password",
                    4: "Go Back"
                }

                print("\n============= Credential Update Screen =============")
                for k,v in update_choices.items():
                    print(f"\t{k}: {v}")
                
                choice = int(input("\nEnter a choice: "))

                if choice == 1:
                    new_user = input("Enter a new username: ")
                    self.update_username(new_user)
                elif choice == 2:
                    new_email = input("Enter a new email: ")
                    self.update_email(new_email)
                elif choice == 3:
                    new_pass = input("Enter a new password: ")
                    self.update_password(new_pass)
                elif choice == 4:
                    break

            except ValueError:
                print("Please enter a valid option!\n")
                continue

        return False
    
    def update_username(self, new_user):
        print("\nUpdating username...")
        if self.role == "Student":
            update_query = """UPDATE Students
                              SET UserName = %s
                              WHERE StudentID = %s"""
            vals = new_user, self.__uid
            self.db_op.db_cursor.execute(update_query, vals)
            
        elif self.role == "Teacher":
            update_query = """UPDATE Teachers
                              SET UserName = %s
                              WHERE TeacherID = %s"""
            vals = new_user, self.__uid
            self.db_op.db_cursor.execute(update_query, vals)
        
        elif self.role == "Administrator":
            update_query = """UPDATE Administrators
                              SET UserName = %s
                              WHERE AdministratorID = %s"""
            vals = new_user, self.__uid
            self.db_op.db_cursor.execute(update_query, vals)
        
        print("Username updated!")
        print(f"New username: {new_user}")
        self.db_op.sql_serv.commit()
        return True

    def update_email(self):
        if self.role == "Student":
            pass
        elif self.role == "Teacher":
            pass
        elif self.role == "Administrator":
            pass

    def update_password(self):
        if self.role == "Student":
            pass
        elif self.role == "Teacher":
            pass
        elif self.role == "Administrator":
            pass
