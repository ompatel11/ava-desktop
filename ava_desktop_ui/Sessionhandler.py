import json
import os
from configparser import ConfigParser

import requests

from Models import user
import FirebaseClientWrapper


class SessionHandler:
    def __init__(self):
        # Get the configparser object
        self.config_object = ConfigParser()
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
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
            print("Directory error while DeleteUserData()")
            return False

    def readUserData(self):
        try:
            self.config_object.read(self.fileName)
            userdata_object = self.config_object["data"]
            print("User Object from readUserData():", userdata_object['idtoken'])
            return userdata_object

        except Exception as e:
            print("Directory error while readUserData()")
            return False

    def setUserData(self):
        try:
            print("Before config file")
            print(user.current_user.email, user.current_user.idtoken)
            self.config_object["data"] = {
                "uid": user.current_user.uid,
                "email": user.current_user.email,
                "idtoken": user.current_user.idtoken,
                "authtoken": user.current_user.auth_token,
                "refreshtoken": user.current_user.refresh_token if user.current_user.refresh_token else "None",
                "isverified": str(user.current_user.isVerified),
                "loginstate": "True"
            }

            # Write the above sections to config.ini file
            with open(self.fileName, 'w+') as conf:
                self.config_object.write(conf)
            # win32api.SetFileAttributes(self.fileName, win32con.FILE_ATTRIBUTE_HIDDEN)
            return True

        except Exception as e:
            print("Directory error while setUserData()")
            return False

    def setloginstate(self):
        """
        Set the login state to database

        :return: True if sucessfull else False
        """
        try:
            userData = self.readUserData()
            try:
                result = requests.get(
                    f"http://localhost:5001/ava-daemon/us-central1/app/setloginstate?email={userData['email']}&uid={userData['uid']}&authtoken={userData['authtoken']}&isverified={userData['isverified']}&loginstate={userData['loginstate']}")
                result = json.loads(result.text)
                if result['status'] == 200:
                    print("Login state updated")
                    return True
                else:
                    return False
            except Exception as e:
                print(e)
                return False

        except Exception as e:
            print(e)
            return False

    def readloginstate(self):
        """
        Read the database login state

        :return: UserData if True else returns False
        """
        try:
            userData = self.readUserData()
            print("Token=", user.current_user.idtoken)
            print("Uid=", user.current_user.uid)
            result = requests.get(
                f"http://localhost:5001/ava-daemon/us-central1/app/readloginstate?email={userData['email']}")
            result = json.loads(result.text)
            if userData is not False and userData['idtoken'] != "None":
                user.current_user.uid = userData['uid']
                user.current_user.email = userData['email']
                user.current_user.idtoken = userData['idtoken']
                user.current_user.auth_token = userData['authtoken']
                user.current_user.refresh_token = userData['refreshtoken']
                user.current_user.isVerified = userData['isverified']

                try:
                    # FirebaseClientWrapper.Firebase_app.auth.refresh(userData["authtoken"])
                    if requests.get(
                            f"https://us-central1-ava-daemon.cloudfunctions.net/app/verify?uid={user.current_user.uid}").text == "Not verified":
                        user.current_user.isVerified = "False"
                        self.setUserData()
                except Exception as e:
                    print(e)
                    self.deleteUserData()
                    return False
                print("Token=", user.current_user.idtoken)
                print("Uid=", user.current_user.uid)
                print("Firebase result=", result)
                result = result["data"]
                user.current_user.lastloggedin = result['lastloggedin']
                print("Last logged in: ", result['lastloggedin'])
                # for key in result.val().keys():
                #     documentId = key
                # print("Here", result.val()[documentId])
                if result["loginstate"] == "True" and userData['loginstate'] == "True":
                    print("User Data from if : ", userData['loginstate'])

                    return userData

            else:
                # documentId = ""
                # for key in result.val().keys():
                #     documentId = key
                #     print("DocumentId=", documentId)
                userData = {'loginstate': result["loginstate"],
                            'email': result["email"], "uid": result['uid']}
                user.current_user.email = result["email"]
                user.current_user.uid = result['uid']
                self.setUserData()
                print("User Data from else called: ", userData)
                return userData

        except Exception as e:
            print(e)
            return False

    def setuserProfile(self):
        profile = {
            "email": user.current_user.email,
            "avatar": "https://avatars.dicebear.com/api/avataaars/hello.svg",
            "name": "Demo Name"
        }
        FirebaseClientWrapper.Firebase_app.database.child("users_authenticated") \
            .child(user.current_user.uid) \
            .child("user_profile").update(profile)

    def getCustomToken(self):
        pass

    def getuserProfile(self):
        result = FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(
            user.current_user.uid).get()

    def logout(self):
        """
        Completely logout user and update loginstate to the database

        :return: bool()
        """
        try:
            boolean_result = self.deleteUserData()
            result = requests.get(
                f"http://localhost:5001/ava-daemon/us-central1/app/setloginstate?email={user.current_user.email}&uid={user.current_user.uid}&authtoken={user.current_user.auth_token}&isverified={user.current_user.isVerified}&loginstate=False")
            result = json.loads(result.text)
            if result['status'] == 200:
                user.current_user.deleteData()

                print(boolean_result)
                print("Token from logout=", user.current_user.idtoken)
                print("Uid from logout=", user.current_user.uid)
                if boolean_result:
                    print("After")
                    print("Token=", user.current_user.idtoken)
                    print("Uid=", user.current_user.uid)
                    print("Writing done")
                    user.current_user.deleteData()
                return True
            else:
                return False
            # FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(
            #     user.current_user.uid).update(login_data)

        except Exception as e:
            print(e)
            return False


sessionHandler = SessionHandler()
