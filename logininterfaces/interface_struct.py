import datetime

from abc import ABC, abstractmethod
from main import LoginInterface
from sqldb import UserOperations

class Interface(ABC, LoginInterface):
    """ A class that mainly gets/sets any of the user's credentials within the class. This is usually an inherited class 
        within interfacing.py.

    Attributes:
      fname (str): The first name of the user.
      lname (str): The last name of the user.
      email (str): The email address of the user.
      username (str): The username of the user.
      password (str): The password of the user.
      teacher_id (str): If the user is a teacher, then they use a teacher ID.
      administrator_id (str): If the user is an administrator, then they use an administrator ID.
      date_today (str): Gets today's date.

    Methods:
        __init__(self):
            The constructor that initializes much of the user's information.

        def get_fname(self):
            A getter method for the user's first name.

        def set_fname(self, new_fname):
            A setter method for the user's first name.

        def get_lname(self):
            A getter method for the user's last name.

        def set_lname(self, new_lname):
            A setter method for the user's last name.
        
        def get_username(self):
            A getter method for the user's username.

        def set_username(self, new_username):
            A setter method for the user's username

        def get_email(self): 
            A getter method for the user's email address.

        def set_email(self, new_email):
            A setter method for the user's email address.
        
        def get_password(self):
            A getter method for the user's password. 

        def set_password(self, new_password):
            A setter method for the user's password
        
        def get_teacher_id(self):
            A getter method for the user's teacher ID.

        def get_admin_id(self):
            A getter method for the user's admin ID.

        def get_table(self, teacher_id, classroom_name, class_id):
            A getter method for the classroom information within the teacher/admin view.

        def get_students_table(self, teacher_id, classroom_name, class_id):
            A getter method for the classroom information within the student view.

        def account_information(self):
            An abstract method for methods to implement a way to get user information.

        def class_details(self):
            An abstract method for methods to implement a way to get course details.

        def student_details(self):
            An abstract method for methods to implement a way to get details about a student.
        
    """

    def __init__(self, fname, lname, username, email, password, teacher_id, administrator_id):
        super().__init__(fname, lname, username, email, password, teacher_id, administrator_id)
        self.date_today = datetime.datetime.now()

    def get_fname(self):
        return self._LoginInterface__fname
    
    def set_fname(self, new_fname):
        self._LoginInterface__fname = new_fname
        return self._LoginInterface__fname

    def get_lname(self):
        return self._LoginInterface__lname
    
    def set_lname(self, new_lname):
        self._LoginInterface__lname = new_lname
        return self._LoginInterface__lname
    
    def get_username(self):
        return self.username
    
    def set_username(self, new_username):
        self.username = new_username
        return self.username
    
    def get_email(self):
        return self._LoginInterface__email
    
    def set_email(self, new_email):
        self._LoginInterface__email = new_email
        return self._LoginInterface__email
    
    def get_password(self):
        return self._LoginInterface__password
    
    def set_password(self, new_password):
        self._LoginInterface__password = new_password
        return self._LoginInterface__password
    
    def get_teacher_id(self):
        return self._LoginInterface__teacher_id
    
    def get_admin_id(self):
        return self._LoginInterface__administrator_id
    
    def get_table(self, teacher_id, classroom_name, class_id):
        table_op = UserOperations()
        return table_op.teacher_show_students(teacher_id, classroom_name, class_id) 
    
    def get_students_table(self, teacher_id, classroom_name, class_id):
        table_op = UserOperations()
        return table_op.students_show_students(teacher_id, classroom_name, class_id) 

    @abstractmethod
    def account_information(self):
        pass

    @abstractmethod
    def class_details(self):
        pass

    @abstractmethod
    def student_details(self):
        pass