import random
import sys
import threading
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow
from pyqt5_plugins.examplebuttonplugin import QtGui

import FirebaseClientWrapper
import Sessionhandler
import audio_manager
import Model.user as user
from ava_desktop_ui.demo import RunTask
from main_ui import Ui_main


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        # self.MircophoneManager = AudioManager()
        self.client_token = ''
        # SET TITLE BAR
        self.ui.frame_title.mouseMoveEvent = self.moveWindow

        # Title Bar buttons
        self.ui.btnWindowMinimize.clicked.connect(self.minimizeWindow)
        self.ui.btnWindowClose.clicked.connect(self.closeWindow)
        self.ui.btnMenu.clicked.connect(self.openMenu)
        self.isMenuOpen = None
        self.isMenuEnabled = False
        self.ui.SubMenuFrame.lower()

        # SubMenu Buttons
        self.ui.btnLogout.clicked.connect(self.logout)
        self.ui.btnSettings.clicked.connect(self.movetoTask)
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

        # Speech Recognition Screen
        self.ui.btnMicrophoneControl.clicked.connect(self.taskListener)
        self.audioManager = audio_manager.AudioManager(self)
        # Microphone Boolean
        self.isMic = False

        self.ui.btnCreateTask.clicked.connect(self.createTask)
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
                print(e)

    def minimizeWindow(self):
        self.showMinimized()

    def closeWindow(self):
        QtCore.QCoreApplication.instance().quit()

    def openMenu(self):
        if self.isMenuEnabled:
            if self.isMenuOpen:
                # Raise state
                print("Inside true")
                self.ui.SubMenuFrame.lower()
                self.isMenuOpen = False
            else:
                # Lower state
                print("Inside false")
                self.ui.SubMenuFrame.raise_()
                self.isMenuOpen = True

    def createTask(self):
        print("Called createTask")
        self.ui.stackPanel.setCurrentIndex(4)
    #     globals()["mainTaskFrame_" + self.taskId] = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
    #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(globals()["mainTaskFrame_" + self.taskId].sizePolicy().hasHeightForWidth())
    #     globals()["mainTaskFrame_" + self.taskId].setSizePolicy(sizePolicy)
    #     globals()["mainTaskFrame_" + self.taskId].setMinimumSize(QtCore.QSize(450, 100))
    #     globals()["mainTaskFrame_" + self.taskId].setMaximumSize(QtCore.QSize(450, 100))
    #     globals()["mainTaskFrame_" + self.taskId].setStyleSheet("border: 1px solid;\n"
    #                                "border-color: rgb(138, 139, 152);\n"
    #                                "border-top-right-radius: 12px;\n"
    #                                "border-bottom-right-radius: 12px;\n"
    #                                "box-shadow: 1px 2px rgba(0, 0, 0, 16);")
    #     globals()["mainTaskFrame_" + self.taskId].setFrameShape(QtWidgets.QFrame.StyledPanel)
    #     globals()["mainTaskFrame_" + self.taskId].setFrameShadow(QtWidgets.QFrame.Raised)
    #     globals()["mainTaskFrame_" + self.taskId].setObjectName("frame_2")
    #     self.frame_8 = QtWidgets.QFrame(globals()["mainTaskFrame_" + self.taskId])
    #     self.frame_8.setGeometry(QtCore.QRect(0, 0, 6, 100))
    #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
    #     self.frame_8.setSizePolicy(sizePolicy)
    #     self.frame_8.setStyleSheet("background-color: rgb(138, 139, 152);\n"
    #                                "border-left: 0px;\n"
    #                                "border-top-right-radius: 0px;\n"
    #                                "border-bottom-right-radius: 0px;")
    #     self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
    #     self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
    #     self.frame_8.setObjectName("frame_8")
    #     globals()["btnDelete_" + self.taskId] = QtWidgets.QPushButton(globals()["mainTaskFrame_" + self.taskId])
    #     globals()["btnDelete_" + self.taskId].setGeometry(QtCore.QRect(425, 4, 20, 20))
    #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(globals()["btnDelete_" + self.taskId].sizePolicy().hasHeightForWidth())
    #     globals()["btnDelete_" + self.taskId].setSizePolicy(sizePolicy)
    #     globals()["btnDelete_" + self.taskId].setStyleSheet("QPushButton{\n"
    #                                                         "border: none;\n"
    #                                                         "border-radius: 10px;\n"
    #                                                         "}\n"
    #                                                         "")
    #     globals()["btnDelete_" + self.taskId].setText("")
    #     icon3 = QtGui.QIcon()
    #     icon3.addPixmap(QtGui.QPixmap("Icons/Delete Task Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #     globals()["btnDelete_" + self.taskId].setIcon(icon3)
    #     globals()["btnDelete_" + self.taskId].setIconSize(QtCore.QSize(12, 12))
    #     globals()["btnDelete_" + self.taskId].setObjectName(f"btnDelete_{self.taskId}")
    #     globals()["btnDelete_" + self.taskId].clicked.connect(self.deleteTask)
    #     globals()["btnRuntask_" + self.taskId] = QtWidgets.QPushButton(globals()["mainTaskFrame_" + self.taskId])
    #     globals()["btnRuntask_" + self.taskId].setGeometry(QtCore.QRect(400, 4, 20, 20))
    #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(globals()["btnRuntask_" + self.taskId].sizePolicy().hasHeightForWidth())
    #     globals()["btnRuntask_" + self.taskId].setSizePolicy(sizePolicy)
    #     globals()["btnRuntask_" + self.taskId].setStyleSheet("QPushButton{\n"
    #                                                          "border: none;\n"
    #                                                          "border-radius: 10px;\n"
    #                                                          "}\n"
    #                                                          "")
    #     globals()["btnRuntask_" + self.taskId].setText("")
    #     icon4 = QtGui.QIcon()
    #     icon4.addPixmap(QtGui.QPixmap("Icons/Run Task Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #     globals()["btnRuntask_" + self.taskId].setIcon(icon4)
    #     globals()["btnRuntask_" + self.taskId].setIconSize(QtCore.QSize(12, 12))
    #     globals()["btnRuntask_" + self.taskId].setObjectName(f"btnRuntask_{self.taskId}")
    #     globals()["btnRuntask_" + self.taskId].clicked.connect(self.runTask)
    #     globals()["frame_7_" + self.taskId] = QtWidgets.QFrame(globals()["mainTaskFrame_" + self.taskId])
    #     globals()["frame_7_" + self.taskId].setGeometry(QtCore.QRect(10, 10, 381, 81))
    #     globals()["frame_7_" + self.taskId].setStyleSheet("border:none;")
    #     globals()["frame_7_" + self.taskId].setFrameShape(QtWidgets.QFrame.StyledPanel)
    #     globals()["frame_7_" + self.taskId].setFrameShadow(QtWidgets.QFrame.Raised)
    #     globals()["frame_7_" + self.taskId].setObjectName("frame_7")
    #     globals()["frame_6_" + self.taskId] = QtWidgets.QLabel(globals()["frame_7_" + self.taskId])
    #     globals()["frame_6_" + self.taskId].setGeometry(QtCore.QRect(10, 0, 370, 30))
    #     font = QtGui.QFont()
    #     font.setFamily("Sitka Banner Semibold")
    #     font.setPointSize(16)
    #     font.setBold(True)
    #     font.setWeight(75)
    #     globals()["frame_6_" + self.taskId].setFont(font)
    #     globals()["frame_6_" + self.taskId].setObjectName("label_6")
    #     self.label_7 = QtWidgets.QLabel(globals()["frame_7_" + self.taskId])
    #     self.label_7.setGeometry(QtCore.QRect(9, 29, 371, 41))
    #     font = QtGui.QFont()
    #     font.setFamily("Sitka Banner Semibold")
    #     font.setPointSize(10)
    #     font.setBold(True)
    #     font.setWeight(75)
    #     self.label_7.setFont(font)
    #     self.label_7.setObjectName("label_7")
    #     self.ui.verticalLayout_4.addWidget(globals()["mainTaskFrame_" + self.taskId])

    def deleteTask(self):
        print("Delete task called")
        print(self.sender().parent().objectName())

    def taskListener(self):
        import task_listener
        task_listener.TaskListener("demo")

    def pausePlayMic(self):
        """
        Change the icon and background based on the state of the microphone
        Calls to the microphone manager class will be made from here.
        """
        if self.audioManager.isClosed is False:
            self.ui.btnMicrophoneControl.setIcon(QIcon("Icons/Pause@2x.png"))
            self.ui.btnMicrophoneControl.setIconSize(QSize(64, 64))
            self.ui.btnMicrophoneControl.setStyleSheet("""
            background-color: white;
            border: none;
            """)
            if self.audioManager is None:
                # Checkbox for continuous transcription
                audio_manager.audioManger = audio_manager.AudioManager(self)

                # Else simple one time audio transcription

            t1 = threading.Thread(target=self.audioManager.start)
            t1.start()
            self.audioManager.isClosed = True
        else:
            self.ui.btnMicrophoneControl.setIconSize(QSize(32, 32))
            self.ui.btnMicrophoneControl.setIcon(QIcon("Icons/Icon ionic-ios-mic.png"))
            self.ui.btnMicrophoneControl.setStyleSheet("""
            background-color: rgb(62, 60, 84);
            border: 1px solid white;
            border-radius: 40;
            """)
            t1 = threading.Thread(target=self.audioManager.stop)
            t1.start()
            audio_manager.audioManger = None
            self.audioManager.isClosed = False

    def is_persistent(self):

        try:
            result = Sessionhandler.sessionHandler.readloginstate()
            print("Result from readLoginstate() is:- ", result)
            if result is not False and result is not None:
                self.ui.stackPanel.setCurrentIndex(2)
                self.isMenuEnabled = True
                user.current_user.email = result["email"]
                user.current_user.uid = result["uid"]
                user.current_user.idtoken = result["idtoken"]
                print("From is_persistent() ", user.current_user.email)
                if result['loginstate']:
                    user.current_user.getTasks()
                    print(user.current_user.uid)
                    self.isMenuEnabled = True
                    self.ui.stackPanel.setCurrentIndex(2)
                    self.ui.frame.lower()
            try:
                if result['idtoken'] == "None":
                    print("Result is ", result)
            except Exception as error:
                print(error)
                self.ui.stackPanel.setCurrentIndex(0)

        except Exception as e:
            self.isMenuEnabled = False
            print("No user found as ", e)
            self.ui.stackPanel.setCurrentIndex(0)

    def logout(self):
        FirebaseClientWrapper.Firebase_app.logout()
        self.ui.stackPanel.setCurrentIndex(0)
        self.isMenuEnabled = False
        self.ui.SubMenuFrame.lower()

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
                self.ui.frame.raise_()
                result = FirebaseClientWrapper.Firebase_app.signup_new_user(self.ui.txtEmail_signup.text(),
                                                                            self.ui.txtPassword_signup.text(),
                                                                            False)
                if result is True:
                    self.RememberMe()
                    if self.isUser():
                        self.isMenuEnabled = True
                        self.ui.frame.lower()
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
        Sessionhandler.sessionHandler.setUserData()
        Sessionhandler.sessionHandler.setloginstate()

    def isUser(self):
        return True if user.current_user.email is not None else False

    def google_login(self):
        # import secrets
        # web = PyQt5.QtWebEngineWidgets.QWebEngineView(self.ui.SettingsPage)
        # client_token = secrets.token_hex(32)
        # web.load(QUrl(f"http://localhost:3000/gauth/{client_token}"))
        # web.setGeometry(QtCore.QRect(30, 30, 421, 571))
        # web.show()

        self.ui.frame.raise_()
        import webbrowser
        import secrets

        self.client_token = secrets.token_hex(32)

        webbrowser.open(f"http://localhost:3000/gauth/{self.client_token}")
        user.current_user.idtoken = self.client_token
        print("Google Login idtoken=", user.current_user.idtoken)
        self.readLogin = threading.Thread(target=self.wait_forloginstate)
        self.readLogin.start()

    def wait_forloginstate(self):
        self.ui.frame.raise_()
        for i in range(5):
            try:
                time.sleep(2)
                result = FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(
                    self.client_token).get()
                print("From Google Login()")
                documentId = ""
                print(result.val())
                for key in result.val().keys():
                    documentId = key
                print('DocumentId=', documentId)
                if result.val()[documentId]['loginstate'] != "False":
                    print("Login Success")
                    self.isMenuEnabled = True
                    self.ui.stackPanel.setCurrentIndex(2)
                    user.current_user.idtoken = self.client_token
                    user.current_user.email = result.val()[documentId]['email']
                    user.current_user.uid = documentId
                    Sessionhandler.sessionHandler.setUserData()
                    self.ui.frame.lower()
            except Exception as e:
                print(e)
        self.ui.frame.lower()

    def user_login(self):
        """
        Takes the data from text fields entered by user and logs in the user if credentials are correct else show
        relevant errors.
        """

        email = self.ui.txtEmail_login.text()
        pwd = self.ui.txtPassword_login.text()
        print("Email = ", email, pwd)
        print(f"PWD= {bool(pwd)}")

        if pwd and email:

            self.ui.waitingSpinner.start()
            # Persist login credentials pending

            if self.ui.chkRememberme.isChecked():
                result = FirebaseClientWrapper.Firebase_app.login_email_password(email, pwd, True)

                self.RememberMe()
                print("Remember me")
            else:
                result = FirebaseClientWrapper.Firebase_app.login_email_password(email, pwd, False)
            if result is True:
                # Navigate to home page

                if self.isUser():
                    self.isMenuEnabled = True
                    self.ui.stackPanel.setCurrentIndex(2)
                    self.ui.frame.lower()
            else:
                # Set the error message for the user
                print(result)
                self.ui.lblError_login.setText(result)
        else:
            print('Else part')
            self.ui.lblError_login.setText("Email and Password fields cannot be empty.")

    def movetoTask(self):
        """
        Navigate to Task Page
        :return: None
        """
        self.Ui_task_List = []
        for item in user.current_user.task_list:
            self.taskId = str(item['name'])
            globals()["mainTaskFrame_" + self.taskId] = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(globals()["mainTaskFrame_" + self.taskId].sizePolicy().hasHeightForWidth())
            globals()["mainTaskFrame_" + self.taskId].setSizePolicy(sizePolicy)
            globals()["mainTaskFrame_" + self.taskId].setMinimumSize(QtCore.QSize(450, 100))
            globals()["mainTaskFrame_" + self.taskId].setMaximumSize(QtCore.QSize(450, 100))
            globals()["mainTaskFrame_" + self.taskId].setStyleSheet("border: 1px solid;\n"
                                                                    "border-color: rgb(138, 139, 152);\n"
                                                                    "border-top-right-radius: 12px;\n"
                                                                    "border-bottom-right-radius: 12px;\n"
                                                                    "box-shadow: 1px 2px rgba(0, 0, 0, 16);")
            globals()["mainTaskFrame_" + self.taskId].setFrameShape(QtWidgets.QFrame.StyledPanel)
            globals()["mainTaskFrame_" + self.taskId].setFrameShadow(QtWidgets.QFrame.Raised)
            globals()["mainTaskFrame_" + self.taskId].setObjectName("mainTaskFrame_" + self.taskId)
            self.frame_8 = QtWidgets.QFrame(globals()["mainTaskFrame_" + self.taskId])
            self.frame_8.setGeometry(QtCore.QRect(0, 0, 6, 100))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
            self.frame_8.setSizePolicy(sizePolicy)
            self.frame_8.setStyleSheet("background-color: rgb(138, 139, 152);\n"
                                       "border-left: 0px;\n"
                                       "border-top-right-radius: 0px;\n"
                                       "border-bottom-right-radius: 0px;")
            self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_8.setObjectName("frame_8")
            globals()["btnDelete_" + self.taskId] = QtWidgets.QPushButton(globals()["mainTaskFrame_" + self.taskId])
            globals()["btnDelete_" + self.taskId].setGeometry(QtCore.QRect(425, 4, 20, 20))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(globals()["btnDelete_" + self.taskId].sizePolicy().hasHeightForWidth())
            globals()["btnDelete_" + self.taskId].setSizePolicy(sizePolicy)
            globals()["btnDelete_" + self.taskId].setStyleSheet("QPushButton{\n"
                                                                "border: none;\n"
                                                                "border-radius: 10px;\n"
                                                                "}\n"
                                                                "")
            globals()["btnDelete_" + self.taskId].setText("")
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap("Icons/Delete Task Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            globals()["btnDelete_" + self.taskId].setIcon(icon3)
            globals()["btnDelete_" + self.taskId].setIconSize(QtCore.QSize(12, 12))
            globals()["btnDelete_" + self.taskId].setObjectName(f"btnDelete_{self.taskId}")
            globals()["btnDelete_" + self.taskId].clicked.connect(self.deleteTask)
            globals()["btnRuntask_" + self.taskId] = QtWidgets.QPushButton(globals()["mainTaskFrame_" + self.taskId])
            globals()["btnRuntask_" + self.taskId].setGeometry(QtCore.QRect(400, 4, 20, 20))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(globals()["btnRuntask_" + self.taskId].sizePolicy().hasHeightForWidth())
            globals()["btnRuntask_" + self.taskId].setSizePolicy(sizePolicy)
            globals()["btnRuntask_" + self.taskId].setStyleSheet("QPushButton{\n"
                                                                 "border: none;\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}\n"
                                                                 "")
            globals()["btnRuntask_" + self.taskId].setText("")
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap("Icons/Run Task Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            globals()["btnRuntask_" + self.taskId].setIcon(icon4)
            globals()["btnRuntask_" + self.taskId].setIconSize(QtCore.QSize(12, 12))
            globals()["btnRuntask_" + self.taskId].setObjectName(f"btnRuntask_{self.taskId}")
            globals()["btnRuntask_" + self.taskId].clicked.connect(self.runTask)
            globals()["frame_7_" + self.taskId] = QtWidgets.QFrame(globals()["mainTaskFrame_" + self.taskId])
            globals()["frame_7_" + self.taskId].setGeometry(QtCore.QRect(10, 10, 381, 81))
            globals()["frame_7_" + self.taskId].setStyleSheet("border:none;")
            globals()["frame_7_" + self.taskId].setFrameShape(QtWidgets.QFrame.StyledPanel)
            globals()["frame_7_" + self.taskId].setFrameShadow(QtWidgets.QFrame.Raised)
            globals()["frame_7_" + self.taskId].setObjectName("frame_7")
            globals()["frame_6_" + self.taskId] = QtWidgets.QLabel(globals()["frame_7_" + self.taskId])
            globals()["frame_6_" + self.taskId].setGeometry(QtCore.QRect(10, 0, 370, 30))
            font = QtGui.QFont()
            font.setFamily("Sitka Banner Semibold")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            globals()["frame_6_" + self.taskId].setFont(font)
            globals()["frame_6_" + self.taskId].setObjectName("label_6")
            print(globals()["frame_6_" + self.taskId])

            self.label_7 = QtWidgets.QLabel(globals()["frame_7_" + self.taskId])
            self.label_7.setGeometry(QtCore.QRect(9, 29, 371, 41))
            font = QtGui.QFont()
            font.setFamily("Sitka Banner Semibold")
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_7.setFont(font)
            self.label_7.setObjectName("label_7")
            self.ui.verticalLayout_4.addWidget(globals()["mainTaskFrame_" + self.taskId])
            self.translate = QtCore.QCoreApplication.translate
            globals()["frame_6_" + self.taskId].setText(self.translate("main", item['name']))
            self.label_7.setText(self.translate("main", item['description']))
            # tasks.Task(self, item['name'], item['description'])
            # print(self.ui.scrollAreaWidgetContents.children())
            # print("Item", item['name'])
        self.ui.stackPanel.setCurrentIndex(3)

        self.ui.SubMenuFrame.lower()
        self.isMenuOpen = False

    def _executeThread(self):
        runTaskObject = RunTask(self.RuntimeTaskName)
        print("Running Task")
        runTaskObject.enumerateData()

    def runTask(self, event):
        print("Task Running:", self.sender().objectName())
        self.RuntimeTaskName = self.sender().objectName().split('_')[1]
        # print(globals()["frame_6_OpenYoutube"])
        # print(globals()["frame_6_OpenYoutube"].parentWidget().parentWidget().objectName())
        t1 = threading.Thread(target=self._executeThread)
        t1.start()

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
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(63, 61, 84))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, QColor(63, 61, 84))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(63, 61, 84))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyle("Oxygen")
    window = MainWindow()
    sys.exit(app.exec_())
