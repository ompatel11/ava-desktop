# This Python file uses the following encoding: utf-8
import sys
import os
from qt_material import apply_stylesheet

from FirebaseClientWrapper import FirebaseClientWrapper
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QStackedWidget, QLineEdit
from PySide2.QtCore import QFile, QPropertyAnimation, QRect
from PySide2.QtUiTools import QUiLoader


class main(QWidget):
    def __init__(self):
        super(main, self).__init__()
        self.Firebase_app = FirebaseClientWrapper()
        self.load_ui()
        self.stackedPanel = self.findChild(QStackedWidget,"stackPanel")
        self.btnLoginPage = self.findChild(QPushButton, "btnLoginPage")
        self.btnSignupPage = self.findChild(QPushButton, "btnSignupPage")

        # Login Button
        self.btnLogin = self.findChild(QPushButton, "btnLogin")

        self.btnLogin.clicked.connect(self.user_login)
        # Login Page
        self.LoginPageWidget = self.findChild(QWidget, "LoginPage")

        # Signup Page
        self.SignupPageWidget = self.findChild(QWidget, "SignupPage")

        # Navigate to Login Page
        self.btnSignupPage.clicked.connect(self.movetoSignup)
        # Navigate to Signup Page
        self.btnLoginPage.clicked.connect(self.movetoLogin)

        # Textbox Email Login Page
        self.txtEmail_login = self.findChild(QLineEdit, "txtEmail_login")
        # Textbox Password Login Page
        self.txtPassword_login = self.findChild(QLineEdit, "txtPassword_login")

        # Textbox Email Signup Page
        self.txtEmail_signup = self.findChild(QLineEdit, "txtPassword_signup")
        # Textbox Password Signup Page
        self.txtPassword_signup = self.findChild(QLineEdit, "txtPassword_signup")

    def user_login(self):
        self.Firebase_app.login_email_password("email","pwd")

    def movetoLogin(self):
        self.stackedPanel.setCurrentIndex(0)

    def movetoSignup(self):

        self.stackedPanel.setCurrentIndex(1)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

if __name__ == "__main__":
    app = QApplication([])
    widget = main()

    widget.show()
    sys.exit(app.exec_())
