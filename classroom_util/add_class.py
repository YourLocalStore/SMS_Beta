import sqldb

class AddClassroom:
    """ A class mainly suited for teachers that want to add classrooms to the database. 

    Attributes:
        teacher_id (str): The teacher's ID.

    Methods:
        __init__(self):
            The constructor for the attributes (teacher ID).

        def add_person(self):
            The method that asks the user was the class name and grade/year should be. Using these values, it then registers
            the classroom accordingly, along with some sort of identifier (classroom ID, section), then assigns the teacher
            who created it.
    """

    def __init__(self, teacher_id):
        self.__teacher_id = teacher_id

    def create_class(self):
        while True:
            try:
                reg_classrooms = sqldb.RegisterClassrooms()
                user_op = sqldb.UserOperations()
                db_op = sqldb.DBOperations()

                class_name = input("\nEnter the course name: ")
                yr_input = input("Enter the year/grade: ")

                register = reg_classrooms.create_classroom(class_name, self.__teacher_id, yr_input)
                class_id = db_op.get_classroom_id(class_name, self.__teacher_id, register)
                user_op.assign_teacher(self.__teacher_id, class_id)
                break

            except Exception as err:
                print("-- Add Classroom Error!")
                print(err)
                return False

