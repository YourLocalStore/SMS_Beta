import datetime

from abc import ABC, abstractmethod
from main import LoginInterface
from sqldb import UserOperations

class Interface(ABC, LoginInterface):
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