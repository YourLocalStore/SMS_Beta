import sqldb

class AddStudent:
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

