import sys
import threading
import time
import ruamel.yaml
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QProxyStyle, QStyle
import progressbar
from ruamel import yaml
import FirebaseClientWrapper
import Sessionhandler
import audio_manager
import Models.user as user
from Models import tasks, TaskManager
from Models.TaskRunner import RunTask
from task_listener import TaskListener
from ui import Ui_MainWindow
from pyupdater.client import Client, AppUpdate
import qtawesome as qta


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
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
        # self.ui.SubMenuFrame_2.lower()

        # Tasks UI controls
        self.Ui_task_List = []
        # self.ui.btnAddTask.clicked.connect(self.createTask)
        self.ui.txtTitle.textChanged.connect(self.titleChange)
        self.ui.txtDescription.textChanged.connect(self.descriptionChange)
        self.ui.btnTaskListener.clicked.connect(self.starTaskListener)
        self.taskListenerObject = None
        self.taskEntries = None
        self.isListener = False
        # SubMenu Buttons
        self.ui.btnLogout.clicked.connect(self.logout)

        # Login Buttons
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
        self.ui.btnMicrophoneControl.clicked.connect(self.pausePlayMic)
        self.audioManager = audio_manager.AudioManager(self)

        # Microphone Boolean
        self.isMic = False

        # Tasks Navigation Buttons
        self.ui.btnBackToTasks.clicked.connect(self.backToTask)

        self.ui.btnCreateTask.clicked.connect(self.movetoCreateTask)

        # Show UI
        self.show()

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
                print("Inside false")
                self.ui.menu.raise_()
                self.isMenuOpen = True

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
                if self.taskListenerObject is not None:
                    print("Exiting taskListeners")
                    self.taskListenerObject.setExit()
                    if self.taskListenerObject.taskEntries is not None:
                        self.taskEntries = self.taskListenerObject.taskEntries
                        print("Task Entries from: ", self.taskEntries)
                        self.createTask()
            else:
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
            self.taskObject = tasks.Task(self, title, description).createTask()
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
            print(self.taskEntries)
            empty = False
            # Check if files are created
            with open("application/config/task_bindings.yml", 'w+') as fp:
                data = yaml.load_all(fp, Loader=ruamel.yaml.Loader)
                print("DATA:", data)
                if data is None:
                    print("Empty yaml file")
                    empty = True
            if empty:
                print("Writing task to file")
                with open("application/config/task_bindings.yml", 'w+', encoding="utf-8") as yamlfile:
                    yaml.dump_all(self.taskEntries, yamlfile,
                              Dumper=yaml.RoundTripDumper, default_flow_style=False)
            else:
                print("Appending task to file")
                with open('application/config/task_bindings.yml', 'a', encoding="utf-8") as yamlfile:
                    yaml.dump(self.taskEntries, yamlfile,
                              Dumper=yaml.RoundTripDumper, default_flow_style=False)

            self.Ui_task_List.append(self.taskObject.findChild(
                QtWidgets.QPushButton, f"btnRuntask_{title}"))
            self.taskObject = None
            self.ui.stackPanel.setCurrentIndex(3)
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
                print("Print UID", user.current_user.uid)
                self.isMenuEnabled = True
                # self.ui.stackPanel.setCurrentIndex(2)
                self.movetoTask()
                # self.ui.frame.lower()
        try:
            if result['idtoken'] == "None":
                print("Result is ", result)
        except Exception as error:
            print(error)
            self.ui.stackPanel.setCurrentIndex(0)
        # try:
        #     result = Sessionhandler.sessionHandler.readloginstate()
        #     print("Result from readLoginstate() is:- ", result)
        #     if result is not False and result is not None:
        #         self.ui.stackPanel.setCurrentIndex(2)
        #         self.isMenuEnabled = True
        #         user.current_user.email = result["email"]
        #         user.current_user.uid = result["uid"]
        #         user.current_user.idtoken = result["idtoken"]
        #         print("From is_persistent() ", user.current_user.email)
        #         if result['loginstate']:
        #             user.current_user.getTasks()
        #             print("Print UID", user.current_user.uid)
        #             self.isMenuEnabled = True
        #             # self.ui.stackPanel.setCurrentIndex(2)
        #             self.movetoTask()
        #             self.ui.frame.lower()
        #     try:
        #         if result['idtoken'] == "None":
        #             print("Result is ", result)
        #     except Exception as error:
        #         print(error)
        #         self.ui.stackPanel.setCurrentIndex(0)
        #
        # except Exception as e:
        #     self.isMenuEnabled = False
        #     print("No user found as ", e)
        #     self.ui.stackPanel.setCurrentIndex(0)

    def logout(self):
        FirebaseClientWrapper.Firebase_app.logout()
        for item in self.Ui_task_List:
            print("Deleting Tasks Nodes in UI")
            print(item.parent().objectName())
            self.ui.verticalLayout_2.removeWidget(
                self.ui.TasksPage.findChild(QtWidgets.QFrame, item.parent().objectName()))

        user.current_user.logout()
        self.ui.stackPanel.setCurrentIndex(0)
        self.isMenuEnabled = False
        self.ui.menu.lower()

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
                        # self.ui.frame.lower()
                        self.movetoTask()

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

        # self.ui.frame.raise_()
        import webbrowser
        import secrets

        self.client_token = secrets.token_hex(32)

        webbrowser.open(f"http://localhost:3000/gauth/{self.client_token}")
        user.current_user.idtoken = self.client_token
        print("Google Login idtoken=", user.current_user.idtoken)
        self.readLogin = threading.Thread(target=self.wait_forloginstate)
        self.readLogin.start()

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
                    self.ui.stackPanel.setCurrentIndex(3)
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
                    self.isMenuEnabled = True
                    self.movetoTask()
                    # self.ui.frame.lower()
            else:
                # Set the error message for the user
                print(result)
                self.ui.lblError_login.setText(result)
        else:
            print('Else part')
            self.ui.lblError_login.setText(
                "Email and Password fields cannot be empty.")

    def backToTask(self):
        """
        Navigate to Tasks Page
        :return:
        """
        self.ui.stackPanel.setCurrentIndex(3)

    def movetoCreateTask(self):
        self.ui.stackPanel.setCurrentIndex(4)

    def movetoTask(self):
        """
        Navigate to Task Page
        :return: None
        """
        self.ui.stackPanel.setCurrentIndex(3)

        if not user.current_user.task_list:
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
            print("Layout children: ", self.ui.TasksPage.children())
        else:

            for item in user.current_user.task_list:
                self.taskObject: QtWidgets.QFrame = tasks.Task(self, item['name'],
                                                               item['description']).createTask()
                TaskManager.TaskLists.addTask(
                    self.taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}"))
                print(self.taskObject.findChild(QtWidgets.QPushButton,
                      f"btnRuntask_{item['name']}").objectName())
                self.taskObject.findChild(QtWidgets.QPushButton, f"btnRuntask_{item['name']}").clicked.connect(
                    self.runTask)
                self.taskObject.findChild(QtWidgets.QPushButton, f"btnDelete_{item['name']}").clicked.connect(
                    self.deleteTask)
                self.ui.verticalLayout_2.addWidget(self.taskObject)
                self.Ui_task_List.append(self.taskObject.findChild(
                    QtWidgets.QPushButton, f"btnRuntask_{item['name']}"))

        self.ui.menu.lower()
        self.isMenuOpen = False

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
    # app.setStyle(Style())
    window = MainWindow()
    sys.exit(app.exec_())


class ClientConfig(object):
    PUBLIC_KEY = 'hEh3Jy6i61sNH42U4LGwRrggIQKd6CcqfGg1E8tOGPE'
    APP_NAME = 'Ava'
    APP_CHANNEL = 'stable'
    APP_VERSION = "0.1.2"
    COMPANY_NAME = 'Daemon Tech'
    HTTP_TIMEOUT = 30
    MAX_DOWNLOAD_RETRIES = 3
    UPDATE_URLS = ['http://localhost:80']


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

    client = Client(ClientConfig(), refresh=True,
                    headers={'basic_auth': 'brofewfefwefewef:EKAXsWkdt5H6yJEmtexN'})

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
    RunApp(sys.argv)
    # if check_for_update():
    #     print('there\'s a new update :D')
    # else:
    #     print("Running on latest version: ", ClientConfig.APP_VERSION)
    #     RunApp(sys.argv)
