import pathlib
import sqldb
import time

class DownloadClass:
    def __init__(self, teacher_id, class_name):
        self.teacher_id = teacher_id
        self.class_name = class_name
     
    def download_file(self):
        DOWNLOAD_DIRECTORY = pathlib.Path.home()/'Downloads'
        save_file = input("Enter a file name: ")
        file_op = sqldb.UserOperations()

        with open(f"{DOWNLOAD_DIRECTORY}\\{save_file}.txt", "w", encoding="utf-8") as userfile:
            print("Clearing any data before handling...")
            userfile.write("")
        
        with open(f"{DOWNLOAD_DIRECTORY}\\{save_file}.txt", "w", encoding="utf-8") as userfile:
            userfile.write(str(file_op.show_students(self.teacher_id, self.class_name)))

            print(f"Writing to {pathlib.Path.home()/'Downloads'}...")
            time.sleep(1)
            print("Write to file successful. \n")
            time.sleep(1)

        return True
        