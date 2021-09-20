import win32con, win32api, os
from configparser import ConfigParser


class SessionHandler:
    def __init__(self):
        # Get the configparser object
        self.config_object = ConfigParser()
        self.fileName = "config.ini"

    def encryptData(self):
        pass

    def writeData(self):
        # Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
        self.config_object["data"] = {
            "rememberme": "True",
        }

        # Write the above sections to config.ini file
        with open('config.ini', 'w') as conf:
            self.config_object.write(conf)
        win32api.SetFileAttributes(self.fileName, win32con.FILE_ATTRIBUTE_HIDDEN)
        print("Writing done")

    def readData(self):
        # Read config.ini file
        try:
            self.config_object.read("config.ini")
            isRemember = self.config_object["data"]["rememberme"]
            print(bool(isRemember))
            return bool(isRemember)

        except Exception as e:
            return False


# obj = SessionHandler()
# obj.writeData()
# obj.readData()
