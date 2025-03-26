class PrintInformation:
    def __init__(self, student_info):
        self.student_info = student_info

    def print_student(self):
        print("")

        for i in range(len(self.student_info)):
            fields = [
                "Student ID", "First Name", 
                "Last Name", "Username", 
                "Student Email"
            ]
            
            print(f"{fields[i]}: {self.student_info[i]}")

        input("Enter anything to continue... ")
        return True