import json
import re
import sys
import threading
import time
import webbrowser
import os
import socket

import pynput.keyboard
from requests_oauthlib import OAuth2Session
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QMainWindow, QProxyStyle, QStyle
import progressbar
from ruamel import yaml
import FirebaseClientWrapper
import Sessionhandler
import audio_manager
import Models.user as user
from Models import tasks, TaskManager
from Models.TaskRunner import RunTask
from Models import Appfonts
from ava_desktop_ui.Models.tasks import CheckTasks, CreateTask
from task_listener import TaskListener
from ui import Ui_MainWindow
from pyupdater.client import Client, AppUpdate
import qtawesome as qta
import requests


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.client_token = ''
        # SET TITLE BAR
        self.ui.frame_title.mouseMoveEvent = self.moveWindow

        # Title Bar buttons
        self.ui.btnWindowMinimize.clicked.connect(self.minimizeWindow)
        self.ui.btnWindowClose.clicked.connect(self.closeWindow)
        self.ui.btnMenu.clicked.connect(self.openMenu)

        # Menu control
        self.isMenuOpen = None
        self.isMenuEnabled = False

        # Tasks UI controls
        self.Ui_task_List = []

        self.ui.txtTitle.textChanged.connect(self.titleChange)
        self.ui.txtDescription.textChanged.connect(self.descriptionChange)
        self.ui.btnTaskListener.clicked.connect(self.starTaskListener)
        self.taskListenerObject = None
        self.taskEntries = None
        self.isListener = False

        self.emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.passwordRegex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?)(&])[A-Za-z\d@$!#%*?)(&]{8,18}$"
        self.compliledRegex = re.compile(self.passwordRegex)

        # Login LineEdit listeners
        self.isEmailLogin = bool
        self.ui.txtEmail_login.textChanged.connect(self.validateEmail)
        self.isPassword = bool

        # Signup LineEdit listeners
        self.ui.txtEmail_signup.textChanged.connect(self.validateEmail)
        self.ui.txtPassword_signup.textChanged.connect(self.validatePassword)
        self.ui.txtConfirmPassword_signup.textChanged.connect(self.validatePasswords)
        self.isEmailSignup = bool
        self.isPasswordSignup = bool

        # SubMenu Buttons
        self.ui.btnLogout.clicked.connect(self.logout)
        self.ui.btnAccount.clicked.connect(self.openAccount)
        self.ui.btnFAQ.clicked.connect(self.movetoMicrophone)

        # Login Buttons
        self.ui.btnLoginPage.clicked.connect(self.movetoLogin)
        self.ui.btnSignupPage.clicked.connect(self.movetoSignup)

        # Login process
        self.ui.btnLogin.clicked.connect(self.user_login)

        # Signup process
        self.ui.btnSignup.clicked.connect(self.user_signup)

        # Social Logins
        self.ui.btnGoogle.clicked.connect(self.google_login_alternate)

        # Email verification page
        self.ui.btnContinue.clicked.connect(self.movetoTask)
        # If user remember me == True then login

        # Speech Recognition Screen
        self.ui.btnMicrophoneControl.clicked.connect(self.pausePlayMic)
        self.audioManager = audio_manager.AudioManager(self)

        # Microphone Boolean
        self.isMic = False

        # Tasks Navigation Buttons
        self.ui.btnBackToTasks.clicked.connect(self.backToTask)

        self.ui.btnCreateTask.clicked.connect(self.movetoCreateTask)
        self.is_persistent()
        # Show UI

        self.show()

    def openAccount(self):
        webbrowser.open("http://localhost:3000/dashboard")

    def validatePasswords(self):
        print(self.sender().text(), self.ui.txtPassword_signup.text())
        if self.sender().text() == self.ui.txtPassword_signup.text():
            self.isPasswordSignup = True
            self.sender().setStyleSheet("border-style: outset;\n"
                                        "border-width: 1px;\n"
                                        "background-color: rgb(231, 231, 231);\n"
                                        "border-radius: 8px;\n"
                                        "border-color: rgb(194,194,194);\n"
                                        "padding: 4px;")
            self.ui.lblError_signup.setText("")
        else:
            self.isPasswordSignup = False
            self.ui.lblError_signup.setText("Passwords do not match")
            self.sender().setStyleSheet("border: 2px solid;\n"
                                        "border-color: rgb(255, 148, 148);\n"
                                        "border-radius: 8px;\n")

    def validatePassword(self):
        print(self.sender().text())
        # result = re.fullmatch(self.passwordRegex, self.sender().text())
        result = re.search(self.compliledRegex, self.sender().text())
        if result:
            print("Valid")
            self.sender().setStyleSheet("border-style: outset;\n"
                                        "border-width: 1px;\n"
                                        "background-color: rgb(231, 231, 231);\n"
                                        "border-radius: 8px;\n"
                                        "border-color: rgb(194,194,194);\n"
                                        "padding: 4px;")
        else:
            print("Invalid")
            self.sender().setStyleSheet("border: 2px solid;\n"
                                        "border-color: rgb(255, 148, 148);\n"
                                        "border-radius: 8px;\n")

    def validateEmail(self):
        print(self.sender().objectName())

        if re.fullmatch(self.emailRegex, self.sender().text()):
            print("Valid Email")
            self.sender().setStyleSheet("border-style: outset;\n"
                                        "background-color: rgb(231, 231, 231);\n"
                                        "border-width: 1px;\n"
                                        "border-radius: 8px;\n"
                                        "border-color: rgb(194,194,194);\n"
                                        "padding: 4px;")
            if self.sender().objectName() == "txtEmail_login":
                self.isEmailLogin = True
            else:
                self.isEmailSignup = True
        else:
            self.isEmailLogin = False
            print("Invalid Email")
            self.sender().setStyleSheet("border-style: outset;\n"
                                        "border: 2px solid;\n"
                                        "background-color: rgb(231, 231, 231);\n"
                                        "border-radius: 8px;\n"
                                        "border-color: rgb(255, 148, 148);")

    def movetoMicrophone(self):
        # self.webView = WebView(self)
        # self.webView.setParent(self.ui.MainPage)
        # self.webView.setGeometry(QtCore.QRect(20, 300, 550, 100))
        # print(self.webView.mainWindow.objectName())
        self.ui.menu.lower()
        self.isMenuOpen = False
        # self.webView.show()
        # self.ui.stackPanel.setCurrentIndex(2)

    def titleChange(self):
        print(self.sender().text())
        if self.sender().text() is not None:
            self.ui.txtTitle.setStyleSheet("QLineEdit{\n"
                                           "border: none;\n"
                                           "background-color: #E7E7E7;\n"
                                           "border-radius: 13px;\n"
                                           "text-align: center;\n"
                                           "}")

    def descriptionChange(self):
        print(self.sender().text())
        if self.sender().text() is not None:
            self.ui.txtDescription.setStyleSheet("QLineEdit{\n"
                                                 "border: none;\n"
                                                 "background-color: #E7E7E7;\n"
                                                 "border-radius: 13px;\n"
                                                 "text-align: center;\n"
                                                 "}")

    def moveToMicrophone(self):
        if self.ui.stackPanel.currentIndex() == 2:
            self.ui.stackPanel.setCurrentIndex(3)
        else:
            self.ui.stackPanel.setCurrentIndex(2)

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

    def closeMenu(self):
        self.ui.menu.lower()

    def openMenu(self):
        if self.isMenuEnabled:
            if self.isMenuOpen:
                # Lower state
                print("Inside true")
                self.ui.menu.lower()
                self.isMenuOpen = False
            else:
                # Raise state
                self.ui.menu.raise_()
                self.isMenuOpen = True
                print("User is ", user.current_user.isVerified, user.current_user.isVerified)

                if user.current_user.isVerified == "False" and self.ui.verticalLayout.findChild(QtWidgets.QPushButton,
                                                                                                "btnEmailverification"):
                    self.btnEmailverification = QtWidgets.QPushButton(self.ui.verticalLayoutWidget)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.btnEmailverification.sizePolicy().hasHeightForWidth())
                    self.btnEmailverification.setSizePolicy(sizePolicy)
                    self.btnEmailverification.setFocusPolicy(QtCore.Qt.NoFocus)
                    self.btnEmailverification.setMinimumSize(QtCore.QSize(0, 60))
                    self.btnEmailverification.setFont(Appfonts.appFonts.getMenuButtonFont())
                    self.btnEmailverification.setStyleSheet("QPushButton{\n"
                                                            "text-align: left center;\n"
                                                            "padding: 0 0 0 20;\n"
                                                            "color: rgb(63, 61, 86);\n"
                                                            "background-color: rgb(255, 255, 255);\n"
                                                            "border-bottom: 1px solid rgb(63, 61, 86);\n"
                                                            "\n"
                                                            "}")
                    iconAccount = QtGui.QIcon(qta.icon('fa5s.exclamation', color='#3e3c54'))
                    self.btnEmailverification.setIcon(iconAccount)
                    self.btnEmailverification.setIconSize(QtCore.QSize(32, 32))
                    self.btnEmailverification.setObjectName("btnEmailverification")
                    self.ui.verticalLayout.addWidget(self.btnEmailverification)
                    self.btnEmailverification.setText("Verify Email")
                    self.btnEmailverification.clicked.connect(self.movetoEmailVerification)
                    print(self.ui.verticalLayout.findChild(QtWidgets.QPushButton, "btnEmailverification"))

                else:
                    print("Removing Email button")
                    user.current_user.isVerified = "True"
                    Sessionhandler.sessionHandler.setUserData()
                    self.ui.verticalLayout.removeWidget(
                        self.ui.verticalLayout.findChild(QtWidgets.QPushButton, "btnEmailverification"))

    def starTaskListener(self):
        if not self.ui.txtTitle.text():
            print("Title Empty")
            self.ui.txtTitle.setStyleSheet("border: none;\n"
                                           "background-color: #E7E7E7;\n"
                                           "border-radius: 13px;\n"
                                           "text-align: center;\n"
                                           "border: 2px solid;\n"
                                           "border-color: rgb(255, 148, 148);}")
        elif not self.ui.txtDescription.text():
            print("Description Empty")
            self.ui.txtDescription.setStyleSheet("border: none;\n"
                                                 "background-color: #E7E7E7;\n"
                                                 "border-radius: 13px;\n"
                                                 "text-align: center;\n"
                                                 "border: 2px solid;\n"
                                                 "border-color: rgb(255, 148, 148);}")
        else:
            if self.isListener:
                # Set the icon to stop
                print("startStatus: ", self.isListener)
                print("Setting icon to stop.")
                icon4 = QtGui.QIcon(qta.icon('fa5s.stop', color='white'))
                self.ui.btnTaskListener.setIcon(icon4)
                self.ui.btnTaskListener.setIconSize(QSize(32, 32))
                self.ui.lblStartStopRec.setText(
                    "Click here to STOP recording task")
                self.isListener = False
                print("Task Object: ", self.taskListenerObject.break_program)
                if self.taskListenerObject is not None:
                    print("Exiting taskListeners")
                    self.taskListenerObject.setExit()

                    if self.taskListenerObject.taskEntries is not None and self.taskListenerObject.break_program:
                        self.taskEntries = self.taskListenerObject.taskEntries
                        print("Task Entries from: ", self.taskEntries)
                        self.createTask()
            elif not self.isListener:
                # Set the icon to play Start Listeners
                print("Set the icon to play")
                print("startStatus: (else) ", self.isListener)

                self.startThread()
                self.isListener = True

    def startThread(self):
        self.TaskListenerThread = threading.Thread(
            target=self.executeListenerThread)
        self.TaskListenerThread.start()
        self.TaskListenerThread.join()
        if self.taskEntries is not None:
            self.createTask()

    def executeListenerThread(self):
        print("Setting Pause Icon")
        self.taskListenerObject = TaskListener(self.ui.txtTitle.text(), self)

        self.taskEntries = self.taskListenerObject.startListeners()
        print("From startListener", self.taskEntries)
        if self.taskEntries is not None:
            self.ui.lblStartStopRec.setText(
                "Click here to STOP recording task")
            icon4 = QtGui.QIcon(qta.icon('fa5s.play', color='#3e3c54'))
            self.ui.btnTaskListener.setIcon(icon4)
            self.ui.btnTaskListener.setIconSize(QSize(32, 32))
            self.ui.btnTaskListener.setStyleSheet("QPushButton{\n"
                                                  "background-color: rgb(62, 60, 84);\n"
                                                  "border: 1px solid white;\n"
                                                  "border-radius: 40;\n"
                                                  "}\n"
                                                  "QPushButton:pressed{\n"
                                                  "    background-color: rgb(103, 100, 138);\n"
                                                  "}")
            self.taskListenerObject = None

    def createTask(self):
        title = self.ui.txtTitle.text()
        description = self.ui.txtDescription.text()
        print("title: ", title)
        print("description: ", description)

        if title and description:
            self.taskObject = tasks.CreateTask(self, title, description).createTask()
            TaskManager.TaskLists.addTask(self.taskObject.findChild(
                QtWidgets.QPushButton, f"btnRuntask_{title}"))
            print(self.taskObject.objectName())
            self.taskObject.findChild(
                QtWidgets.QPushButton, f"btnRuntask_{title}").clicked.connect(self.runTask)
            self.taskObject.findChild(
                QtWidgets.QPushButton, f"btnDelete_{title}").clicked.connect(self.deleteTask)
            self.ui.verticalLayout_2.addWidget(self.taskObject)
            print("Task added to UI")
            taskJsonObj = {'name': title,
                           'description': description, 'runCounter': '0'}
            user.current_user.addTask(taskJsonObj)
            print(f"Task Entries for {title}", self.taskEntries[title])
            empty = False
            # Check if files are created
            yaml.allow_duplicate_keys = True
            taskData = yaml.load(open("application/config/task_bindings.yml", "r"), Loader=yaml.SafeLoader)

            def getList(dict):
                return [*dict]

            new_dict = {}

            if taskData is not None:
                for item in getList(taskData):
                    print(item)
                    new_dict.update({item: item})

            # with open('application/config/task_bindings.yml', 'a', encoding="utf-8") as yamlfile:
            #     print(f"Adding {self.taskEntries} to yaml file")
            #     yaml.dump(self.taskEntries, yamlfile)

            self.taskEntries = None
            # if empty:
            #     print("Writing task to file")
            #     with open("application/config/task_bindings.yml", 'w+', encoding="utf-8") as yamlfile:
            #         yaml.dump(self.taskEntries, yamlfile, Dumper=ruamel.yaml.SafeDumper)
            # else:
            #     print("Appending task to file")
            #     with open('application/config/task_bindings.yml', 'a', encoding="utf-8") as yamlfile:
            #         yaml.dump(self.taskEntries, yamlfile, Dumper=ruamel.yaml.SafeDumper)

            self.Ui_task_List.append(self.taskObject.findChild(
                QtWidgets.QPushButton, f"btnRuntask_{title}"))
            self.taskObject = None
            self.ui.stackPanel.setCurrentIndex(2)
            self.ui.txtTitle.setText("")
            self.ui.txtDescription.setText("")
            print("Removing Empty Label", self.ui.TasksPage.findChild(
                QtWidgets.QLabel, "emptyTasksLabel"))
            self.ui.verticalLayout_2.removeWidget(
                self.ui.TasksPage.findChild(QtWidgets.QLabel, "emptyTasksLabel"))

        if not title:
            print("Title Empty")
            self.ui.txtTitle.setStyleSheet("border: 2px solid;\n"
                                           "border-color: rgb(255, 148, 148);")

        if not description:
            print("Description Empty")
            self.ui.txtDescription.setStyleSheet("border: none;\n"
                                                 "background-color: #E7E7E7;\n"
                                                 "border-radius: 13px;\n"
                                                 "text-align: center;\n"
                                                 "border: 2px solid;\n"
                                                 "border-color: rgb(255, 148, 148);}")

    def deleteTask(self):
        print("Delete task called")
        print(str(self.sender().objectName()).replace("btnDelete_", ""))
        user.current_user.deleteTask(
            str(self.sender().objectName()).replace("btnDelete_", ""))
        self.ui.verticalLayout_2.removeWidget(self.sender().parentWidget())
        print("User task list: ", user.current_user.task_list)
        if not user.current_user.task_list:
            emptyTasksLabel = QtWidgets.QLabel()
            emptyTasksLabel.setGeometry(QtCore.QRect(110, 55, 251, 71))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(27)
            font.setBold(True)
            font.setWeight(75)
            emptyTasksLabel.setFont(font)
            emptyTasksLabel.setStyleSheet("color:rgb(63, 61, 84)")
            emptyTasksLabel.setAlignment(QtCore.Qt.AlignCenter)
            emptyTasksLabel.setObjectName("emptyTasksLabel")
            addTaskPng = QPixmap('Icons/add note.png')
            emptyTasksLabel.setPixmap(addTaskPng)
            self.ui.verticalLayout_2.addWidget(emptyTasksLabel)
            print("Empty Label Added")

    def taskListener(self):
        import task_listener
        task_listener.TaskListener("demo")

    def pausePlayMic(self):
        """
        Change the icon and background based on the state of the microphone
        Calls to the microphone manager class will be made from here.
        """
        if self.audioManager.isClosed is False:
            icon4 = QtGui.QIcon(qta.icon('fa5s.stop', color='#3e3c54'))
            self.ui.btnTaskListener.setIcon(icon4)
            self.ui.btnTaskListener.setIconSize(QSize(32, 32))
            self.ui.btnTaskListener.setStyleSheet("QPushButton{\n"
                                                  "background-color: rgb(255, 255, 255);\n"
                                                  "border: 1px solid white;\n"
                                                  "border-radius: 40;\n"
                                                  "}\n"
                                                  "QPushButton:pressed{\n"
                                                  "    background-color: rgb(103, 100, 138);\n"
                                                  "}")
            if self.audioManager is None:
                # Checkbox for continuous transcription
                audio_manager.audioManger = audio_manager.AudioManager(self)

                # Else simple one time audio transcription

            t1 = threading.Thread(target=self.audioManager.start)
            t1.start()
            self.audioManager.isClosed = True
        else:
            self.ui.lblStartStopRec.setText(
                "Click here to STOP recording task")
            icon4 = QtGui.QIcon(qta.icon('fa5s.play', color='#3e3c54'))
            self.ui.btnTaskListener.setIcon(icon4)
            self.ui.btnTaskListener.setIconSize(QSize(32, 32))
            self.ui.btnTaskListener.setStyleSheet("QPushButton{\n"
                                                  "background-color: rgb(62, 60, 84);\n"
                                                  "border: 1px solid white;\n"
                                                  "border-radius: 40;\n"
                                                  "}\n"
                                                  "QPushButton:pressed{\n"
                                                  "    background-color: rgb(103, 100, 138);\n"
                                                  "}")
            t1 = threading.Thread(target=self.audioManager.stop)
            t1.start()
            audio_manager.audioManger = None
            self.audioManager.isClosed = False

    def is_persistent(self):
        """
        Check if user is already logged in or not

        :return: None
        """
        result = Sessionhandler.sessionHandler.readloginstate()
        self.ui.stackPanel.setCurrentIndex(5)
        print("Result from readLoginstate() is:- ", result)
        if result is not False and result is not None:
            self.isMenuEnabled = True
            user.current_user.email = result["email"]
            user.current_user.uid = result["uid"]
            user.current_user.idtoken = result["idtoken"]
            print("From is_persistent() ", user.current_user.email)
            if result['loginstate']:
                if result['isverified']:
                    refreshAuthThread = threading.Thread(target=self.refreshToken)
                    # refreshAuthThread.start()
                    print("Print UID", user.current_user.uid)
                    self.isMenuEnabled = True
                    self.checkTasks()
                    print("Moved to task")
                else:
                    # Move to Email Verification Page
                    print("False")
                    self.movetoEmailVerification()
                    pass
        try:
            if result['idtoken'] == "None":
                print("Result is ", result)
        except Exception as error:
            print(error)
            self.ui.loginLoadingFrame.lower()
            self.ui.stackPanel.setCurrentIndex(0)

    def refreshToken(self):
        while True:
            FirebaseClientWrapper.Firebase_app.updateAuthToken()
            time.sleep(10)

    def checkTasks(self):
        self.chkTasks = CheckTasks(self)
        self.chkTasks.tasks.connect(self.addTasks)
        self.chkTasks.start()

    def addTasks(self, data):
        """
        Adds tasks if found or else adds "No task svg"

        :param data: Object (Task Name and Description)
        :return: None
        """
        print("Task found in addTasks", data)
        print(data)
        try:
            if data['label']:
                emptyTasksLabel = QtWidgets.QLabel()
                emptyTasksLabel.setGeometry(QtCore.QRect(110, 55, 251, 71))
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                font.setPointSize(27)
                font.setBold(True)
                font.setWeight(75)
                emptyTasksLabel.setFont(font)
                emptyTasksLabel.setStyleSheet("color:rgb(63, 61, 84)")
                emptyTasksLabel.setAlignment(QtCore.Qt.AlignCenter)
                emptyTasksLabel.setObjectName("emptyTasksLabel")
                addTaskPng = QPixmap('Icons/add note.png')
                emptyTasksLabel.setPixmap(addTaskPng)
                self.ui.verticalLayout_2.addWidget(emptyTasksLabel)
                self.ui.stackPanel.setCurrentIndex(2)

        except Exception as e:
            self.ui.stackPanel.setCurrentIndex(2)
            taskObject = CreateTask(self, data['name'], data['description']).createTask()
            taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{data['name']}").clicked.connect(
                self.runTask)
            taskObject.findChild(QtWidgets.QPushButton, f"btnDelete_{data['name']}").clicked.connect(
                self.deleteTask)
            self.ui.verticalLayout_2.addWidget(taskObject)

    def logout(self):

        FirebaseClientWrapper.Firebase_app.logout()
        print(self.Ui_task_List)
        try:
            for item in self.Ui_task_List:
                print("Deleting Tasks Nodes in UI")
                self.ui.verticalLayout_2.removeWidget(
                    self.ui.TasksPage.findChild(QtWidgets.QFrame, item.parent().objectName()))
        except Exception as e:
            print(e)
        user.current_user.logout()
        self.ui.stackPanel.setCurrentIndex(0)
        self.isMenuEnabled = False
        self.ui.menu.lower()
        self.ui.loginLoadingFrame.lower()

    def movetoEmailVerification(self):
        FirebaseClientWrapper.Firebase_app.send_email_verification()
        self.ui.stackPanel.setCurrentIndex(4)
        # count = 0
        # while count < 5:
        #     time.sleep(2.5)
        #
        #     r = requests.get(
        #         f"https://us-central1-ava-daemon.cloudfunctions.net/app/verify?uid={user.current_user.uid}")
        #     print(r.text)
        #     if r.text == "Verfied":
        #         print("True")
        #         self.movetoTask()
        #         break
        # self.movetoTask()
        # self.ui.stackPanel.setCurrentIndex(4)
        # self.ui.emailwebView.show()
        # FirebaseClientWrapper.Firebase_app.send_email_verification()
        # isVerifiedThread = threading.Thread(target=self.check_if_verified)
        # isVerifiedThread.start()

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

                result = FirebaseClientWrapper.Firebase_app.signup_new_user(self.ui.txtEmail_signup.text(),
                                                                            self.ui.txtPassword_signup.text(),
                                                                            False)
                print("Signup Result: ", result)
                if result is True:
                    # self.ui.frame.raise_()
                    self.RememberMe()
                    if self.isUser():
                        self.isMenuEnabled = True
                        # Move to Email Verification Page

                        self.movetoEmailVerification()
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

    def google_login_alternate(self):
        import uuid
        token = str(uuid.uuid4().hex)
        req = webbrowser.open(f"http://localhost:3000/googlelogin?id={token}")
        print(token)
        FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(token).set({
            "login": "False"
        })

        def stream_handler(data):
            print("Data:", data['data'])
            print("Data:", type(data['data']))
            try:
                print("Data:", data['data']['login'])
                if data['data']['login'] == 'True':
                    user.current_user.email = data['data']['email']
                    user.current_user.auth_token = data['data']['authtoken']
                    user.current_user.isVerified = 'True'
                    user.current_user.uid = data['data']['uid']
                    Sessionhandler.sessionHandler.setUserData()
                    Sessionhandler.sessionHandler.setloginstate()
                    self.checkTasks()
                    FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").child(token).remove()
                    my_stream.close()
            except KeyError as e:
                print(e)

        my_stream = FirebaseClientWrapper.Firebase_app.database.child("users_authenticated").stream(stream_handler)

    def google_login(self):
        try:
            client_id = "41961847947-sqpmjbbl0qnt5o3hf9hrhsem85hcd71l.apps.googleusercontent.com"
            client_secret = "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"
            redirect_uri = 'http://127.0.0.1:3000'

            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
            # OAuth endpoints given in the Google API documentation
            authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
            token_url = "https://www.googleapis.com/oauth2/v4/token"
            scope = [
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ]

            google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

            # Redirect user to Google for authorization
            authorization_url, state = google.authorization_url(authorization_base_url,
                                                                # offline for refresh token
                                                                # force to always make user click authorize
                                                                access_type="offline", prompt="select_account")
            print('Please go here and authorize:', authorization_url)
            webbrowser.open(authorization_url)

            HOST = '127.0.0.1'
            PORT = 3000
            redirect_response = ""

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:

                    while True:
                        print('Connected by', addr)
                        data = conn.recv(1024)
                        print(data.split())
                        if not data:
                            continue
                        else:
                            redirect_response = str(data.split()[1])
                            break

            # Fetch the access token
            print("Redirect response: ", redirect_response)
            google.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=redirect_response)

            # Fetch a protected resource, i.e. user profile
            r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
            print(r.content)
            profile = json.loads(r.content)
            print(profile)
            tokenResult = requests.get(f"https://us-central1-ava-daemon.cloudfunctions.net/app/gettoken")
            tokenResult = tokenResult.json()
            userObject = FirebaseClientWrapper.Firebase_app.auth.sign_in_with_custom_token(
                tokenResult["customToken"])
            tokenResult = requests.get(f"https://us-central1-ava-daemon.cloudfunctions.net/app/gettoken")
            tokenResult = tokenResult.json()
            userFromToken = FirebaseClientWrapper.Firebase_app.auth.sign_in_with_custom_token(
                tokenResult["customToken"])
            try:
                user.current_user.uid = tokenResult["uid"]
                user.current_user.email = profile["email"]
                user.current_user.isVerified = "true"
                user.current_user.auth_token = userObject["idToken"]
                Sessionhandler.sessionHandler.setUserData()
                # Sessionhandler.sessionHandler.setloginstate()
            except Exception as e:
                print(e)
            print("User object after signup: ", userFromToken, userFromToken)
            # user.current_user.uid = profile[""]
            # self.movetoTask()
        except Exception as e:
            print(e)

    def wait_forloginstate(self):
        # self.ui.frame.raise_()
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
                    # self.ui.frame.lower()
            except Exception as e:
                print(e)
        # self.ui.frame.lower()

    def user_login(self):
        """
        Takes the data from text fields entered by user and logs in the user if credentials are correct else show
        relevant errors.
        """

        email = self.ui.txtEmail_login.text()
        pwd = self.ui.txtPassword_login.text()
        print("Email = ", email, pwd)
        print(f"PWD= {bool(pwd)}")
        self.ui.btnLogin.setCursor(Qt.ForbiddenCursor)
        self.ui.btnLogin.setEnabled(False)
        self.ui.loginLoadingFrame.raise_()
        if pwd and email:

            # self.ui.waitingSpinner.start()
            # Persist login credentials pending

            if self.ui.chkRememberme.isChecked():
                result = FirebaseClientWrapper.Firebase_app.login_email_password(
                    email, pwd, True)

                self.RememberMe()
                print("Remember me")
            else:
                result = FirebaseClientWrapper.Firebase_app.login_email_password(
                    email, pwd, False)
            if result is True:
                # Navigate to home page
                if self.isUser():
                    self.ui.txtEmail_login.setText('')
                    self.ui.txtPassword_login.setText('')
                    self.isMenuEnabled = True
                    self.ui.btnLogin.setCursor(Qt.ArrowCursor)
                    self.ui.btnLogin.setEnabled(True)
                    self.ui.loginLoadingFrame.lower()
                    self.movetoTask()
                    # self.ui.frame.lower()
            else:
                # Set the error message for the user
                print(result)

                self.ui.btnLogin.setCursor(Qt.ArrowCursor)
                self.ui.btnLogin.setEnabled(True)
                self.ui.lblError_login.setText(result)
        else:
            print('Else part')
            self.ui.btnLogin.setCursor(Qt.ArrowCursor)
            self.ui.btnLogin.setEnabled(True)
            self.ui.loginLoadingFrame.lower()
            self.ui.lblError_login.setText(
                "Email and Password fields cannot be empty.")

    def backToTask(self):
        """
        Navigate to Tasks Page
        :return:
        """
        self.ui.stackPanel.setCurrentIndex(2)

    def movetoCreateTask(self):
        self.ui.stackPanel.setCurrentIndex(3)

    def movetoTask(self):
        """
        Navigate to Task Page
        :return: None
        """
        print("Inside movetoTask()")
        print(f"""
Task list: {user.current_user.task_list}
Empty label: {self.ui.TasksPage.findChild(QtWidgets.QLabel, "emptyTasksLabel")}
        """)
        self.ui.stackPanel.setCurrentIndex(2)
        if not user.current_user.task_list and self.ui.TasksPage.findChild(
                QtWidgets.QLabel, "emptyTasksLabel") is None:
            print("Else Part")
            emptyTasksLabel = QtWidgets.QLabel()
            emptyTasksLabel.setGeometry(QtCore.QRect(110, 55, 251, 71))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(27)
            font.setBold(True)
            font.setWeight(75)
            emptyTasksLabel.setFont(font)
            emptyTasksLabel.setStyleSheet("color:rgb(63, 61, 84)")
            emptyTasksLabel.setAlignment(QtCore.Qt.AlignCenter)
            emptyTasksLabel.setObjectName("emptyTasksLabel")
            addTaskPng = QPixmap('Icons/add note.png')
            emptyTasksLabel.setPixmap(addTaskPng)
            self.ui.verticalLayout_2.addWidget(emptyTasksLabel)

            print("Label", self.ui.TasksPage.findChild(
                QtWidgets.QLabel, "emptyTasksLabel"))
        else:
            try:
                for item in user.current_user.task_list:
                    self.taskObject: QtWidgets.QFrame = tasks.CreateTask(self, item['name'],
                                                                         item['description']).createTask()
                    TaskManager.TaskLists.addTask(
                        self.taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}"))
                    self.taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}").clicked.connect(
                        self.runTask)
                    self.taskObject.findChild(QtWidgets.QPushButton, f"btnDelete_{item['name']}").clicked.connect(
                        self.deleteTask)
                    self.ui.verticalLayout_2.addWidget(self.taskObject)
                    self.Ui_task_List.append(self.taskObject.findChild(
                        QtWidgets.QPushButton, f"btnRuntask_{item['name']}"))
                    self.taskObject = None
                    print(f"""
                    {self.ui.verticalLayout_2.findChild(QtWidgets.QFrame, "mainTaskFrame_Demo")}
Layout Children: {self.ui.verticalLayout_2.children()}
Tasks UI list: {self.Ui_task_List}
                    """)
            except Exception as error:
                print(error)

    def _executeThread(self):
        runTaskObject = RunTask(self.RuntimeTaskName)
        print("Running Task")
        runTaskObject.enumerateData()

    def runTask(self, event):
        self.showMinimized()
        print("Task Running:", self.sender().objectName())
        self.RuntimeTaskName = self.sender().objectName().split('_')[1]
        t1 = threading.Thread(target=self._executeThread)
        t1.start()
        t1.join()

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


class Style(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget):
        if element == QStyle.PE_FrameFocusRect:
            return
        super().drawPrimitive(element, option, painter, widget)


def RunApp(arg):
    app = QtWidgets.QApplication(arg)
    dir_ = QtCore.QDir("Poppins")
    _poppinsBold = QtGui.QFontDatabase.addApplicationFont(
        "application/fonts/Poppins-Bold.ttf")
    _poppinsLight = QtGui.QFontDatabase.addApplicationFont(
        "application/fonts/Poppins-Light.ttf")
    _poppinsExtraLight = QtGui.QFontDatabase.addApplicationFont(
        "application/fonts/Poppins-ExtraLight.ttf")
    _poppinsSemiBold = QtGui.QFontDatabase.addApplicationFont(
        "application/fonts/Poppins-SemiBold.ttf")
    # app.setStyle(Style())
    window = MainWindow()
    sys.exit(app.exec_())


class ClientConfig(object):
    PUBLIC_KEY = 'hEh3Jy6i61sNH42U4LGwRrggIQKd6CcqfGg1E8tOGPE'
    APP_NAME = 'Ava'
    APP_VERSION = "0.0.4"
    APP_CHANNEL = "stable"
    COMPANY_NAME = 'Daemon Technologies'
    HTTP_TIMEOUT = 30
    MAX_DOWNLOAD_RETRIES = 3
    UPDATE_URLS = ['https://ava-desktop-deploy.s3.ap-south-1.amazonaws.com/ava-deploy-app/windows/deploy/']


bar = None


def check_for_update():
    def print_status_info(info):
        total = info.get(u'total')
        downloaded = info.get(u'downloaded')
        status = info.get(u'status')
        print(downloaded, total, status)

    def cb(status):
        global bar

        if bar is None:
            bar = progressbar.ProgressBar(
                widgets=[progressbar.Percentage(), progressbar.Bar()], fd=sys.stdout).start()
        zz = float(status['percent_complete'])

        bar.update(zz)

    # sys.stdout = open(os.devnull, 'w')

    client = Client(ClientConfig(), refresh=True)

    client.platform = "win"
    app_update = client.update_check(
        ClientConfig.APP_NAME, ClientConfig.APP_VERSION, channel='stable')
    if app_update is not None:
        app_update.progress_hooks.append(cb)
        app_update.progress_hooks.append(print_status_info)
        if app_update.download():
            if isinstance(app_update, AppUpdate):
                app_update.extract_restart()
                RunApp(sys.argv)
                return True
            else:
                app_update.extract()
                return True
    return False


if __name__ == "__main__":
    print(sys.argv)
    print(f"Running on {ClientConfig.APP_CHANNEL} channel")
    print(f"App version: {ClientConfig.APP_VERSION}")

    print("Checking for Updates please wait!")
    # print("Updates are disabled for now! :(")
    # RunApp(sys.argv)
    if check_for_update():
        print('there\'s a new update :D')
    else:
        print("Running on latest version: ", ClientConfig.APP_VERSION)
        RunApp(sys.argv)
