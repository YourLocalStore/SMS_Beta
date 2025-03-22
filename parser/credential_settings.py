import configparser

class WriteInfo:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def write_credentials(self):
        parser = configparser.ConfigParser(allow_no_value=False)
        parser["Credentials"] = {"Host": self.host,
                                "Port": self.port,
                                "User": self.user,
                                "Password": self.password,}

        with open ("Credential-Configuration.ini", "w") as parsefile:
            parser.write(parsefile)
        
        return True

config = WriteInfo(host="", port="", user="", password="")
config.write_credentials()