# This Python file uses the following encoding: utf-8
import sys
import os
import threading

from FirebaseClientWrapper import FirebaseClientWrapper
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import Qt
from PySide2 import QtCore

from pyQtTest.audio_manager import AudioManager


class MainApp(QWidget):

    def __init__(self):
        super(MainApp, self).__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.Firebase_app = FirebaseClientWrapper()
        self.MircophoneManager = AudioManager()
        self.load_ui()
        self.stackedPanel = self.findChild(QStackedWidget, "stackPanel")
        self.stackedPanel.setCurrentIndex(0)
        self.btnLoginPage = self.findChild(QPushButton, "btnLoginPage")
        self.btnSignupPage = self.findChild(QPushButton, "btnSignupPage")

        # Main Window Widget
        self.mainWindow = self.findChild(QWidget, "main")

        # Title Bar Buttons
        self.btnWindowMinimize = self.findChild(QPushButton, "btnWindowMinimize")
        self.btnWindowMinimize.clicked.connect(self.minimizeWindow)
        self.btnWindowClose = self.findChild(QPushButton, "btnWindowClose")
        self.btnWindowClose.clicked.connect(QtCore.QCoreApplication.instance().quit)

        # Login Page
        self.LoginPageWidget = self.findChild(QWidget, "LoginPage")
        self.txtEmail_login = self.findChild(QLineEdit, "txtEmail_login")
        self.txtPassword_login = self.findChild(QLineEdit, "txtPassword_login")
        # Login Button
        self.btnLogin = self.findChild(QPushButton, "btnLogin")
        self.btnLogin.clicked.connect(self.user_login)

        # Signup Page
        self.SignupPageWidget = self.findChild(QWidget, "SignupPage")
        self.txtEmail_signup = self.findChild(QLineEdit, "txtEmail_login")
        self.txtPassword_signup = self.findChild(QLineEdit, "txtPassword_signup")
        self.txtConfirmPassword_signup = self.findChild(QLineEdit, "txtConfirmPassword_signup")
        self.lblError_signup = self.findChild(QLabel, "lblError_signup")

        # Signup Button
        self.btnSignup = self.findChild(QPushButton, "btnSignup")
        self.btnSignup.clicked.connect(self.user_signup)
        # Navigate to Login Page
        self.btnSignupPage.clicked.connect(self.movetoSignup)
        # Navigate to Signup Page
        self.btnLoginPage.clicked.connect(self.movetoLogin)

        # Textbox Email Login Page
        self.txtEmail_login = self.findChild(QLineEdit, "txtEmail_login")
        # Textbox Password Login Page
        self.txtPassword_login = self.findChild(QLineEdit, "txtPassword_login")
        # Error Label Login Page
        self.lblError_login = self.findChild(QLabel, "lblError_login")

        # Textbox Email Signup Page
        self.txtEmail_signup = self.findChild(QLineEdit, "txtPassword_signup")
        # Textbox Password Signup Page
        self.txtPassword_signup = self.findChild(QLineEdit, "txtPassword_signup")

        # Microphone and Trascription Page
        self.btnMicrophoneControl = self.findChild(QPushButton, "btnMicrophoneControl")
        self.isMic = False

        # Connect Microphone to change the display icon
        self.btnMicrophoneControl.clicked.connect(self.pausePlayMic)
        self.lblLiveTranscript = self.findChild(QLabel, "lblLiveTranscript")

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def minimizeWindow(self):
        self.showMinimized()

    def pausePlayMic(self):
        """
        Change the icon and background based on the state of the microphone
        Calls to the microphone manager class will be made from here.
        """
        if not self.isMic:
            self.btnMicrophoneControl.setIcon(QIcon("Icons/Pause@2x.png"))
            self.btnMicrophoneControl.setIconSize(QSize(64, 64))
            self.btnMicrophoneControl.setStyleSheet("""
            background-color: white;
            border: none;
            """)
            if self.MircophoneManager is None:
                self.MircophoneManager = AudioManager()

            t1 = threading.Thread(target=self.MircophoneManager.start)
            t1.start()
            self.isMic = True
        else:
            self.btnMicrophoneControl.setIconSize(QSize(32, 32))
            self.btnMicrophoneControl.setIcon(QIcon("Icons/Icon ionic-ios-mic.png"))
            self.btnMicrophoneControl.setStyleSheet("""
            background-color: rgb(62, 60, 84);
            border: 1px solid white;
            border-radius: 40;
            """)
            t2 = threading.Thread(target=self.MircophoneManager.stop)
            t2.start()
            self.MircophoneManager = None
            self.isMic = False

    def user_signup(self):
        """
        Takes the data from text fields entered by user and creates a new user if no errors are found
        """
        pwd = self.txtPassword_signup.text()
        confirm_pwd = self.txtConfirmPassword_signup.text()
        result = ""
        print(pwd, self.txtEmail_signup.text())
        if pwd and confirm_pwd:
            if pwd == confirm_pwd:
                result = self.Firebase_app.signup_new_user(self.txtEmail_signup.text(), self.txtPassword_signup.text())
                if result == True:
                    self.stackedPanel.setCurrentIndex(2)
                else:
                    # Set the error message for the user
                    print(result)
                    self.lblError_signup.setText(result)
            elif pwd != confirm_pwd:
                self.lblError_signup.setText("Passwords do not match")
            else:
                # Set Error passwords do not match
                self.lblError_signup.setText(result)
        else:
            self.lblError_signup.setText("Password fields cannot be empty")

    def user_login(self):
        """
        Takes the data from text fields entered by user and logs in the user if credentials are correct else show
        relevent errors.
        """
        email = self.txtEmail_login.text()
        pwd = self.txtPassword_login.text()
        result = ""
        if pwd and email:
            # Persist login credentials pending
            result = self.Firebase_app.login_email_password(email, pwd)
        if result == True:
            # Navigate to home page
            self.stackedPanel.setCurrentIndex(2)
        else:
            # Set the error message for the user
            print(result)
            self.lblError_login.setText(result)

    def movetoLogin(self):
        """
        Navigate to Login Page
        """
        self.stackedPanel.setCurrentIndex(0)

    def movetoSignup(self):
        """
        Navigate to Signup Page
        """
        self.stackedPanel.setCurrentIndex(1)

    def load_ui(self):
        """
        Load the UI from the 'form.ui' file
        """
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainApp()

    widget.show()
    sys.exit(app.exec_())
