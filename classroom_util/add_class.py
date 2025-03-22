import sqldb

class AddClassroom:
    def __init__(self, teacher_id):
        self.__teacher_id = teacher_id
        #self.class_id = class_id

    def create_class(self):
        while True:
            try:
                reg_classrooms = sqldb.RegisterClassrooms()
                user_op = sqldb.UserOperations()
                db_op = sqldb.DBOperations()

                class_name = input("Enter the course name: ")
                yr_input = input("Enter the year/grade: ")

                reg_classrooms.create_classroom(class_name, self.__teacher_id, yr_input)
                class_id = db_op.get_classroom_id(class_name, self.__teacher_id)
                user_op.assign_teacher(self.__teacher_id, class_id)
                break

            except Exception as err:
                print("-- Add Classroom Error!")
                print(err)
                return False

