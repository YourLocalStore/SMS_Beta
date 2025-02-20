import mysql.connector
import os
from dotenv import load_dotenv
from mysql import *
from mysql.connector import errorcode

class ConnectSQLDatabase:
    db_name = "tester"

    def __init__(self):
        self.sql_serv = mysql.connector.connect(
            charset = "utf8",
            use_unicode = True,

            host = "localhost",
            port = "3306",

            user = os.environ.get("USER"),
            password = os.environ.get("PASSWORD")
        )
        self.db_cursor = self.sql_serv.cursor()

        try:
            self.db_cursor.execute(
                    f"USE {self.db_name}"
            )

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
        self.close_cursor_connection()

        return f"Current Databases in '{self.db_name}': " + \
               f"{', '.join(map(str, [i[0] for i in databases]))}"

def main():
    connect_db = ConnectSQLDatabase()
    db_status = CheckDBState()
    print(db_status.return_status())
    print(db_status.check_dbs())

if __name__ == "__main__":
    load_dotenv()
    main()