import os
from configparser import ConfigParser

import user
import FirebaseClientWrapper


class SessionHandler:
    def __init__(self):
        # Get the configparser object
        self.config_object = ConfigParser()
        self.fileName = "application/config/config.ini"

    def deleteUserData(self):
        try:
            print("Before config file")
            print(user.current_user.email, user.current_user.idtoken)
            self.config_object["data"] = {
                "uid": "None",
                "email": "None",
                "idtoken": "None",
                "loginstate": "False"
            }

            # Write the above sections to config.ini file
            with open(self.fileName, 'w+') as conf:
                self.config_object.write(conf)
            # win32api.SetFileAttributes(self.fileName, win32con.FILE_ATTRIBUTE_HIDDEN)
            return True

        except Exception as e:
            print(e)
            return False

    def readUserData(self):
        try:
            self.config_object.read(self.fileName)
            userdata_object = self.config_object["data"]
            print("User Object from readUserData():", userdata_object['idtoken'])
            return userdata_object

        except Exception as e:
            print(e)
            return False

    def setUserData(self):
        try:
            print("Before config file")
            print(user.current_user.email, user.current_user.idtoken)
            self.config_object["data"] = {
                "uid": user.current_user.uid,
                "email": user.current_user.email,
                "idtoken": user.current_user.idtoken,
                "loginstate": "True"
            }

            # Write the above sections to config.ini file
            with open(self.fileName, 'w+') as conf:
                self.config_object.write(conf)
            # win32api.SetFileAttributes(self.fileName, win32con.FILE_ATTRIBUTE_HIDDEN)
            return True

        except Exception as e:
            print(e)
            return False

    def setloginstate(self):
        # Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG

        try:
            login_data = {
                "loginstate": "True",
                "email": user.current_user.email,

            }
            userData = self.readUserData()
            if True:
                result = FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(
                    user.current_user.idtoken).child(
                    user.current_user.uid).update(login_data)
                print(result.val())
                print("Writing done")
                return True

        except Exception as e:
            print(e)
            return False

    def readloginstate(self):
        # Read the database login state
        try:
            userData = self.readUserData()
            print("Token=", user.current_user.idtoken)
            print("Uid=", user.current_user.uid)
            result = FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(
                userData['idtoken']).child(
                userData['uid']).get()
            if userData is not False and userData['idtoken'] != "None":
                user.current_user.uid = userData['uid']
                user.current_user.email = userData['email']
                user.current_user.idtoken = userData['idtoken']
                print("Token=", user.current_user.idtoken)
                print("Uid=", user.current_user.uid)
                documentId = ""
                print(result.val())
                for key in result.val().keys():
                    documentId = key
                print("Here", type(result.val()[documentId]))
                if result.val()[documentId] == "True" and userData['loginstate'] == "True":
                    print("User Data from else: ", userData['loginstate'])
                    return userData

            else:
                documentId = ""
                for key in result.val().keys():
                    documentId = key
                    print("DocumentId=", documentId)
                userData = {'loginstate': result.val()[documentId],
                            'email': result.val()[documentId]["email"], "uid": documentId}
                user.current_user.email = result.val()[documentId]["email"]
                user.current_user.uid = documentId
                self.setUserData()
                print("User Data from else: ", userData)
                return userData

        except Exception as e:
            print(e)
            return False

    async def logout(self):
        try:
            login_data = {
                "loginstate": "False",
                "email": user.current_user.email
            }
            boolean_result = self.deleteUserData()
            print("Token from logout=", user.current_user.idtoken)
            print("Uid from logout=", user.current_user.uid)
            result = await FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(
                user.current_user.idtoken).remove()
            # .child(
            #     user.current_user.uid).update(login_data)
            print(result.val())
            # user.current_user.deleteData()

            print(boolean_result)
            print("Token from logout=", user.current_user.idtoken)
            print("Uid from logout=", user.current_user.uid)
            if boolean_result:
                print("After")
                print("Token=", user.current_user.idtoken)
                print("Uid=", user.current_user.uid)
                print("Writing done")
            return True

        except Exception as e:
            return False


sessionHandler = SessionHandler()
