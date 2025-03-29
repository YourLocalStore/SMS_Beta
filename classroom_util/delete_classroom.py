import sqldb

class DeleteCourse:
    """ The class where teachers and administrators can remove existing classrooms from the classrooms table in the database.

    Attributes:
        course_name (str): The classroom name.
        class_id (str): The classroom ID.
        section (str): The section of the classroom.
        db_op (obj): The instantiation of the DBOperations() class in sqldb.py

    Methods:
        __init__(self):
            The constructor for the attributes (course name, class ID, section, db_op)

        def delete_course(self):
            The method attempts to obtain all of the class names and IDs, of which are used to update the course
            sections after deleting the classroom. Once that is done, the method makes sure to delete any relations based
            in other tables.

            These "relations" being in junction tables (i.e. student_classroom), and updates it accordingly by deleting 
            the related information (student ID and class ID).
    """

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

        update_mode_query_off = """SET SQL_SAFE_UPDATES = 0"""
        self.db_op.db_cursor.execute(update_mode_query_off)
        
        update_student_classrooms = """DELETE FROM student_classroom WHERE ClassroomID = %s"""
        self.db_op.db_cursor.execute(update_student_classrooms, (self.class_id,))

        update_mode_query_on = """SET SQL_SAFE_UPDATES = 1"""
        self.db_op.db_cursor.execute(update_mode_query_on)

        print(f"{self.course_name} (ID: {self.class_id}) (Section: {self.section}) has been deleted.")
        self.db_op.sql_serv.commit()
        return True