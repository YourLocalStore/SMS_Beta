import sqldb

class RemoveStudents:
    """ The class where teachers/administrators are able to remove students from specific classrooms only.

    Attributes:
        student_id (str): The ID of the student.
        class_id (str): The ID of the classroom.

    Methods:
        __init__(self):
            The constructor for the attributes (student/class ID).

        def remove_person(self):
            This method removes a student from a specific classroom. It first checks whether or not the
            student actually exists within the classroom, so we can avoid teachers from removing random
            students (who are not assigned to their specific class) off the database.
    """

    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    def remove_person(self):
        remove_op = sqldb.UserOperations()
        check_existing = remove_op.student_exists_in_class(self.student_id, self.class_id)

        if check_existing:
            pass
        else:
            print(f"The student with (ID: {self.student_id}) is not in this class! \n")
            return False

        remove_op.remove_student(self.student_id, self.class_id)

        if not check_existing or type(remove_op) == None:
            print(f"Removing Student of (ID: {self.student_id})" +
                  f" from Course of (ID: {self.class_id}) was unsuccessful. \n")
            return False
        else:
            print(f"Removing Student of (ID: {self.student_id})" +
                  f" from Course of (ID: {self.class_id}) was successful! \n")
            return True