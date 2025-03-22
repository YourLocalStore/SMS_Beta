import sqldb

class AddStudent:
    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    def add_person(self):
        add_op = sqldb.UserOperations()

        add_op.add_student(self.student_id, self.class_id)

        if not add_op or type(add_op) == None:
            print(f"Adding Student of (ID: {self.student_id})" +
                    f" to Course of (ID: {self.class_id}) was unsuccessful. \n")
        else:
            print(f"Adding Student of (ID: {self.student_id})" +
                    f" to Course of (ID: {self.class_id}) was successful! \n")
        return

