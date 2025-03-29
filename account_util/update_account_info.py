import sqldb

class UpdateInfo():
    """ A class that aims to update the user's information depending on the role that is passed into it. 

    Attributes:
        uid (str): The user's ID.
        user (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        role (str): The role of the user, i.e. Student, teacher, administrator.
        db_op (obj): The instantiation of the DBOperations() class in sqldb.py

    Methods:
        __init__(self):
            The constructor for the attributes (ID, username, email, password, role, db_op).

        def update_menu(self):
            The method that asks the user was the class name and grade/year should be. Using these values, it then registers
            the classroom accordingly, along with some sort of identifier (classroom ID, section), then assigns the teacher
            who created it.
        
        def check_dupe_username(self, username):
            The method that checks whether or not a user is attempting to create a username that is the same
            as another in their current table. Each username is unique and can only be created once in the database.

        def check_dupe_email(self, email):
            The method that checks whether or not a user is attempting to use an email address that is the same
            as another in their current table. Each email address is unique and can only be created once in the database.
            
        def update_username(self, new_user):
            The method that applies a username change depending on the role that is being passed into the class.
            It first checks whether or not the user enters an existing username using the check_dupe_username method.

        def update_email(self, new_email):
            The method that applies a email address change depending on the role that is being passed into the class.
            It first checks whether or not the user enters an existing address using the check_dupe_email method.

        def update_password(self, new_pwd):
            The method that applies a password change depending on the role that is being passed into the class.
            No checks are needed since passwords should not be unique. 
    """

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
                print("")
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
    
    def check_dupe_username(self, username):
        username_dupe_query = f"""SELECT UserName FROM {self.role + "s"} WHERE UserName = %s"""
        user_val = username

        self.db_op.db_cursor.execute(username_dupe_query, (user_val,))
        res = self.db_op.db_cursor.fetchall()
        if len(res) >= 1:
            print("You or someone else already has the same username!")
            return True
        else:
            return False
        
    def check_dupe_email(self, email):
        username_dupe_query = f"""SELECT EmailAddress FROM {self.role.lower() + "s"} WHERE EmailAddress = %s"""
        user_val = email

        self.db_op.db_cursor.execute(username_dupe_query, (user_val,))
        res = self.db_op.db_cursor.fetchall()
        if len(res) >= 1:
            print("You or someone else already has the same email address!")
            return True
        else:
            return False
        
    def update_username(self, new_user):
        print("\nUpdating username...")

        if self.role == "Student":
            dupe = self.check_dupe_username(new_user)
            if dupe:
                return None
            else:
                update_query = """UPDATE students
                                SET UserName = %s
                                WHERE StudentID = %s"""
                vals = new_user, self.__uid
                self.db_op.db_cursor.execute(update_query, vals)
            
        elif self.role == "Teacher":
            dupe = self.check_dupe_username(new_user)
            if dupe:
                return None
            else:
                update_query = """UPDATE teachers
                                SET UserName = %s
                                WHERE TeacherID = %s"""
                vals = new_user, self.__uid
                self.db_op.db_cursor.execute(update_query, vals)
        
        elif self.role == "Administrator":
            dupe = self.check_dupe_username(new_user)
            if dupe:
                return None
            else:
                update_query = """UPDATE administrators
                                SET UserName = %s
                                WHERE AdministratorID = %s"""
                vals = new_user, self.__uid
                self.db_op.db_cursor.execute(update_query, vals)
        
        print("Username updated!")
        print(f"New username: {new_user}")
        self.db_op.sql_serv.commit()
        return True

    def update_email(self, new_email):
        print("\nUpdating Email Address...") 
        if self.role == "Student":
            dupe = self.check_dupe_email(new_email)
            if dupe:
                return None
            else:
                update_query = """UPDATE students
                                    SET EmailAddress = %s
                                    WHERE StudentID = %s"""
                vals = new_email, self.__uid
                self.db_op.db_cursor.execute(update_query, vals)
            
        elif self.role == "Teacher":
            dupe = self.check_dupe_email(new_email)
            if dupe:
                return None
            else:
                update_query = """UPDATE teachers
                                SET EmailAddress = %s
                                WHERE TeacherID = %s"""
                vals = new_email, self.__uid
                self.db_op.db_cursor.execute(update_query, vals)
        
        elif self.role == "Administrator":
            dupe = self.check_dupe_email(new_email)
            if dupe:
                return None
            else:
                update_query = """UPDATE administrators
                                SET EmailAddress = %s
                                WHERE AdministratorID = %s"""
                vals = new_email, self.__uid
                self.db_op.db_cursor.execute(update_query, vals)
        
        print("Email updated!")
        print(f"New email address: {new_email}")
        self.db_op.sql_serv.commit()
        return True

    def update_password(self, new_pwd):
        print("\nUpdating Email Password...")
        if self.role == "Student":
            update_query = """UPDATE students
                              SET Password = %s
                              WHERE StudentID = %s"""
            vals = new_pwd, self.__uid
            self.db_op.db_cursor.execute(update_query, vals)
            
        elif self.role == "Teacher":
            update_query = """UPDATE teachers
                              SET Password = %s
                              WHERE TeacherID = %s"""
            vals = new_pwd, self.__uid
            self.db_op.db_cursor.execute(update_query, vals)
        
        elif self.role == "Administrator":
            update_query = """UPDATE administrators
                              SET Password = %s
                              WHERE AdministratorID = %s"""
            vals = new_pwd, self.__uid
            self.db_op.db_cursor.execute(update_query, vals)
        
        print("Password updated!")
        print(f"New password: {new_pwd}")
        self.db_op.sql_serv.commit()
        return True