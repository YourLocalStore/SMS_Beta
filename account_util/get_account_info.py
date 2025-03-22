from prettytable import PrettyTable

class GetUserInformation:
    information_table = PrettyTable()
    information_table.field_names = ["First Name", "Last Name", 
                                     "Username", "Email Address", 
                                     "Employee ID", "Password"]
    
    def __init__(self, fname, lname, user, id, pwd):
        self.fname = fname
        self.lname = lname
        self.user = user
        self.id = id
        self.pwd = pwd
    
    def __str__(self):
        table = self.information_table.add_row([
            self.get_fname(), self.get_lname(),
            self.get_username(), self.get_email(),
            self.get_teacher_id(), self.get_password()
        ])
        return table
    
    
