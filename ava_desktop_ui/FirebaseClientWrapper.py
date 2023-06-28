import json

import schedule

import secrets
import time

from Models import user
import firebase

import Sessionhandler


class FirebaseClientWrapper:
    def __init__(self):
        config = {
            "apiKey": "",
            "authDomain": "ava-daemon.firebaseapp.com",
            "databaseURL": "",
            "projectId": "",
            "storageBucket": "",
            "messagingSenderId": "",
            "appId": "",
            "measurementId": ""
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
        self.firebase_app = firebase.Firebase(config)
        self.auth = self.firebase_app.auth()
        self.database = self.firebase_app.database()

    def updateAuthToken(self):
        print("Before refresh: ", user.current_user.auth_token)
        print("Refreshing auth token")
        new_user = Firebase_app.auth.refresh(user.current_user.refresh_token)
        user.current_user.auth_token = new_user['idToken']
        print("After refresh: ", user.current_user.auth_token)

    def signup_new_user(self, email, password, isPersist):
        """
        Returns true if created new user else returns error object
        """
        try:
            result = self.auth.create_user_with_email_and_password(email, password)
            print(result)
            user.current_user.uid = result["localId"]
            user.current_user.email = result["email"]
            user.current_user.auth_token = result["idToken"]
            user.current_user.refresh_token = result['refreshToken']
            user.current_user.idtoken = secrets.token_hex(32)
            print(user.current_user.email, user.current_user.idtoken, user.current_user.email)
            print("New user created: ")
            if isPersist:
                if Sessionhandler.sessionHandler.setUserData():
                    Sessionhandler.sessionHandler.setloginstate()
            return True
        except Exception as e:
            print("Error occured: ", e)
            errorMessage = self.error[str(json.loads(e.args[1])['error']['message'])]
            return errorMessage

    def send_email_verification(self):
        if user.current_user.email:
            try:
                result = self.auth.send_email_verification(user.current_user.auth_token)
                print(result)
            except Exception as e:
                print(e)

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
            user.current_user.auth_token = result["idToken"]
            user.current_user.refresh_token = result['refreshToken']
            print(user.current_user.refresh_token)
            if user.current_user.idtoken == '':
                user.current_user.idtoken = secrets.token_hex(32)
            print(user.current_user.email, user.current_user.uid, user.current_user.idtoken)

            if isPersist and result["email"]:
                result = Sessionhandler.sessionHandler.setUserData()
                print(result)
                Sessionhandler.sessionHandler.setloginstate()
            print("Log In Success")

        except Exception as e:
            print("Error occured: ", e)
            errorMessage = self.error[str(json.loads(e.args[1])['error']['message'])]
            print(errorMessage)

            return errorMessage

        return True

    def setUserObject(self):
        try:
            profile = {
                "loginstate": "True",
                "email": user.current_user.email,
            }
            if True:
                result = self.database.child("users_authenticated").child(
                    user.current_user.uid).child("profile").set(profile)
                print(result.val())
                print("Writing done")
                return True

        except Exception as e:
            print(e)
            return False

    def logout(self):
        Sessionhandler.sessionHandler.logout()


Firebase_app = FirebaseClientWrapper()
