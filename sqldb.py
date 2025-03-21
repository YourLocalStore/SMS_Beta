import mysql.connector
import os
import time

from dotenv import load_dotenv
from mysql import *
from mysql.connector import errorcode
from passlib.hash import pbkdf2_sha256
from prettytable import PrettyTable, from_db_cursor
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

                host = "127.0.0.1",
                port = "3306",

                user = "root",
                password = "ENTER YOUR DB PASSWORD HERE",
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
            print(err)
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

    # This is only for main.py's login/register screen.
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
            try:
                row_query = f"""SELECT * FROM `{table_name}` WHERE UserName = %s"""

                self.db_cursor.execute(row_query, (username,))
                fetch_query = self.db_cursor.fetchone()
                return fetch_query

            except Exception as err:
                print(err)
                return None
    
    def student_exists_in_class(self, student_id, classroom_id):
        try:
            check_query = """SELECT * FROM student_classroom WHERE StudentID = %s AND ClassroomID = %s"""
            student_id_val = student_id
            classroom_id_val = classroom_id

            self.db_cursor.execute(check_query, (student_id_val, classroom_id_val,))
            existing = self.db_cursor.fetchone()

            if type(existing) == None:
                print(f"The student with (ID: {student_id}) is not in this class.")
            else:
                return True

        except Exception:
            print("Something went wrong checking class for student...")
    
    def student_id_exists(self, student_id):
        try:
            # Check if the student ID exists, otherwise goes against the foreign key constraint
            check_query = """SELECT * FROM students WHERE StudentID = %s"""
            id_val = student_id
            self.db_cursor.execute(check_query, (id_val,))

            existing = self.db_cursor.fetchone()

            if type(existing) == None:
                print(f"The student with (ID: {student_id}) does not exist.")
            else:
                return True
            
        except Exception:
            print("Something went wrong checking student IDs...")

        finally:
            return existing
        
    def get_classroom_id(self, course, teacher_id):
        try:
            id_query = """SELECT ClassroomID FROM classrooms WHERE CourseName = %s and TeacherID = %s"""
            self.db_cursor.execute(id_query, (course, teacher_id))

            fetch_query = self.db_cursor.fetchone()
            return fetch_query[0]

        except Exception:
            return None

    def get_table_names(self):
        table_queries = """SHOW TABLES"""

        self.db_cursor = self.sql_serv.cursor(buffered=True)
        self.db_cursor.execute(table_queries)

        table_data = self.db_cursor.fetchall()
        table_data = ' '.join(map(str, [i[0] for i in table_data])).split()

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
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def show_students(self, teacher_id, classroom_name):
        try:
            student_table = PrettyTable()

            show_query = """ 
            SELECT teachers.TeacherID AS TEACHER_ID,
                    students.FirstName AS STUDENT_FIRST_NAME,
                    students.LastName AS STUDENT_LAST_NAME,
                    students.StudentID AS STUDENT_ID,
                    classrooms.ClassroomID AS CLASSROOM_ID
            FROM students
            INNER JOIN student_classroom ON students.StudentID = student_classroom.StudentID
            INNER JOIN classrooms ON student_classroom.ClassroomID = classrooms.ClassroomID
            INNER JOIN teacher_classroom ON classrooms.ClassroomID = teacher_classroom.ClassroomID
            INNER JOIN teachers ON teacher_classroom.TeacherID = teachers.TeacherID
            WHERE teachers.TeacherID = %s AND classrooms.CourseName = %s;
            """

            self.db_cursor.execute(show_query, (teacher_id, classroom_name))

            student_table = from_db_cursor(self.db_cursor)

            query_res = self.db_cursor.fetchall()

            if query_res:
                print(f"\n{student_table}\n")
                return True
            else:
                print(f"\n{student_table}")
                return False

        except Exception as err:
            print("Unfortunately, trying to view the student table went wrong!")
            print(err)

        finally:
            return str(student_table)
            
    def add_student(self, student_id, class_id):
        try:
            exists = DBOperations()
            student_exists = exists.student_id_exists(student_id)

            if type(student_exists) == None:
                print("Student does not exist... \n")

            if student_exists:
                insert_query = """ 
                INSERT INTO student_classroom(StudentID, ClassroomID) VALUES(%s, %s)
                """

                self.db_cursor.execute(insert_query, (int(student_id), int(class_id)))
                self.sql_serv.commit()
                return True
            else:
                print('womp')
                return False

        except Exception as err:
            print("\n-- Adding Student Error")
            print("Something went wrong trying to add students!")
            print("Are you sure that the student and/or class IDs exist?")
            return False
        
    def remove_student(self, student_id, classroom_id):
        try:
            remove_query = """
            DELETE FROM student_classroom WHERE StudentID = %s AND ClassroomID = %s
            """
            student_id_val = student_id
            classroom_id_val = classroom_id

            self.db_cursor.execute(remove_query, (student_id_val, classroom_id_val,))
            self.sql_serv.commit()
            return True
        
        except Exception as err:
            print(err)

    def assign_teacher(self, teacher_id, class_id):
        try:
            insert_query = """ 
            INSERT INTO teacher_classroom(`TeacherID`, `ClassroomID`) VALUES(%s, %s)
            """

            self.db_cursor.execute(insert_query, (teacher_id, class_id))
            self.sql_serv.commit()

            print(f"Teacher of (ID: {teacher_id}) successfully assigned to classroom of (ID: {class_id}).")
            return True

        except Exception as err:
            print("\nassign teacher error")
            print(err)
            raise SystemExit

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
            check_individual = """SELECT * FROM `teachers` WHERE UserName = %s"""
            check_id = """SELECT * FROM `teachers` WHERE TeacherID = %s"""
            
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
            check_individual = """SELECT password FROM `teachers` WHERE UserName = %s"""
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
            check_individual = """SELECT * FROM `administrators` WHERE UserName = %s"""
            check_id = """SELECT * FROM `administrators` WHERE TeacherID = %s"""
            
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
            check_individual = """SELECT password FROM `administrators` WHERE UserName = %s"""
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
            #time.sleep(1.5)

            self.user_table["Students"] = self.db_cursor.execute(
                """CREATE TABLE `students`( 
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
                #time.sleep(1.5)
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
            #time.sleep(1.5)

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
                #time.sleep(1.5)
                return True
            else:
                print(err)
        
        except Exception as exc:
            print("SQL Cursor -- Not Found! :(")
            print(exc)
            raise SystemExit
        
    def classroom_table(self):
        try:
            print("Checking for Classrooms...")
            #time.sleep(1.5)

            self.user_table["Classrooms"] = self.db_cursor.execute(
                """CREATE TABLE Classrooms( 
                ClassroomID int NOT NULL AUTO_INCREMENT,
                TeacherID int NOT NULL,
                Grade int NOT NULL,
                CourseName TEXT NOT NULL, 
                PRIMARY KEY(ClassroomID))"""
            )

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Classrooms table exists.\n")
                #time.sleep(1.5)
                return True
            else:
                print(err)
        
        except Exception as exc:
            print("SQL Cursor -- Not Found! :(")
            print(exc)
            raise SystemExit
        
    def student_classroom_tables(self):
        try:
            print("Checking for Student-Classroom Table Relations...")
            #time.sleep(1.5)

            self.user_table["student_classroom"] = self.db_cursor.execute(
                """CREATE TABLE student_classroom( 
                StudentID int NOT NULL,
                ClassroomID int NOT NULL,
                FOREIGN KEY(StudentID) 
                    REFERENCES students(StudentID)
                    ON DELETE CASCADE,
                FOREIGN KEY(ClassroomID) 
                    REFERENCES classrooms(ClassroomID)
                    ON DELETE CASCADE
                )
                """
            )

            # self.user_table["student_classroom"] = self.db_cursor.execute(
            #     """CREATE TABLE student_classroom( 
            #     StudentID int NOT NULL,
            #     ClassroomID int NOT NULL)
            #     """
            # )

            # self.db_cursor.execute("TRUNCATE TABLE student_classroom")
            # self.sql_serv.commit()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("-- Good! \n")
                #time.sleep(1.5)
                return True
            else:
                print(err)
        
        except Exception as exc:
            print("SQL Cursor -- Not Found! :(")
            print(exc)
            raise SystemExit

    def teacher_classroom_tables(self):
        try:
            print("Checking for Teacher-Classroom Table Relations...")
            #time.sleep(1.5)

            self.user_table["teacher_classroom"] = self.db_cursor.execute(
                """CREATE TABLE teacher_classroom( 
                TeacherID int NOT NULL, 
                ClassroomID int NOT NULL,
                FOREIGN KEY(TeacherID) 
                    REFERENCES teachers(TeacherID)
                    ON DELETE CASCADE,
                FOREIGN KEY(ClassroomID) 
                    REFERENCES classrooms(ClassroomID)
                    ON DELETE CASCADE
                )
                """
            )

            # self.user_table["teacher_classroom"] = self.db_cursor.execute(
            #     """CREATE TABLE teacher_classroom( 
            #     TeacherID int NOT NULL, 
            #     ClassroomID int NOT NULL)
            #     """
            # )

            # self.db_cursor.execute("TRUNCATE TABLE teacher_classroom")
            # self.sql_serv.commit()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("-- Good! \n")
                #time.sleep(1.5)
                return True
            else:
                print(err)
        
        except Exception as exc:
            print("SQL Cursor -- Not Found! :(")
            print(exc)
            raise SystemExit
        
class RegisterClassrooms(DBOperations, ConnectSQLDatabase):
    classroom_table = {}

    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor()

    def check_classroom_table(self, employee_id):
        try:
            print("Checking for your classrooms... \n")

            check_query = """SELECT * FROM classrooms WHERE TeacherID = %s"""
            id_val = int(employee_id)
            self.db_cursor.execute(check_query, (id_val,))
            res = self.db_cursor.fetchall()

            return res

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                return True
            else:
                return False
            
        except Exception as err:
            print("BRUH")

    def create_classroom(self, class_name, teacher_id, yr):
        try:
            create_query = """INSERT INTO classrooms(TeacherID, CourseName, Grade) VALUES (%s, %s, %s)"""
            vals = teacher_id, class_name, yr
            self.db_cursor.execute(create_query, vals)
            self.sql_serv.commit()
            
        except Exception as err:
            print("WHAT")
    
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
            info = {
                "Username: ": username,
                "Email: ": email,
                "Password: ": password
            }

            register_query = """INSERT INTO teachers(FirstName, LastName, UserName, EmailAddress, Password) 
                                VALUES (%s, %s, %s, %s, %s)"""
            register_val = (fname, lname, username, email, password)

            check_individual = """SELECT * FROM teachers WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            res = self.db_cursor.fetchone()

            print("\n\n** Please save this information if needed. **")
            for k, v in info.items():
                print(f"{k} {v}")
            print("\n\n")

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
            info = {
                "Username: ": username,
                "Email: ": email,
                "Password: ": password
            }

            register_query = """INSERT INTO students(FirstName, LastName, UserName, EmailAddress, Password) 
                                VALUES (%s, %s, %s, %s, %s)"""
            register_val = (fname, lname, username, email, password)

            check_individual = """SELECT * FROM students WHERE UserName = %s"""
            individual_val = str(username)

            self.db_cursor.execute(check_individual, (individual_val,))
            res = self.db_cursor.fetchone()

            print("\n\n** Please save this information if needed. **")
            for k, v in info.items():
                print(f"{k} {v}")
            print("\n\n")

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
        pass

def main():
    pass

if __name__ == "__main__":
    main()