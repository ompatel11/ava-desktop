from configparser import ConfigParser
import os

import pyrebase.pyrebase
import win32api
import win32con
from FirebaseClientWrapper import Firebase_app
import user


class SessionHandler:
    def __init__(self):
        # Get the configparser object
        self.config_object = ConfigParser()
        self.fileName = "application/config/config.ini"

    def readUserData(self):
        try:
            self.config_object.read(self.fileName)
            userdata_object = self.config_object["data"]
            return userdata_object

        except Exception as e:
            print(e)
            return False

    def setUserData(self):
        try:
            print("Before config file")
            print(user.current_user.email, user.current_user.uid)
            self.config_object["data"] = {
                "uid": user.current_user.uid,
                "email": user.current_user.email,
                "idToken": user.current_user.idToken,
                "loginState": "True"
            }

            # Write the above sections to config.ini file
            with open('config.ini', 'w+') as conf:
                self.config_object.write(conf)
            # win32api.SetFileAttributes(self.fileName, win32con.FILE_ATTRIBUTE_HIDDEN)
            return True

        except Exception as e:
            print(e)
            return False

    def deleteData(self):
        try:
            os.remove(self.fileName)
        except Exception as e:
            print(e)

    def setLoginState(self):
        # Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG

        try:
            login_data = {
                "loginState": "True",
                "email": user.current_user.email,

            }
            userData = self.readUserData()
            if True:
                result = Firebase_app.database.child("users_authenticated").child(user.current_user.idToken).child(user.current_user.uid).set(login_data)
                print(result.val())
                print("Writing done")
                return True

        except Exception as e:
            print(e)
            return False

    def readLoginState(self):
        # Read the database login state
        try:
            userData = self.readUserData()
            print("Token=",user.current_user.idToken)
            print("Uid=",user.current_user.uid)
            result = Firebase_app.database.child("users_authenticated").child(user.current_user.idToken).child(
                user.current_user.uid).get()
            print(result.val())
            if userData is not False:
                documentId = ""
                for key in result.val().keys():
                    documentId = key

                if result.val()[documentId]["loginState"] == userData["state"]:
                    return userData

            else:
                documentId = ""
                for key in result.val().keys():
                    documentId = key
                    print("DocumentId=", documentId)
                userData = {'loginState': result.val()[documentId]["loginState"], 'email': result.val()[documentId]["email"], "uid": documentId}
                self.setUserData()

                return userData

        except Exception as e:
            print(e)
            return False

    def logout(self):
        try:
            login_data = {
                "loginState": "False",
                "email": user.current_user.email
            }
            print("Token=", user.current_user.idToken)
            print("Uid=", user.current_user.uid)
            result = Firebase_app.database.child("users_authenticated").child(user.current_user.idToken).child(user.current_user.uid).update(login_data)
            print(result.val())
            self.deleteData()
            print("Writing done")
            return True

        except Exception as e:
            return False


sessionHandler = SessionHandler()
