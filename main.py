import sqldb
import visuals.titlescreen as titlescreen
import time

from threading import Thread

class StudentInterface:
    pass

class TeacherInterface:
    pass

class AdminInterface:
    pass

class LoginInterface:
    def __init__(self):
        while True:
            try:
                print("\n -------- SMS Login Menu -------- \n")
                selection = {
                        1: "Log-in",
                        2: "Register",
                        3: "Exit"
                    }

                for k,v in selection.items():
                    print(f"\t{k}: {v}")

                user_selection = int(input("\nEnter a selection: "))

                if user_selection == 1:
                    LoginInterface.user_login()
                elif user_selection == 2:
                    LoginInterface.user_register()
                elif user_selection == 3:
                    break
            
            except ValueError as err:
                print("\n***************************************")
                print("An exception occurred! Have you tried entering the right values?")
                print(err)
                print("***************************************\n")
                continue

    def user_login(self):
        pass

    def user_register(self):
        pass

def connect_to_db():
    msg = "Connecting to Database"

    try:
        connection_thread = Thread(target=sqldb.try_connection)
        message_thread = Thread(target=load_msg(msg, connection_thread))

        message_thread.start()
        connection_thread.start()

        message_thread.join()
        connection_thread.join()

    except Exception as err:
        print("Please try again, or contact the developer immediately. \n")
        print(f"Error: {err}")

def load_msg(msg, loading_thread):
    while True:
        for j in range(4):
            dot_amount = "." * j
            print(f"{msg}{dot_amount}", end='\r')
            time.sleep(0.25)

        print(f"{msg}     ", end='\r')

        if not Thread.isAlive(loading_thread):
            break
        
        return False

def main():
    while True:
        try:
            print(titlescreen.title)
            selection = {
                1: "Enter",
                2: "Exit"
            }


            for k,v in selection.items():
                print(f"{k}: {v}")

            user_selection = int(input("\nEnter a selection: "))

            if user_selection == 1:
                login = LoginInterface()
            elif user_selection == 2:
                break
            
        except ValueError as err:
            print("\n***************************************")
            print("An exception occurred! Have you tried entering the right values?")
            print(err)
            print("***************************************\n")
            continue

    return False

if __name__ == "__main__":
    print("\nWelcome to the Student Management System (SMS)!")
    time.sleep(1.5)

    print("Please wait while we load the database... \n")
    time.sleep(1.5)

    connect_to_db()
    main()
