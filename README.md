First-Year Programming Project for IT

# Welcome to the Student Management System (SMS)!
This is a simple, easy-to-use management system that is mainly housed on MySQL to fetch and send data. You can think of it as some sort of "simulator" for a traditional LMS, just simpler!
Some of the features include:

- A Login and Register System
- Adding and Removing Students
- Viewing Student Information
- Viewing Account Information

Please ensure to read [Getting Started](#getting-started-libraries-and-modules), as it's extremely important to use specific parameters and libraries to run the program.

# Built With
This is a list of libraries and modules that were used throughout this project:
- MySQL, for database features;
- PTable, for formatting tables;
- Datetime & Time, for time-related outputs (or to delay some functions);
- Threading, for some things to load simultaneously

# How does it Work?

It's a console-based program, so no TKinter or GUI-based programs were involved in the making, except for some formatting libraries like PTable.
```
NOTE: For simplicity, security, and less error-prone events, this program will be **locally run**, meaning the SQL database will
not query to a dedicated machine to connect to and send data.
```
The database will be run on the user's machine instead (see [Getting Started - MySQL Connections](#getting-started-mysql-connection)).

Moving on, you need to register an account. This is really just a school project, you can enter anything you want as a field and it will accept it! 
You can choose between three different types of users:
- Student, which can view and manage account information and look at classrooms they are in.
- Teacher, which can view and manage student within the classroom, as well as their own information.
- Administrator, highest level of permissions, can do anything from managing all classrooms to removing teachers/students.

Observe that for administrators, they were manually added. That's why I have inserted a test account in ```sqldb.py``` under the following credentials if you want one to play around with:
```python
admin_vals = (
    AdministratorID="727",
    FirstName="root", 
    LastName="user",
    UserName="rootadministrator",
    EmailAddress="root@yourlocalstore.com",
    Password="!_INFR2025_$$$$$$"
)
```

Once you make your "account" and log in, you will be given sets of options depending on what you choose.

# Getting Started (Libraries and Modules)
If you haven't already, you will need to clone this project. In your VSCode Terminal, enter:
```
git clone https://github.com/YourLocalStore/SMS_Beta.git
```
Alternatively, you can simply download the ZIP file of this project, and move the unzipped folder into VSCode.

Then, you must install the following packages/libraries by doing the following:
```
pip install mysql-connector-python
pip install python-dotenv
pip install ptable
pip install passlib
pip install configparser
```

# Getting Started (MySQL Connection)
You will need to download the [SQL Installer](https://dev.mysql.com/downloads/installer/), specifically the 352MB version in 32-bit.
You may watch a [quick installation guide here](https://www.youtube.com/watch?v=pK-U5L75PYk), otherwise here are the steps:

1. In the installer, you can choose between what features you can install. Just ensure that the installation includes both the ```MySQL Server``` and ```MySQL Workbench```, if you are unsure, just select a full installation.
2. Keep everything default, besides the password you make (making a user is not needed and will default to a ```root``` user). Ensure to keep this password, as it is important for the database connection.

After installing, locate the "+" icon next to ```"MySQL Connections"``` in the ```MySQL Workbench```, then ensure the following settings in ```Parameters```:
```
Connection Name - {Enter any name}
Connection Method - Standard (TCP/IP)
Hostname - 127.0.0.1
Port - 3306
Username - root
```

After that, click "OK", then enter the SQL connection you just made using the password from installation.
Make sure that the MySQL Windows service is running ```(Task Manager -> Services -> Search "SQL")```. 

For the final step, there is a config file in the codebase named ```Credential-Configuration.ini```.
1. In ```Credential-Configuration.ini```, you will need to change the fields according to your database configuration.

This is what the ```Credential-Configuration.ini``` file should look like:
```ini
[Credentials]
host =
port = 
user =
password = 
```

2. Once that is done, Save the ```Credential-Configuration.ini``` file, then run ```main.py```.

The ```.ini``` file will grab these credentials and use them in the SQL connector like so:
```python
self.sql_serv = mysql.connector.connect(
    charset = "utf8",
    use_unicode = True,
    host = self.config["Credentials"]["Host"],
    port = self.config["Credentials"]["Port"],
    user = self.config["Credentials"]["User"],
    password = self.config["Credentials"]["Password"],
    connection_timeout = 300
)
```
So there is no need to change any values in ```sqldb.py```.







