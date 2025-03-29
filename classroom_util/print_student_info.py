class PrintInformation:
    """ The class where teachers/administrators are able to view student information and print them out.

    Attributes:
        student_info (tuple): All of the information about the student, typically a tuple

    Methods:
        __init__(self):
            The constructor for the attributes (student/class ID).

        def print_student(self):
            Gets all of the student information and prints them out line by line, given 
            the fields.
    """

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