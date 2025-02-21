import mysql.connector
import os

from dotenv import load_dotenv
from mysql import *
from mysql.connector import errorcode
from passlib.hash import pbkdf2_sha256

load_dotenv()

class ConnectSQLDatabase:
    db_name = "tester"

    def __init__(self):
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
            self.db_cursor.execute(
                f"USE {self.db_name}"
            )

            self.db_cursor.close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Connection failed due to password/username. \n")

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Attempting to create database {self.db_name}...")
                ConnectSQLDatabase.create_db(self, self.db_cursor)

    def create_db(self, cursor):
        try:
            cursor.execute(
                f"CREATE DATABASE {self.db_name}"
            )
            print(f"Database: {self.db_name} has been created. \n")

        except mysql.connector.Error as err:
            print("Could not create the database. \n")

    def get_db_cursor(self):
        return self.sql_serv.cursor()
    
class DBOperations(ConnectSQLDatabase):
    def __init__(self):
        super().__init__()
                   
    def show_students(self):
        pass

    def add_row(self):
        pass

    def delete_row(self):
        pass

    def close_serv_connection(self):
        if self.sql_serv.is_connected:
            self.sql_serv.close()
            return "Closing connection..."
    
    def close_cursor_connection(self):
        return self.db_cursor.close()
    
class RegisterPerson(ConnectSQLDatabase):
    user_table = {}

    def __init__(self, fname, lname, username, email, password):
        super().__init__()
        
        self.__fname = fname
        self.__lname = lname
        self.__email = email
        self.username = username
        self.__password = password

        self.db_cursor = self.sql_serv.cursor()

    def register_table(self):
        try:
            print("Creating table... ")

            self.user_table["Users"] = self.db_cursor.execute(
                """CREATE TABLE users( 
                ID int NOT NULL AUTO_INCREMENT, 
                FirstName varchar(255) not NULL, 
                LastName varchar(255) not NULL, 
                UserName varchar(255) not NULL, 
                EmailAddress varchar(255) not NULL, 
                Password varchar(64) not NULL, 
                PRIMARY KEY(ID))"""
            )

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                return "User table exists."
            else:
                print(err)

    def get_uid(self):
        user_id = self.db_cursor.execute(
            f"SELECT FROM users WHERE UserName = {self.username}"
        )

        user_id = self.db_cursor.fetchone()
        return user_id

    def register_user(self, fname, lname, username, email, password):
        try:
            # self.db_cursor.execute("TRUNCATE TABLE users")
            # self.sql_serv.commit()

            register_query = """INSERT INTO users(FirstName, LastName, UserName, EmailAddress, Password) 
                        VALUES (%s, %s, %s, %s, %s)"""
            register_val = (fname, lname, username, email, password)

            check_individual = """SELECT * FROM users WHERE UserName = %s"""
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
    def __init__(self):
        super().__init__()

    def return_status(self):
        if self.sql_serv.is_connected:
            return ("Connection to database successful!")
        else:
            return ("Connection to database unsuccessful.")
    
    def check_dbs(self):
        self.db_cursor = self.sql_serv.cursor()
        self.db_cursor.execute("SHOW DATABASES")

        databases = self.db_cursor.fetchall()

        return f"Current Databases in '{self.db_name}': " + \
               f"{', '.join(map(str, [i[0] for i in databases]))}"
    
def try_connection():
    connect_db = ConnectSQLDatabase()
    db_status = CheckDBState()
    print(db_status.return_status())

def main():
    pass
    # connect_db = ConnectSQLDatabase()
    # db_status = CheckDBState()
    # print(db_status.return_status())

    # # print(db_status.check_dbs())

    # register = RegisterPerson(fname = "", lname = "", username = "", email = "", password = "")
    # print(register.register_table())

    # register.register_user("John", "Doe", "johndoe123", "johndoe123@gmail.com", "1234567890")

if __name__ == "__main__":
    main()