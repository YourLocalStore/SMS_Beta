import sqldb

class RemoveStudents:
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

        if not remove_op or type(remove_op) == None:
            print(f"Removing Student of (ID: {self.student_id})" +
                  f" from Course of (ID: {self.class_id}) was unsuccessful. \n")
            return False
        else:
            print(f"Removing Student of (ID: {self.student_id})" +
                  f" from Course of (ID: {self.class_id}) was successful! \n")
            return True