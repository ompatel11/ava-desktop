# This Python file uses the following encoding: utf-8
import pyrebase

class FirebaseClientWrapper:
    def __init__(self):
        config ={
            "apiKey": "AIzaSyBtitwcE_As4_dMv8GQrXOgfi2ePwiEhbQ",
            "authDomain": "ava-daemon.firebaseapp.com",
            "databaseURL": "https://ava-daemon.firebaseio.com",
            "projectId": "ava-daemon",
            "storageBucket": "ava-daemon.appspot.com",
            "messagingSenderId": "41961847947",
            "appId": "1:41961847947:web:f65107ad2f44e29c9aa88e",
            "measurementId": "G-CY5HDPPDY5"
         }

        self.firebase_app = pyrebase.initialize_app(config)
        self.auth = self.firebase_app.auth()

        # Log the user in
        self.user = ''

    def signup_new_user(self,email,password):
        """
        Returns true if created new user else returns error object
        """
        try:
            self.user = self.auth.create_user_with_email_and_password(email,password)
            return true
        except Exception as e:
            print(e)
            return e

    def login_email_password(self,email, password):
        """
        Returns true if user is logged in else returns error object
        """
        try:
            self.user = self.auth.sign_in_with_email_and_password(email,password)
            print("Log In Success")
            return true
        except Exception as e:
            print(e)
            return e




