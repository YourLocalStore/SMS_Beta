Project by Joshua Tuibuen (INFR2141U)

# Welcome to the Student Management System (SMS)!
This is a simple, easy-to-use management system that is mainly housed on MySQL to fetch and send data. You can think of it as some sort of "simulator" for a traditional LMS, just simpler!
Some of the features include:

- A Login and Register System
- Adding and Removing Students
- Viewing Student Information
- Viewing Account Information

``` Please ensure to read 'Getting Started', as it's extremely important to use specific parameters and libraries to run the program.```

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

Rather, the database will be run on the user's machine instead (see 'Getting Started')
```

First, you need to register an account. This is really just a school project, you can enter anything you want as a field and it will accept it! 
You can choose between three different types of users:
- Student, which can view and manage account information and look at classrooms they are in.
- Teacher, which can view and manage student within the classroom, as well as their own information.
- Administrator, highest level of permissions, can do anything from managing all classrooms to removing teachers/students.

Once you make your "account", you will be given sets of options depending on what you choose. There should be a "help" option across all accounts once
you login which tells you what each option does. 

# Getting Started (Libraries and Modules)
If you haven't already, you will need to clone this project. In your VSCode Terminal, enter:
```
git clone https://github.com/YourLocalStore/SMS_Beta.git
```
Then, you must install the following packages/libraries by doing the following:
```
pip install mysql-connector-python
pip install python-dotenv
pip install ptable
pip install passlib
```

```Credentials are already provided to you, and the only value you need to change is the password attribute in sqldb.py (see below for more infomation).```


# Getting Started (MySQL Connection)
You will need to download the [SQL Installer](https://dev.mysql.com/downloads/installer/).
You may watch a [quick installation guide here](https://www.youtube.com/watch?v=pK-U5L75PYk), otherwise here are the steps:

1. In the installer, you can choose between what features you can install. Just ensure that the installation includes both the ```MySQL Server``` and ```MySQL Workbench```
2. Keep everything default, besides the password you make (making a user is not needed and will default to a ```root``` user). Ensure to keep this password, as it is important for the database connection.

After installing, locate the "+" icon next to ```"MySQL Connections"``` in the ```MySQL Workbench```, then ensure the following settings in ```"Parameters"```:
```
Connection Name - {Enter any name}
Connection Method - Standard (TCP/IP)
Hostname - 127.0.0.1
Port - 3306
Username - root
```

After that, click "OK", then enter the SQL connection you just made! 
Make sure that the MySQL Windows service is running ```(Task Manager -> Services -> Search "SQL")```. 

As a further note... In the codebase, there is one value you need to change. This is to ensure the connection is fully met between your database and the connector.
In future updates, I'll just setup a config file for the user to change.

1. In ```sqldb.py``` there is a ```ConnectSQLDatabase``` class.
2. Within ```__init__``` change the ```password``` attribute to the password you used for the installation.
3. Save the ```sqldb.py``` file, then run ```main.py```







