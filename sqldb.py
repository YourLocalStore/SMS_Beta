import mysql.connector
import time
import configparser

#from dotenv import load_dotenv
from mysql import *
from mysql.connector import errorcode
from prettytable import PrettyTable, from_db_cursor
from abc import ABC, abstractmethod
from threading import Thread

class ConnectSQLDatabase:
    db_name = "tester"
    config = configparser.ConfigParser()

    def __init__(self):
        try:
            self.config.read_file(open("Credential-Configuration.ini"))

            """
            ** Note that the host, port, user, and password must be configured to the database credentials.
               To change these credentials, locate 'Credential-Configuration.ini'.
            """

            self.sql_serv = mysql.connector.connect(
                charset = "utf8",
                use_unicode = True,
                host = self.config["Credentials"]["Host"],
                port = self.config["Credentials"]["Port"],
                user = self.config["Credentials"]["User"],
                password = self.config["Credentials"]["Password"],
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

    def get_all_classrooms(self):
        try:
            print("\nViewing all clasrooms...")
            classroom_table = PrettyTable()

            classroom_row_query = """SELECT * FROM classrooms"""
            self.db_cursor.execute(classroom_row_query)
            
            classroom_table = from_db_cursor(self.db_cursor)
            print(f"{classroom_table}\n")

        except Exception as err:
            print("\n-- Something went wrong gathering all classrooms!")
            print(err)
            return None

    # This is only for main.py's login/register screen.
    def get_user_info(self, table_name, username):
        table_list = ["teachers", "students", "administrators"]

        if table_name not in table_list:
            print(f"\n{table_name} does not exist.")
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
            
    def get_classroom_from_id(self, cid):
        try:
            row_query = f"""SELECT * FROM classrooms WHERE ClassroomID = %s"""
            id_val = cid

            self.db_cursor.execute(row_query, (id_val,))
            fetch_query = self.db_cursor.fetchone()

            if len(fetch_query) > 0:
                return fetch_query
            else:
                print(f"The coruse with ID: {cid} does not exist in the records! \n")
                return None
        
        except Exception as err:
            print(err)
            return None

    # This method is called when updating information.
    def get_student_from_id(self, uid):
        try:
            row_query = f"""SELECT * FROM students WHERE StudentID = %s"""
            id_val = uid

            self.db_cursor.execute(row_query, (id_val,))
            fetch_query = self.db_cursor.fetchone()

            if len(fetch_query) > 0:
                return fetch_query
            else:
                print(f"The student with ID: {uid} does not exist in the records! \n")
                return None
        
        except Exception as err:
            print(err)
            return None
        
    def get_teacher_from_id(self, uid):
        try:
            row_query = f"""SELECT * FROM teachers WHERE TeacherID = %s"""
            id_val = uid

            self.db_cursor.execute(row_query, (id_val,))
            fetch_query = self.db_cursor.fetchone()

            if len(fetch_query) > 0:
                return fetch_query
            else:
                print(f"The teacher with ID: {uid} does not exist in the records! \n")
                return None
        
        except Exception as err:
            print(err)
            return None

    def get_student_classnames(self, student_id):
        try:
            class_lst = []

            student_class_id = """SELECT ClassroomID FROM student_classroom WHERE StudentID = %s"""
            student_id_val = student_id

            self.db_cursor.execute(student_class_id, (student_id_val,))
            class_ids = self.db_cursor.fetchall()

            for i in range(len(class_ids)):
                student_class_names = """SELECT CourseName FROM Classrooms WHERE ClassroomID = %s"""
                class_id_val = class_ids[i]

                self.db_cursor.execute(student_class_names, (class_id_val))
                class_names = self.db_cursor.fetchall()

                class_lst.append(class_names)

            return class_lst
        
        except Exception:
            pass

    def get_student_class_id(self, student_id, class_name):
        try:
            student_class_id = """SELECT ClassroomID FROM student_classroom WHERE StudentID = %s"""
            student_id_val = student_id

            self.db_cursor.execute(student_class_id, (student_id_val,))
            class_ids = self.db_cursor.fetchall()

            for i in range(len(class_ids)):
                name_query = """SELECT CourseName FROM Classrooms WHERE ClassroomID = %s"""
                class_id_val = class_ids[i]

                self.db_cursor.execute(name_query, (class_id_val))
                class_names = self.db_cursor.fetchall()

                if class_name in class_names[0]:
                    return class_id_val[0]
                break

            else:
                return None
            
        except Exception as err:
            print("-- Searching for ClassroomID Error")
            print(err)
    
    def get_class_teacher_id(self, student_id, class_name):
        try:
            correct_cls_id = ""
            class_id_query = """SELECT ClassroomID FROM student_classroom WHERE StudentID = %s"""
            student_id_val = student_id

            self.db_cursor.execute(class_id_query, (student_id_val,))
            class_ids = self.db_cursor.fetchall()

            for i in range(len(class_ids)):
                course_name_query = """SELECT CourseName FROM Classrooms WHERE ClassroomID = %s"""
                class_id_vals = class_ids[i][0]

                self.db_cursor.execute(course_name_query, (class_id_vals,))
                course = self.db_cursor.fetchone()

                if course[0] == class_name:
                    class_name = course[0]
                    correct_cls_id = class_id_vals
                    break

            teacher_id_query = """SELECT TeacherID FROM Classrooms WHERE ClassroomID = %s AND CourseName = %s"""
            correct_cls_id_val = correct_cls_id
            course_name_val = class_name

            self.db_cursor.execute(teacher_id_query, (correct_cls_id_val, course_name_val,))
            teacher_id = self.db_cursor.fetchone()
            return teacher_id[0]

        except Exception as err:
            print("\n-- Teacher ID Error")
            print(err)
    
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
        
    # Teacher Method
    def get_classroom_id(self, course, teacher_id, section):
        try:
            id_query = """SELECT ClassroomID FROM classrooms WHERE CourseName = %s AND TeacherID = %s AND Section = %s"""
            self.db_cursor.execute(id_query, (course, teacher_id, section,))

            fetch_query = self.db_cursor.fetchone()
            return fetch_query[0]

        except Exception:
            return None 
        
    def get_classroom_name(self, classroom_id):
        try:
            classroom_name_query = """SELECT CourseName FROM Classrooms WHERE ClassroomID = %s"""
            class_id_val = classroom_id

            self.db_cursor.execute(classroom_name_query, (class_id_val,))
            class_name = self.db_cursor.fetchone()
            return class_name
        
        except Exception as err:
            print("-- Classroom Name Error")
            print(err)

    def delete_class(self, course_name, class_id, section):
        try:
            course_query = """DELETE FROM classrooms WHERE CourseName = %s AND ClassroomID = %s AND Section = %s"""
            course_vals = course_name, class_id, section
            self.db_cursor.execute(course_query, course_vals)
            self.sql_serv.commit()
            return True
        
        except Exception as err:
            print("\n-- Class Deletion Error")
            print(err)
            return False
        
    def delete_all_classes(self, teacher_id):
        try:
            course_id_query = """SELECT ClassroomID FROM classrooms WHERE TeacherID = %s"""
            teacher_val = teacher_id

            self.db_cursor.execute(course_id_query, (teacher_val,))
            get_ids = self.db_cursor.fetchall()

            for i in range(len(get_ids)):

                course_query = """DELETE FROM classrooms WHERE ClassroomID = %s"""
                class_ids = get_ids[i][0]
                self.db_cursor.execute(course_query, (class_ids,))

                update_mode_query_off = """SET SQL_SAFE_UPDATES = 0"""
                self.db_op.db_cursor.execute(update_mode_query_off)
        
                update_student_classrooms = """DELETE FROM student_classroom WHERE ClassroomID = %s"""
                self.db_op.db_cursor.execute(update_student_classrooms, (class_ids,))

                update_mode_query_on = """SET SQL_SAFE_UPDATES = 1"""
                self.db_op.db_cursor.execute(update_mode_query_on)

            self.sql_serv.commit()
            return True
        
        except Exception as err:
            print("\n-- Class Deletion Error")
            print(err)
            return False

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

class UserOperations(DBOperations, ConnectSQLDatabase):
    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def teacher_show_students(self, teacher_id, classroom_name, class_id):
        try:
            table_header = PrettyTable()
            table_header.field_names = [classroom_name]

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
            WHERE teachers.TeacherID = %s AND classrooms.CourseName = %s AND classrooms.ClassroomID = %s;
            """

            self.db_cursor.execute(show_query, (teacher_id, classroom_name, class_id))
            student_table = from_db_cursor(self.db_cursor)
            query_res = self.db_cursor.fetchall()

            if query_res:
                print(f"\n\n{table_header}")
                print(f"\n{student_table}\n")
                return True
            else:
                print(f"\n\n{table_header}")
                print(f"\n{student_table}")
                return False

        except Exception as err:
            print("Unfortunately, trying to view the student table went wrong!")
            print(err)

        finally:
            return str(student_table)
        
    def students_show_students(self, teacher_id, classroom_name, class_id):
        try:
            table_header = PrettyTable()
            table_header.field_names = [classroom_name]

            student_table = PrettyTable()

            show_query = """ 
            SELECT students.FirstName AS STUDENT_FIRST_NAME,
                   students.LastName AS STUDENT_LAST_NAME,
                   classrooms.ClassroomID AS CLASSROOM_ID
            FROM students
            INNER JOIN student_classroom ON students.StudentID = student_classroom.StudentID
            INNER JOIN classrooms ON student_classroom.ClassroomID = classrooms.ClassroomID
            INNER JOIN teacher_classroom ON classrooms.ClassroomID = teacher_classroom.ClassroomID
            INNER JOIN teachers ON teacher_classroom.TeacherID = teachers.TeacherID
            WHERE teachers.TeacherID = %s AND classrooms.CourseName = %s AND classrooms.ClassroomID = %s;
            """

            self.db_cursor.execute(show_query, (teacher_id, classroom_name, class_id))
            student_table = from_db_cursor(self.db_cursor)
            query_res = self.db_cursor.fetchall()

            if query_res:
                print(f"\n\n{table_header}")
                print(f"\n{student_table}\n")
                return True
            else:
                print(f"\n\n{table_header}")
                print(f"\n{student_table}\n")
                return False

        except Exception as err:
            print("Unfortunately, trying to view the student table went wrong!")
            print(err)

        finally:
            return str(student_table)
    
    def show_all_students(self):
        try:
            print("\nViewing all students...")
            student_table = PrettyTable()

            show_all_query = """SELECT * FROM students"""
            self.db_cursor.execute(show_all_query)

            student_table = from_db_cursor(self.db_cursor)
            print(f"\n{student_table}\n")

        except Exception as err:
            print("\n- Something went wrong gathering all students!")
            print(err)
            return None
        
    def show_all_teachers(self):
        try:
            print("\nViewing all teachers...")
            teacher_table = PrettyTable()

            show_all_query = """SELECT * FROM teachers"""
            self.db_cursor.execute(show_all_query)

            teacher_table = from_db_cursor(self.db_cursor)
            print(f"\n{teacher_table}\n")
            
        except Exception as err:
            print("\n-- Something went wrong gathering all students!")
            print(err)
            return None
        
    def add_student(self, student_id, class_id):
        try:
            exists = DBOperations()
            student_exists = exists.student_id_exists(student_id)
            student_classes = []

            if type(student_exists) == None:
                print("Student does not exist... \n")

            if student_exists:
                class_id_query = """SELECT ClassroomID FROM student_classroom WHERE StudentID = %s"""
                self.db_cursor.execute(class_id_query, (student_id,))
                class_ids = self.db_cursor.fetchall()
                
                if len(class_ids) > 0 or type(class_ids) != None:
                    for i in range(len(class_ids)):
                        if class_id in class_ids[0]:
                            print("This user is already in your class! \n")
                            return None
                        
                    for i in range(len(class_ids)):
                        class_name_query = """SELECT CourseName FROM Classrooms WHERE ClassroomID = %s"""
                        self.db_cursor.execute(class_name_query, (class_ids[i][0],))
                        names = self.db_cursor.fetchone()
                        student_classes.append(names[0])

                    class_name_query = """SELECT CourseName FROM Classrooms WHERE ClassroomID = %s"""
                    self.db_cursor.execute(class_name_query, (class_id,))
                    current_class_name = self.db_cursor.fetchone()[0]

                    if current_class_name in student_classes:
                        print("\n==== This student is already registered for the same class! ====")
                        return None
                
                insert_query = """INSERT INTO student_classroom(StudentID, ClassroomID) VALUES(%s, %s)"""
                self.db_cursor.execute(insert_query, (student_id, class_id,))
                self.sql_serv.commit()
                return True
            
            else:
                print('womp')
                return False

        except Exception as err:
            print("\n-- Adding Student Error")
            print("Something went wrong trying to add students!")
            print("Are you sure that the student and/or class IDs exist?")
            print(err)
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

    def remove_student_record(self, student_id):
        try:
            remove_query = """
            DELETE FROM students WHERE StudentID = %s
            """
            student_id_val = student_id

            self.db_cursor.execute(remove_query, (student_id_val,))
            self.sql_serv.commit()
            return True
        
        except Exception as err:
            print("-- Record Removal Error")
            print(err)

    def remove_teacher_record(self, teacher_id):
        try:
            remove_query = """
            DELETE FROM teachers WHERE TeacherID = %s
            """
            teacher_id_val = teacher_id

            self.db_cursor.execute(remove_query, (teacher_id_val,))
            print(f"Removed teacher of (ID: {teacher_id}). \n")
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

            print(f"Teacher of (ID: {teacher_id}) successfully assigned to classroom of (ID: {class_id}).\n")
            return True

        except Exception as err:
            print("\n-- Assign Teacher Error")
            print(err)

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
            
        except Exception:
            return False

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
              
        except Exception:
            return False

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
            
        except Exception:
            return False

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
              
        except Exception:
            return False

class AdminLoginCheck(ConnectSQLDatabase, LoginCheck):
    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor(buffered=True)

    def login_user_exists(self, username, employee_id):
        try:
            check_individual = """SELECT * FROM `administrators` WHERE UserName = %s"""
            check_id = """SELECT * FROM `administrators` WHERE AdministratorID = %s"""
            
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
            
        except Exception:
            return False

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
              
        except Exception:
            return False

class CreateRegisterTables(ConnectSQLDatabase):
    user_table = {}

    def __init__(self):
        super().__init__()
        self.db_cursor = self.sql_serv.cursor()

    def student_register_table(self):
        try:
            print("Checking for Student Table...")
            #time.sleep(1.5)

            self.user_table["Students"] = self.db_cursor.execute(
                """CREATE TABLE `students`( 
                StudentID int NOT NULL AUTO_INCREMENT, 
                FirstName varchar(255) not NULL, 
                LastName varchar(255) not NULL, 
                UserName varchar(20) not NULL UNIQUE, 
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
            print("Checking for Teacher Table...")
            #time.sleep(1.5)

            self.user_table["Teachers"] = self.db_cursor.execute(
                """CREATE TABLE teachers( 
                TeacherID int NOT NULL AUTO_INCREMENT, 
                FirstName varchar(255) not NULL, 
                LastName varchar(255) not NULL, 
                UserName varchar(255) not NULL UNIQUE, 
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
        
    def administrator_register_table(self):
        try:
            print("Checking for Administrator Table...")
            #time.sleep(1.5)

            self.user_table["Administrators"] = self.db_cursor.execute(
                """CREATE TABLE administrators( 
                AdministratorID int NOT NULL, 
                FirstName varchar(255) not NULL, 
                LastName varchar(255) not NULL, 
                UserName varchar(255) not NULL UNIQUE, 
                EmailAddress varchar(255) not NULL, 
                Password varchar(64) not NULL, 
                PRIMARY KEY(AdministratorID))"""
            )

            # Probably fine to just have the admin credentials here...
            admin_query = """INSERT INTO administrators(AdministratorID, FirstName,
                                                        LastName, UserName, EmailAddress,
                                                        Password)
                             VALUES(%s, %s, %s, %s, %s, %s)"""
            admin_vals = (
                "727", "root", 
                "user", "rootadministrator", 
                "root@yourlocalstore.com", "!_INFR2025_$$$$$$"
            )
            self.db_cursor.execute(admin_query, admin_vals)
            self.sql_serv.commit()
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Administrator table exists.\n")
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
                Section int NOT NULL DEFAULT 1,
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
                    ON DELETE CASCADE)
                """
            )

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
                    ON DELETE CASCADE)
                """
            )

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
            count_query = """SELECT COUNT(*) as Section_Count
                             FROM Classrooms
                             WHERE CourseName = %s"""
            self.db_cursor.execute(count_query, (class_name,))
            count_greater_than_zero = self.db_cursor.fetchone()[0] > 0 # Check the count

            if count_greater_than_zero:
                max_section_query = """SELECT MAX(Section) FROM Classrooms WHERE CourseName = %s"""
                self.db_cursor.execute(max_section_query, (class_name,))
                max_section = self.db_cursor.fetchone()[0]
                new_section = max_section + 1
            else:
                new_section = 1 # default section is 1

            create_query = """INSERT INTO classrooms(TeacherID, CourseName, Grade, Section) 
                              VALUES (%s, %s, %s, %s)"""
            vals = teacher_id, class_name, yr, new_section
            self.db_cursor.execute(create_query, vals)

            self.sql_serv.commit()
            return new_section
            
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
        id_query = """SELECT TeacherID FROM students WHERE UserName = %s"""
        self.db_cursor.execute(id_query, (self.username,))

        student_user_id = self.db_cursor.fetchone()
        return student_user_id
    
    def get_teacher_uid(self):
        id_query = """SELECT TeacherID FROM teachers WHERE UserName = %s"""
        self.db_cursor.execute(id_query, (self.username,))

        teacher_user_id = self.db_cursor.fetchone()
        print(teacher_user_id)
        return teacher_user_id

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

                teacher_id = self.get_teacher_uid()[0]

                info = {
                    "Username: ": username,
                    "Email: ": email,
                    "Password: ": password,
                    "Teacher ID (IMPORTANT): ": teacher_id
                }

                print("\n\n** Please save this information if needed. **")
                for k, v in info.items():
                    print(f"{k} {v}")
                print("\n")

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
        obj = ConnectSQLDatabase()
        pass
