import sqldb

class DeleteCourse:
    def __init__(self, course_name, class_id, section):
        self.course_name = course_name
        self.class_id = class_id
        self.section = section
        self.db_op = sqldb.DBOperations()

    def delete_course(self):
        self.db_op.delete_class(
            self.course_name, self.class_id,
            self.section
        )

        get_all_courses = """SELECT * FROM classrooms"""
        self.db_op.db_cursor.execute(get_all_courses)
        class_names = [name[3] for name in self.db_op.db_cursor.fetchall()]

        get_all_ids = """SELECT * FROM classrooms"""
        self.db_op.db_cursor.execute(get_all_ids)
        class_ids = [ids[0] for ids in self.db_op.db_cursor.fetchall()]

        section_lst = []
        counter = {}

        for courses in class_names:
            counter[courses] = counter.get(courses, 0) + 1
            section_lst.append(counter[courses])
        
        update_course_sections = """UPDATE classrooms
                                    SET Section = %s
                                    WHERE ClassroomID = %s"""
        
        for i in range(len(class_names)):
            course_vals = section_lst[i], class_ids[i]
            self.db_op.db_cursor.execute(update_course_sections, course_vals)

        print(f"{self.course_name} (ID: {self.class_id}) (Section: {self.section}) has been deleted.")
        self.db_op.sql_serv.commit()
        return True