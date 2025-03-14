import mysql.connector
import os
import time

from dotenv import load_dotenv
from mysql import *
from mysql.connector import errorcode
from passlib.hash import pbkdf2_sha256
from abc import ABC, abstractmethod
from threading import Thread

load_dotenv()

class ConnectSQLDatabase:
    db_name = "tester"

    def __init__(self):
        try:
            self.sql_serv = mysql.connector.connect(
                charset = "utf8",
                use_unicode = True,

                host = "localhost",
                port = "3306",

                user = os.environ.get("USER"),
                password = os.environ.get("PASSWORD"),
                connection_timeout = 300
            )
            self.db_cursor = self.sql_serv.cursor()

            try:
                self.db_cursor.execute(f"USE {self.db_name}")
                self.db_cursor.close()

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Connection failed due to password/username. \n")

                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(f"Attempting to create database {self.db_name}...")
                    ConnectSQLDatabase.create_db(self, self.db_cursor)

        except Exception as err:
            print("The database must be down... Please contact the creator!\n")
            return None

    def create_db(self, cursor):
        try:
            cursor.execute(f"CREATE DATABASE {self.db_name}")
            print(f"Database: {self.db_name} has been created. \n")

        except mysql.connector.Error as err:
            print("Could not create the database. \n")

    def get_db_cursor(self):
        return self.sql_serv.cursor()
    
class DBOperations(ConnectSQLDatabase):
    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def get_user_info(self, table_name, username):
        table_list = ["teachers", "students"]

        if table_name not in table_list:
            print(f"{table_name} does not exist.")
            return None
        
        else:
            for i in range(len(table_list)):
                if table_list[i] == table_name:
                    table_name = table_list[i]
                break

            print(table_name)

            try:
                row_query = f"""SELECT * FROM `{table_name}` WHERE UserName = %s"""

                self.db_cursor.execute(row_query, (username,))
                fetch_query = self.db_cursor.fetchone()

                print(fetch_query)
                return fetch_query

            except Exception as err:
                return None

    def get_table_names(self):
        table_queries = """SHOW TABLES"""

        self.db_cursor = self.sql_serv.cursor(buffered=True)
        self.db_cursor.execute(table_queries)

        table_data = self.db_cursor.fetchall()
        table_data = ' '.join(map(str, [i[0] for i in table_data])).split()

        print(table_data)
        return table_data

    def close_serv_connection(self):
        if self.sql_serv.is_connected:
            self.sql_serv.close()
            return "Closing connection..."
    
    def close_cursor_connection(self):
        return self.db_cursor.close()

class UserOperations(DBOperations, ConnectSQLDatabase):
    def __init__(self):
        super().__init__()

    def show_students(self):
        pass

    def add_student(self):
        pass

    def delete_student(self):
        pass
    
class LoginCheck(ABC):
    @abstractmethod
    def login_user_exists(self):
        pass

    @abstractmethod
    def login_pwd_check(self):
        pass

class StudentLoginCheck(ConnectSQLDatabase, LoginCheck):
    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def login_user_exists(self, username):
        try:
            check_individual = """SELECT * FROM students WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            user_exists = self.db_cursor.fetchone()

            if user_exists:
                return True
            else:
                print("The user does not exist! \n")
                return False
            
        except Exception as err:
            print(err)

    def login_pwd_check(self, username, pwd):
        try:
            check_individual = """SELECT password FROM students WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            pwd_valid = self.db_cursor.fetchone()

            if pwd_valid[0] == pwd:
                return True
            
            else:
                return False
              
        except Exception as err:
            raise err

class TeacherLoginCheck(ConnectSQLDatabase, LoginCheck):
    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def login_user_exists(self, username, employee_id):
        try:
            check_individual = """SELECT * FROM teachers WHERE UserName = %s"""
            check_id = """SELECT * FROM teachers WHERE TeacherID = %s"""
            
            individual_val = str(username)
            individual_id = int(employee_id)

            self.db_cursor.execute(check_individual, (individual_val,))
            user_exists = self.db_cursor.fetchone()

            self.db_cursor.execute(check_id, (individual_id,))
            uid_exists = self.db_cursor.fetchone()

            if user_exists and uid_exists:
                return True
            else:
                print("The user does not exist!")
                print("Did you enter your name and/or ID properly? \n")
                return False
            
        except Exception as err:
            raise err

    def login_pwd_check(self, username, pwd):
        try:
            check_individual = """SELECT password FROM teachers WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            pwd_valid = self.db_cursor.fetchone()

            if pwd_valid[0] == pwd:
                return True
            else:
                return False
              
        except Exception as err:
            print(err)

class AdminLoginCheck(ConnectSQLDatabase, LoginCheck):
    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def login_user_exists(self, username, employee_id):
        try:
            check_individual = """SELECT * FROM administrators WHERE UserName = %s"""
            check_id = """SELECT * FROM administrators WHERE TeacherID = %s"""
            
            individual_val = str(username)
            individual_id = int(employee_id)

            self.db_cursor.execute(check_individual, (individual_val,))
            user_exists = self.db_cursor.fetchone()

            self.db_cursor.execute(check_id, (individual_id,))
            uid_exists = self.db_cursor.fetchone()

            if user_exists and uid_exists:
                return True
            else:
                print("The user does not exist!")
                print("Did you enter your name and/or ID properly? \n")
                return False
            
        except Exception as err:
            raise err

    def login_pwd_check(self, username, pwd):
        try:
            check_individual = """SELECT password FROM administrators WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            pwd_valid = self.db_cursor.fetchone()

            if pwd_valid[0] == pwd:
                return True
            else:
                return False
              
        except Exception as err:
            raise err

class CreateRegisterTables(ConnectSQLDatabase):
    user_table = {}

    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor()

    def student_register_table(self):
        try:
            print("Checking for Student Table")
            time.sleep(1.5)

            self.user_table["Students"] = self.db_cursor.execute(
                """CREATE TABLE students( 
                StudentID int NOT NULL AUTO_INCREMENT, 
                FirstName varchar(255) not NULL, 
                LastName varchar(255) not NULL, 
                UserName varchar(20) not NULL, 
                EmailAddress varchar(255) not NULL, 
                Password varchar(64) not NULL, 
                PRIMARY KEY(StudentID))"""
            )

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Student table exists.\n")
                time.sleep(1.5)
                return True
            else:
                print(err)
        
        except Exception as exc:
            print("SQL Cursor -- Not Found! :(")
            print(exc)
            raise SystemExit

    def teacher_register_table(self):
        try:
            print("Checking for Teacher Table")
            time.sleep(1.5)

            self.user_table["Teachers"] = self.db_cursor.execute(
                """CREATE TABLE teachers( 
                TeacherID int NOT NULL AUTO_INCREMENT, 
                FirstName varchar(255) not NULL, 
                LastName varchar(255) not NULL, 
                UserName varchar(255) not NULL, 
                EmailAddress varchar(255) not NULL, 
                Password varchar(64) not NULL, 
                PRIMARY KEY(TeacherID))"""
            )

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Teacher table exists.\n")
                time.sleep(1.5)
                return True
            else:
                print(err)
        
        except Exception as exc:
            print("SQL Cursor -- Not Found! :(")
            print(exc)
            raise SystemExit
    
class RegisterPerson(ConnectSQLDatabase):
    def __init__(self, fname, lname, username, email, password):
        super().__init__()
        
        self.__fname = fname
        self.__lname = lname
        self.__email = email
        self.username = username
        self.__password = password

        self.db_cursor = self.sql_serv.cursor()

    def get_student_uid(self):
        student_user_id = self.db_cursor.execute(
            f"SELECT FROM students WHERE UserName = {self.username}"
        )

        student_user_id = self.db_cursor.fetchone()
        return student_user_id
    
    def get_teacher_uid(self):
        teacher_user_id = self.db_cursor.execute(
            f"SELECT FROM teachers WHERE UserName = {self.username}"
        )

        get_teacher_uid = self.db_cursor.fetchone()
        return get_teacher_uid

    def register_teacher(self, fname, lname, username, email, password):
        try:

            register_query = """INSERT INTO teachers(FirstName, LastName, UserName, EmailAddress, Password) 
                                VALUES (%s, %s, %s, %s, %s)"""
            register_val = (fname, lname, username, email, password)

            check_individual = """SELECT * FROM teachers WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            res = self.db_cursor.fetchone()

            if res:
                print("The username already exists!")
                return True

            else:
                self.db_cursor.execute(register_query, register_val)
                self.sql_serv.commit()
                return False

        except Exception as err:
            print(err)
            pass

    def register_student(self, fname, lname, username, email, password):
        try:
            # self.db_cursor.execute("TRUNCATE TABLE users")
            # self.sql_serv.commit()

            register_query = """INSERT INTO students(FirstName, LastName, UserName, EmailAddress, Password) 
                                VALUES (%s, %s, %s, %s, %s)"""
            register_val = (fname, lname, username, email, password)

            check_individual = """SELECT * FROM students WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            res = self.db_cursor.fetchone()

            if res:
                print("The username already exists!")
                return True

            else:
                self.db_cursor.execute(register_query, register_val)
                self.sql_serv.commit()
                return False

        except Exception as err:
            print(err)
            pass

class CheckDBState(DBOperations):
    """

    ** Debugging purposes only**

    """
    def __init__(self):
        super().__init__()
    
    def check_dbs(self):
        self.db_cursor = self.sql_serv.cursor()
        self.db_cursor.execute("SHOW DATABASES")

        databases = self.db_cursor.fetchall()

        return f"Current Databases in '{self.db_name}': " + \
               f"{', '.join(map(str, [i[0] for i in databases]))}"
    
    def return_status(self):
        if self.sql_serv.is_connected:
            return True
        else:
            return False
    
    @staticmethod
    def try_connection():
        connect_db = ConnectSQLDatabase()

def main():
    pass

if __name__ == "__main__":
    main()