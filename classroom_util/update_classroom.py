import sqldb

class UpdateClass:
    def __init__(self, class_id, teacher_id, grade, course_name, section):
        self._class_id = class_id
        self.__teacher_id = teacher_id
        self.grade = grade
        self.course_name = course_name
        self.section = section
        self.db_op = sqldb.DBOperations()
        self.user_op = sqldb.UserOperations()

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
        try:
            print("\nUpdating teacher ID...")
        
            class_update_query = """UPDATE classrooms
                                    SET TeacherID = %s
                                    WHERE ClassroomID = %s"""
            vals = new_teacher_id, self._class_id
            self.db_op.db_cursor.execute(class_update_query, vals)

            teacher_class_delete_query = """DELETE FROM teacher_classroom
                                            WHERE ClassroomID = %s"""
            vals = self._class_id
            self.db_op.db_cursor.execute(teacher_class_delete_query, (vals,))

            teacher_class_insert_query = """INSERT INTO teacher_classroom(TeacherID, ClassroomID)
                                            VALUES(%s, %s)"""
            vals = new_teacher_id, self._class_id
            self.db_op.db_cursor.execute(teacher_class_insert_query, vals)
            
            print(f"Teacher ID updated for class of ID: {self._class_id}")
            print(f"New ID: {new_teacher_id}")
            self.db_op.sql_serv.commit()
            return True
        except Exception:
            print("-- Updating Teacher ID Error")
            print("Are you sure that this teacher exists?")
            return False
    
    def update_course_year(self, new_course_year):
        print("\nUpdating course year...")

        grade_update_query = """UPDATE classrooms
                                SET Grade = %s
                                WHERE ClassroomID = %s"""
        vals = new_course_year, self._class_id
        self.db_op.db_cursor.execute(grade_update_query, vals)
        
        print(f"Course Year updated for class of ID: {self._class_id}")
        print(f"New Course Year: {new_course_year}")
        self.db_op.sql_serv.commit()
        return True
    
    def update_course_name(self, new_course_name):
        section_lst = []
        counter = {}

        print("\nUpdating course name...")

        course_name_query = """SELECT CourseName FROM classrooms
                               WHERE CourseName = %s"""
        course_name_val = new_course_name
        self.db_op.db_cursor.execute(course_name_query, (course_name_val,))

        course_name_query = """UPDATE classrooms
                                SET CourseName = %s
                                WHERE ClassroomID = %s"""
        course_vals = new_course_name, self._class_id
        self.db_op.db_cursor.execute(course_name_query, course_vals)

        get_all_courses = """SELECT * FROM classrooms"""
        self.db_op.db_cursor.execute(get_all_courses)
        class_names = [name[3] for name in self.db_op.db_cursor.fetchall()]

        get_all_ids = """SELECT * FROM classrooms"""
        self.db_op.db_cursor.execute(get_all_ids)
        class_ids = [ids[0] for ids in self.db_op.db_cursor.fetchall()]

        for courses in class_names:
            counter[courses] = counter.get(courses, 0) + 1
            section_lst.append(counter[courses])

        update_course_sections = """UPDATE classrooms
                                    SET Section = %s
                                    WHERE ClassroomID = %s"""
        
        for i in range(len(class_names)):
            course_vals = section_lst[i], class_ids[i]
            self.db_op.db_cursor.execute(update_course_sections, course_vals)

        print(f"Classroom of ID: {self._class_id} has been updated to {new_course_name}.")
        self.db_op.sql_serv.commit()
