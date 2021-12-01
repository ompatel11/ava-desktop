# This Python file uses the following encoding: utf-
import json
import secrets

from Model import user
import pyrebase

import Sessionhandler


class FirebaseClientWrapper:
    def __init__(self):
        config = {
            "apiKey": "AIzaSyBtitwcE_As4_dMv8GQrXOgfi2ePwiEhbQ",
            "authDomain": "ava-daemon.firebaseapp.com",
            "databaseURL": "https://ava-daemon.firebaseio.com",
            "projectId": "ava-daemon",
            "storageBucket": "ava-daemon.appspot.com",
            "messagingSenderId": "41961847947",
            "appId": "1:41961847947:web:f65107ad2f44e29c9aa88e",
            "measurementId": "G-CY5HDPPDY5"
        }
        self.error = {
            "EMAIL_EXISTS": "Email already is use. Try logging in.",

            "INVALID_PASSWORD": "Incorrect email/password.",
            "INVALID_EMAIL": "Invalid email address.",

            "USER_DISABLED": "User disabled contact the support team.",

            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts made to log into this account, you can immediately "
                                           "restore it by resetting your password or you can try again later",

            "ERROR_OPERATION_NOT_ALLOWED": "Server under maintenance, please try again later.",
            "operation-not-allowed": "Server under maintenance, please try again later.",

            "EMAIL_NOT_FOUND": "Email address not found.",

        }
        self.firebase_app = pyrebase.initialize_app(config)
        self.auth = self.firebase_app.auth()
        self.database = self.firebase_app.database()

    def signup_new_user(self, email, password, isPersist):
        """
        Returns true if created new user else returns error object
        """
        try:
            result = self.auth.create_user_with_email_and_password(email, password)
            print(result)
            user.current_user.uid = result["localId"]
            user.current_user.email = result["email"]
            user.current_user.idtoken = secrets.token_hex(32)
            print(user.current_user.email, user.current_user.idtoken, user.current_user.email)
            print("New user created")
            if isPersist:
                if Sessionhandler.sessionHandler.setUserData():
                    Sessionhandler.sessionHandler.setloginstate()
            return True
        except Exception as e:

            errorMessage = self.error[str(json.loads(e.args[1])['error']['message'])]
            print(e)
            return errorMessage

    def login_email_password(self, email, password, isPersist):
        """
        Returns true if user is logged in else returns error object
        """
        try:
            result = self.auth.sign_in_with_email_and_password(email, password)
            # self.user_id = result.
            print(result["localId"])
            user.current_user.uid = result["localId"]
            user.current_user.email = result["email"]
            print(type(user.current_user.idtoken))
            print(user.current_user.idtoken)
            if user.current_user.idtoken is '':
                user.current_user.idtoken = user.current_user.idtoken = secrets.token_hex(32)
            print(user.current_user.email, user.current_user.uid, user.current_user.idtoken)

            if isPersist:
                result = Sessionhandler.sessionHandler.setUserData()
                print(result)
                Sessionhandler.sessionHandler.setloginstate()
            print("Log In Success")

        except Exception as e:
            print(e)
            errorMessage = self.error[str(json.loads(e.args[1])['error']['message'])]
            print(errorMessage)

            return errorMessage

        return True

    def logout(self):
        Sessionhandler.sessionHandler.logout()


Firebase_app = FirebaseClientWrapper()
