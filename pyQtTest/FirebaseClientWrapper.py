# This Python file uses the following encoding: utf-8
import json

import pyrebase


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

            "ERROR_TOO_MANY_REQUESTS": "Too many attempts made to log into this account.",

            "ERROR_OPERATION_NOT_ALLOWED": "Server under maintenance, please try again later.",
            "operation-not-allowed": "Server under maintenance, please try again later.",

            "EMAIL_NOT_FOUND": "Email address not found.",

        }
        self.firebase_app = pyrebase.initialize_app(config)
        self.auth = self.firebase_app.auth()

        # Log the user in
        self.user = ''

    def signup_new_user(self, email, password):
        """
        Returns true if created new user else returns error object
        """
        try:
            result = self.auth.create_user_with_email_and_password(email, password)
        except Exception as e:

            errorMessage = self.error[str(json.loads(e.args[1])['error']['message'])]
            print(e)
            return errorMessage

        return True

    def login_email_password(self, email, password):
        """
        Returns true if user is logged in else returns error object
        """
        try:
            result = self.auth.sign_in_with_email_and_password(email, password)
            print("Log In Success")

        except Exception as e:
            print(e)
            errorMessage = self.error[str(json.loads(e.args[1])['error']['message'])]
            print(errorMessage)

            return errorMessage

        return True

# obj = FirebaseClientWrapper()
