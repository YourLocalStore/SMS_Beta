import pathlib
import sqldb
import time

from prettytable import PrettyTable

class DownloadClass:
    def __init__(self, teacher_id, class_name, class_id):
        self.teacher_id = teacher_id
        self.class_name = class_name
        self.class_id = class_id
     
    def download_file(self):
        DOWNLOAD_DIRECTORY = pathlib.Path.home()/'Downloads'
        save_file = input("Enter a file name: ")
        file_op = sqldb.UserOperations()

        class_header = PrettyTable()
        class_header.field_names = [self.class_name]

        with open(
            f"{DOWNLOAD_DIRECTORY}\\{save_file}.txt", "w", encoding="utf-8"
        ) as userfile:
            print("Clearing any data before handling...")
            userfile.write("")
        
        with open(
            f"{DOWNLOAD_DIRECTORY}\\{save_file}.txt", "w", encoding="utf-8"
        ) as userfile:
            userfile.write(f"{str(class_header)}\n")
            userfile.write(
                str(file_op.teacher_show_students(self.teacher_id, self.class_name, self.class_id))
            )

            print(f"Writing to {pathlib.Path.home()/'Downloads'}...")
            time.sleep(1)
            print("Write to file successful. \n")
            time.sleep(1)

        return True
        