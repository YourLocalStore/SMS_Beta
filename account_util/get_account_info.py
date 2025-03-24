from prettytable import PrettyTable

class GetUserInformation():
    information_table = PrettyTable()
    information_table.field_names = ["First Name", "Last Name", 
                                     "Username", "Email Address", 
                                     "ID", "Password"]
    
    def __init__(self, fname, lname, user, email, uid, pwd):
        self.fname = fname
        self.lname = lname
        self.user = user
        self.email = email
        self.id = uid
        self.pwd = pwd

        GetUserInformation.information_table.add_row([
            self.fname, self.lname,
            self.user, self.email,
            self.id, self.pwd
        ])
    
    def __str__(self):
        return str(GetUserInformation.information_table)