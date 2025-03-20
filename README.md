Project by Joshua Tuibuen (INFR2141U)

# Welcome to the Student Management System (SMS)!
Kept together with zip ties and duct tape, this is a simple, easy-to-use management system that is mainly housed on MySQL to fetch and send data. You can think of it as some sort of "simulator" for a traditional LMS, just simpler!
Some of the features include:

- A Login and Register System
- Adding and Removing Students
- Viewing Student Information
- Viewing Account Information

# Built With
This is a list of libraries and modules that were used throughout this project:
- MySQL, for database features;
- PTable, for formatting tables;
- Datetime & Time, for time-related outputs (or to delay some functions);
- Threading, for some things to load simultaneously

# How does it Work?

It's a console-based program, so no TKinter or GUI-based programs were involved in the making, except for some formatting libraries like PTable.

First, you need to register an account. This is really just a school project, you can enter anything you want as a field and it will accept it! 
You can choose between three different types of users:
- Student, which can view and manage account information and look at classrooms they are in.
- Teacher, which can view and manage student within the classroom, as well as their own information.
- Administrator, highest level of permissions, can do anything from managing all classrooms to removing teachers/students.

Once you make your "account", you will be given sets of options depending on what you choose. There should be a "help" option across all accounts once
you login which tells you what each option does. 

# Getting Started
If you haven't already, you will need to clone this project. In your VSCode Terminal, enter:
```
git clone https://github.com/YourLocalStore/SMS_Beta.git
```
Then, you must install the following packages/libraries by doing the following:
```
pip install mysql-connector
pip install python-dotenv
pip install ptable
pip install passlib
```
The guest account for the database has already been given, so there's **no need** to modify any of the strings for the ODBC connection in sqldb.py.

You will need to download the [SQL Workbench](https://dev.mysql.com/downloads/workbench/) to have a remote connection to the database (note that this is an installation for x64 Windows).
After installing, locate the "+" icon next to "MySQL Connections", and do the following:
```
1. Enter a connection name (this is mandatory)
2. Change "Hostname" to "LocalComputer", which should be set to Port 3306
3. Set the "Username" to "guest"
3a. Ensure that the connection is okay by clicking "test connection". You will be prompted to enter a password.
  - Please try "ChickenBeagleNoodleSoup4$$$$$@!#" as this is the guest password; it will not work with any other user.
3b. If a connection can be made, click the "ok" button and enter the database using the same password.
```
After that, you should be fully connected to the database! You just need to run:
```
py main.py
```






