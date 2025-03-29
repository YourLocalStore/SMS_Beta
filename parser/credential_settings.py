import configparser

class WriteInfo:
    """ The class where the user attempts to connect to the database. The credentials are fed through an .ini file, which is configured
        by the user.

    Attributes:
        self.host (int): The hostname/IP that is used for the database connection.
        self.port (int): The port that is used in accordance with the hostname and SQL installation.
        self.user (str): The "super user" name within the SQL database, in most cases this is "root".
        self.password (str): The password of the database.

    Methods:
        __init__(self):
            The constructor for the database credentials.
        write_credentials(self):
            This method uses the configparser library to write any non-null values into an .ini file,
            however since all installations come with a pre-installed .ini file, this method will not
            be called during usage.
    """

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def write_credentials(self):
        parser = configparser.ConfigParser(allow_no_value=False)
        parser["Credentials"] = {
            "Host": self.host,
            "Port": self.port,
            "User": self.user,
            "Password": self.password
        }

        with open ("Credential-Configuration.ini", "w") as parsefile:
            parser.write(parsefile)
        return True

config = WriteInfo(
    host="", port="", 
    user="", password=""
)
config.write_credentials()