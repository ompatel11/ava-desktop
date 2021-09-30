import sys
import threading
from subprocess import run

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QIcon
# GUI FILE
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QDialog

from FirebaseClientWrapper import FirebaseClientWrapper
from Sessionhandler import SessionHandler
from audio_manager import AudioManager
from user import User
from ui_form import Ui_main


class MainWindow(QMainWindow):
    def __init__(self):
        print(self)
        QMainWindow.__init__(self)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.MircophoneManager = AudioManager()
        self.sessionHandler = SessionHandler()
        self.current_user = User()
        self.Firebase_app = FirebaseClientWrapper()

        # SET TITLE BAR
        self.ui.frame_title.mouseMoveEvent = self.moveWindow

        # Title Bar buttons
        self.ui.btnWindowMinimize.clicked.connect(self.minimizeWindow)
        self.ui.btnWindowClose.clicked.connect(self.closeWindow)

        # Connecting functions to the components
        self.ui.btnLoginPage.clicked.connect(self.movetoLogin)
        self.ui.btnSignupPage.clicked.connect(self.movetoSignup)

        # Login process
        self.ui.btnLogin.clicked.connect(self.user_login)

        # Signup process
        self.ui.btnSignup.clicked.connect(self.user_signup)

        # Social Logins
        self.ui.btnGoogle.clicked.connect(self.google_login)
        # If user remember me == True then login
        self.is_persistent()

        # Show UI
        self.show()

    def moveWindow(self, event):
        # IF LEFT CLICK MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            try:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
            except Exception as e:
                pass

    def minimizeWindow(self):
        self.showMinimized()

    def closeWindow(self):
        QtCore.QCoreApplication.instance().quit()

    def openSettings(self):
        self.sessionHandler.deleteData()
        self.stackPanel.setCurrentIndex(0)

    def pausePlayMic(self):
        """
        Change the icon and background based on the state of the microphone
        Calls to the microphone manager class will be made from here.
        """
        if not self.isMic:
            self.ui.btnMicrophoneControl.setIcon(QIcon("Icons/Pause@2x.png"))
            self.ui.btnMicrophoneControl.setIconSize(QSize(64, 64))
            self.ui.btnMicrophoneControl.setStyleSheet("""
            background-color: white;
            border: none;
            """)
            if self.MircophoneManager is None:
                self.MircophoneManager = AudioManager()

            t1 = threading.Thread(target=self.MircophoneManager.start)
            t1.start()
            self.isMic = True
        else:
            self.ui.btnMicrophoneControl.setIconSize(QSize(32, 32))
            self.ui.btnMicrophoneControl.setIcon(QIcon("Icons/Icon ionic-ios-mic.png"))
            self.ui.btnMicrophoneControl.setStyleSheet("""
            background-color: rgb(62, 60, 84);
            border: 1px solid white;
            border-radius: 40;
            """)
            t2 = threading.Thread(target=self.MircophoneManager.stop)
            t2.start()
            self.MircophoneManager = None
            self.isMic = False

    def is_persistent(self):
        if self.sessionHandler.readData():
            self.ui.stackPanel.setCurrentIndex(2)

    def user_signup(self):
        """
        Takes the data from text fields entered by user and creates a new user if no errors are found
        """
        pwd = self.ui.txtPassword_signup.text()
        confirm_pwd = self.ui.txtConfirmPassword_signup.text()
        result = ""
        print(pwd, self.ui.txtEmail_signup.text())
        if pwd and confirm_pwd:
            if pwd == confirm_pwd:

                result = self.Firebase_app.signup_new_user(self.ui.txtEmail_signup.text(), self.ui.txtPassword_signup.text())
                if result is True:
                    self.RememberMe()
                    self.current_user.setData(self.ui.txtEmail_signup.text())
                    if self.isUser():
                        self.ui.stackPanel.setCurrentIndex(2)
                else:
                    # Set the error message for the user
                    print(result)
                    self.ui.lblError_signup.setText(result)
            elif pwd != confirm_pwd:
                self.ui.lblError_signup.setText("Passwords do not match")
            else:
                # Set Error passwords do not match
                self.ui.lblError_signup.setText(result)
        else:
            self.ui.lblError_signup.setText("Password fields cannot be empty")

    def RememberMe(self):
        """Returns True if credentials are found in the specified files or else returns false and navigate
        appropriately """
        self.sessionHandler.writeData()

    def isUser(self):
        return True if self.current_user.email is not None else False

    def google_login(self):
        import demo

    def user_login(self):
        """
        Takes the data from text fields entered by user and logs in the user if credentials are correct else show
        relevant errors.
        """

        email = self.ui.txtEmail_login.text()
        pwd = self.ui.txtPassword_login.text()
        result = None
        if pwd and email:
            # Persist login credentials pending
            result = self.Firebase_app.login_email_password(email, pwd)
        if result is True:
            # Navigate to home page
            if self.ui.chkRememberme.isChecked():
                self.RememberMe()
            self.current_user.setData(self.ui.txtEmail_signup.text())
            if self.isUser():
                self.ui.stackPanel.setCurrentIndex(2)
        else:
            # Set the error message for the user
            print(result)
            self.ui.lblError_login.setText(result)

    def movetoLogin(self):
        """
        Navigate to Login Page
        """
        self.ui.stackPanel.setCurrentIndex(0)

    def movetoSignup(self):
        """
        Navigate to Signup Page
        """
        self.ui.stackPanel.setCurrentIndex(1)

    # APP EVENTS
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
