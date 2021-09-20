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
from PySide2 import QtCore, QtGui, QtWidgets

from audio_manager import AudioManager
from Sessionhandler import  SessionHandler

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
        self.sessionHandler = SessionHandler()
        # Main Window Widget
        self.mainWindow = self.findChild(QWidget, "main")

        # Login Page
        self.LoginPageWidget = self.findChild(QWidget, "LoginPage")
        self.txtEmail_login = self.findChild(QLineEdit, "txtEmail_login")
        self.txtPassword_login = self.findChild(QLineEdit, "txtPassword_login")
        self.chkRememberme = self.findChild(QCheckBox, "chkRememberme")

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
        self.txtEmail_signup = self.findChild(QLineEdit, "txtEmail_signup")
        # Textbox Password Signup Page
        self.txtPassword_signup = self.findChild(QLineEdit, "txtPassword_signup")

        # Microphone and Trascription Page
        self.btnMicrophoneControl = self.findChild(QPushButton, "btnMicrophoneControl")
        self.isMic = False

        # Connect Microphone to change the display icon
        self.btnMicrophoneControl.clicked.connect(self.pausePlayMic)
        self.lblLiveTranscript = self.findChild(QLabel, "lblLiveTranscript")

        # Title Bar
        self.title_bar_2 = QtWidgets.QFrame(self.mainWindow)
        self.title_bar_2.setGeometry(QtCore.QRect(0, 0, 501, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_bar_2.sizePolicy().hasHeightForWidth())
        self.title_bar_2.setSizePolicy(sizePolicy)
        self.title_bar_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar_2.setStyleSheet("background-color: none;")
        self.title_bar_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title_bar_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title_bar_2.setObjectName("title_bar_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.title_bar_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_title = QtWidgets.QFrame(self.title_bar_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_title.sizePolicy().hasHeightForWidth())
        self.frame_title.setSizePolicy(sizePolicy)
        self.frame_title.setMinimumSize(QtCore.QSize(10, 50))
        font = QtGui.QFont()
        font.setFamily("Roboto Condensed Light")
        font.setPointSize(14)
        self.frame_title.setFont(font)
        self.frame_title.setStyleSheet("background-color: rgb(62, 60, 84);\n"
                                       "border:none;")
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_title)
        self.verticalLayout_2.setContentsMargins(0, 0, 350, 20)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnSettings = QtWidgets.QPushButton(self.frame_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSettings.sizePolicy().hasHeightForWidth())
        self.btnSettings.setSizePolicy(sizePolicy)
        self.btnSettings.setStyleSheet("QPushButton{\n"
                                       "background-color: rgb(63, 61, 85);\n"
                                       "border: 0px solid rgb(63, 61, 85);}\n"
                                       "QPushButton:hover{\n"
                                       "background-color: rgb(99, 96, 134);\n"
                                       "}\n"
                                       "")
        self.btnSettings.setIcon(QtGui.QIcon("Icons/Icon ionic-ios-settings.png"))
        self.btnSettings.setIconSize(QtCore.QSize(12, 12))
        self.btnSettings.setObjectName("btnSettings")
        self.verticalLayout_2.addWidget(self.btnSettings)
        self.horizontalLayout.addWidget(self.frame_title)
        self.frame_btns = QtWidgets.QFrame(self.title_bar_2)
        self.frame_btns.setMaximumSize(QtCore.QSize(100, 16777215))
        self.frame_btns.setStyleSheet("border:none;")
        self.frame_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns.setObjectName("frame_btns")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_btns)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnWindowMinimize = QtWidgets.QPushButton(self.frame_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWindowMinimize.sizePolicy().hasHeightForWidth())
        self.btnWindowMinimize.setSizePolicy(sizePolicy)
        self.btnWindowMinimize.setMinimumSize(QtCore.QSize(10, 20))
        self.btnWindowMinimize.setStyleSheet("QPushButton{\n"
                                             "background-color: rgb(63, 61, 85);\n"
                                             "border: 0px solid rgb(63, 61, 85);}\n"
                                             "QPushButton:hover{\n"
                                             "background-color: rgb(99, 96, 134);\n"
                                             "}\n"
                                             "")
        self.btnWindowMinimize.setIcon(QtGui.QIcon("Icons/Icon awesome-window-minimize.png"))
        self.btnWindowMinimize.setIconSize(QtCore.QSize(8, 8))
        self.btnWindowMinimize.setObjectName("btnWindowMinimize")
        self.btnWindowMinimize.clicked.connect(self.minimizeWindow)
        self.horizontalLayout_3.addWidget(self.btnWindowMinimize)
        self.btnWindowClose = QtWidgets.QPushButton(self.frame_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWindowClose.sizePolicy().hasHeightForWidth())
        self.btnWindowClose.setSizePolicy(sizePolicy)
        self.btnWindowClose.setMinimumSize(QtCore.QSize(10, 20))
        self.btnWindowClose.setStyleSheet("QPushButton{\n"
                                          "background-color: rgb(63, 61, 85);\n"
                                          "border: 0px solid rgb(63, 61, 85);\n"
                                          "}\n"
                                          "QPushButton:hover{\n"
                                          "background-color: rgb(255, 0, 0);\n"
                                          "}")
        self.btnWindowClose.setIcon(QtGui.QIcon("Icons/Icon ionic-ios-close.png"))
        self.btnWindowClose.setIconSize(QtCore.QSize(8, 8))
        self.btnWindowClose.setObjectName("btnWindowClose")
        self.btnWindowClose.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.horizontalLayout_3.addWidget(self.btnWindowClose)
        self.horizontalLayout.addWidget(self.frame_btns)

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.frame_title.mouseMoveEvent = moveWindow
        self.is_persistent()

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

    def is_persistent(self):
        if self.sessionHandler.readData():
            self.stackedPanel.setCurrentIndex(2)

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

    def RememberMe(self):
        """Returns True if credentials are found in the specified files or else returns false and navigate
        appropriately """
        if self.chkRememberme.isChecked():
            self.sessionHandler.writeData()

        return False

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
            self.RememberMe()
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
    app.setStyle('Linux')
    widget.show()
    sys.exit(app.exec_())
