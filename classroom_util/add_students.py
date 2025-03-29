import sqldb

class AddStudent:
    """ The class where teachers are able to add students into their own classrooms. 

    Attributes:
        student_id (str): The student's ID.
        class_id (str): The classroom ID.

    Methods:
        __init__(self):
            The constructor for the attributes (student/class ID).

        def add_person(self):
            This method assigns a student to an existing classroom, based on the UserOperations() class in
            sqldb.py.
    """

    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    def add_person(self):
        add_op = sqldb.UserOperations()
        res = add_op.add_student(self.student_id, self.class_id)

        if not res or type(res) == None:
            print(f"Adding Student of (ID: {self.student_id})" +
                    f" to Course of (ID: {self.class_id}) was unsuccessful. \n")
        elif res:
            print(f"Adding Student of (ID: {self.student_id})" +
                    f" to Course of (ID: {self.class_id}) was successful! \n")
        return

