import sqldb

class UpdateClass:
    def __init__(self, class_id, teacher_id, grade, course_name, section):
        self._class_id = class_id
        self.__teacher_id = teacher_id
        self.grade = grade
        self.course_name = course_name
        self.section = section
        self.db_op = sqldb.DBOperations()

    def update_menu(self):
        while True:
            try:
                update_choices = {
                    1: "Change Teacher ID",
                    2: "Change Grade",
                    3: "Change Course Name",
                    4: "Go Back"
                }

                print("\n============= Credential Update Screen =============")
                print("")
                for k,v in update_choices.items():
                    print(f"\t{k}: {v}")
                
                choice = int(input("\nEnter a choice: "))

                if choice == 1:
                    new_teacher_id = input("Enter a new teacher ID: ")
                    self.update_teacher_id(new_teacher_id)
                elif choice == 2:
                    new_course_year = input("Enter a new grade: ")
                    self.update_course_year(new_course_year)
                elif choice == 3:
                    new_course_name = input("Enter a new course name: ")
                    self.update_course_name(new_course_name)
                elif choice == 4:
                    break

            except ValueError:
                print("Please enter a valid option!\n")
                continue

        return False
    
    def update_teacher_id(self, new_teacher_id):
        print("\nUpdating teacher ID...")

        class_update_query = """UPDATE classrooms
                                SET TeacherID = %s
                                WHERE ClassroomID = %s"""
        vals = new_teacher_id, self._class_id
        self.db_op.db_cursor.execute(class_update_query, vals)

        teacher_class_update_query = """UPDATE teacher_classroom
                                        SET TeacherID = %s
                                        WHERE ClassroomID = %s"""
        vals = new_teacher_id, self._class_id
        self.db_op.db_cursor.execute(teacher_class_update_query, vals)
        
        print(f"Teacher ID updated for class of ID: {self._class_id}")
        print(f"New ID: {new_teacher_id}")
        self.db_op.sql_serv.commit()
        return True
    
    def update_teacher_id(self, new_grade):
        print("\nUpdating teacher ID...")

        grade_update_query = """UPDATE classrooms
                                SET Grade = %s
                                WHERE ClassroomID = %s"""
        vals = new_grade, self._class_id
        self.db_op.db_cursor.execute(grade_update_query, vals)
        
        print(f"Course Year updated for class of ID: {self._class_id}")
        print(f"New Course Year: {new_grade}")
        self.db_op.sql_serv.commit()
        return True
    
