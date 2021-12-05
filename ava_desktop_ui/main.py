import random
import sys
import threading
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow
import FirebaseClientWrapper
import Sessionhandler
import audio_manager
import Model.user as user
from ava_desktop_ui.Model import tasks, TaskManager
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

        # Tasks Page

        # Tasks Navigation Buttons
        self.ui.btnBackToTasks.clicked.connect(self.backToTask)

        self.ui.btnCreateTask.clicked.connect(self.createTask)
        self.Ui_task_List = []
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
        taskObject: QtWidgets.QFrame = tasks.Task(self, "Demo", "Demo").createTaskComponent()
        TaskManager.TaskLists.addTask(taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_Demo"))
        print(taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_Demo").objectName())
        taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_Demo").clicked.connect(self.runTask)
        taskObject.findChild(QtWidgets.QPushButton, f"btnDelete_Demo").clicked.connect(self.deleteTask)
        self.ui.verticalLayout_4.addWidget(taskObject)
        taskJsonObj = {'name': "Demo", 'description': "Demo", 'runCounter': '0'}
        user.current_user.addTask(taskJsonObj)
        self.Ui_task_List.append(taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_Demo"))
        self.ui.stackPanel.setCurrentIndex(4)

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

    def backToTask(self):
        """
        Navigate to Tasks Page
        :return:
        """
        self.ui.stackPanel.setCurrentIndex(3)

    def movetoTask(self):
        """
        Navigate to Task Page
        :return: None
        """
        self.ui.stackPanel.setCurrentIndex(3)
        if not self.Ui_task_List:
            print(self.Ui_task_List)
            for item in user.current_user.task_list:
                taskObject: QtWidgets.QFrame = tasks.Task(self, item['name'], item['description']).createTaskComponent()
                TaskManager.TaskLists.addTask(taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}"))
                print(taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}").objectName())
                taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}").clicked.connect(self.runTask)
                taskObject.findChild(QtWidgets.QPushButton, f"btnDelete_{item['name']}").clicked.connect(self.deleteTask)
                self.ui.verticalLayout_4.addWidget(taskObject)
                self.Ui_task_List.append(taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}"))

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
