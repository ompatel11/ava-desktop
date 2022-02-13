import random
import time
from PyQt5 import QtCore, QtWidgets, QtGui
import yaml
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from yaml import SafeLoader
import qtawesome as qta

from . import user
from .Appfonts import appFonts
from .TaskManager import TaskManager


class CreateTask:
    def __init__(self, mainParent, taskHeading: str, taskDescription: str):
        self.taskDescription = taskDescription
        self.taskFrameColor = ["#A6A8BF", "#8A8B98", "#2F3041", "#A4A5AF", "#292838", "#44434d", "#282736"]
        self.currentColor = random.choice(self.taskFrameColor)
        print("Current Color: ", self.currentColor)
        self.taskName = taskHeading
        self.parent = mainParent
        self.taskId = taskHeading
        self.translate = QtCore.QCoreApplication.translate

    def createTask(self):
        globals()["mainTaskFrame_" + self.taskId] = QtWidgets.QFrame(self.parent.ui.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(globals()["mainTaskFrame_" + self.taskId].sizePolicy().hasHeightForWidth())
        globals()["mainTaskFrame_" + self.taskId].setSizePolicy(sizePolicy)
        globals()["mainTaskFrame_" + self.taskId].setMinimumSize(QtCore.QSize(480, 150))
        globals()["mainTaskFrame_" + self.taskId].setStyleSheet("background-color: rgb(231, 231, 231);\n"
                                                                "border-radius: 12px;")
        globals()["mainTaskFrame_" + self.taskId].setFrameShape(QtWidgets.QFrame.StyledPanel)
        globals()["mainTaskFrame_" + self.taskId].setFrameShadow(QtWidgets.QFrame.Raised)
        globals()["mainTaskFrame_" + self.taskId].setObjectName(f"mainTaskFrame_{self.taskId}")
        globals()["btnRuntask_" + self.taskId] = QtWidgets.QPushButton(globals()["mainTaskFrame_" + self.taskId])
        globals()["btnRuntask_" + self.taskId].setFocusPolicy(QtCore.Qt.NoFocus)
        print("Mainframe name: ", globals()["mainTaskFrame_" + self.taskId].objectName())
        globals()["btnRuntask_" + self.taskId].setGeometry(QtCore.QRect(350, 40, 80, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(globals()["btnRuntask_" + self.taskId].sizePolicy().hasHeightForWidth())
        globals()["btnRuntask_" + self.taskId].setSizePolicy(sizePolicy)
        globals()["btnRuntask_" + self.taskId].setMaximumSize(QtCore.QSize(100, 100))
        globals()["btnRuntask_" + self.taskId].setStyleSheet("QPushButton{\n"
                                                             "background-color: rgb(62, 60, 84);\n"
                                                             "border: 1px solid white;\n"
                                                             "border-radius: 40;\n"
                                                             "}\n"
                                                             "QPushButton:pressed{\n"
                                                             "    background-color: rgb(103, 100, 138);\n"
                                                             "}")
        globals()["btnRuntask_" + self.taskId].setText("")
        icon5 = QtGui.QIcon(qta.icon('fa5s.play', color='white'))
        globals()["btnRuntask_" + self.taskId].setIcon(icon5)
        globals()["btnRuntask_" + self.taskId].setIconSize(QtCore.QSize(32, 32))
        globals()["btnRuntask_" + self.taskId].setObjectName(f"btnRuntask_{self.taskName}")
        self.lbltaskTitle = QtWidgets.QLabel(globals()["mainTaskFrame_" + self.taskId])
        self.lbltaskTitle.setGeometry(QtCore.QRect(20, 10, 300, 40))
        self.lbltaskTitle.setFont(appFonts.getTaskTitleFont())
        self.lbltaskTitle.setStyleSheet("color: #3F3D56;")
        self.lbltaskTitle.setObjectName("taskTitle")
        self.lbltaskDescription = QtWidgets.QLabel(globals()["mainTaskFrame_" + self.taskId])
        self.lbltaskDescription.setGeometry(QtCore.QRect(20, 60, 321, 90))
        self.lbltaskDescription.setFont(appFonts.getTaskDescriptionFont())
        self.lbltaskDescription.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.lbltaskDescription.setAlignment(QtCore.Qt.AlignTop)
        self.lbltaskDescription.setWordWrap(True)
        self.lbltaskDescription.setStyleSheet("color: #3F3D56;")
        self.lbltaskDescription.setObjectName("lbltaskDescription")
        globals()["btnDelete_" + self.taskId] = QtWidgets.QPushButton(globals()["mainTaskFrame_" + self.taskId])
        globals()["btnDelete_" + self.taskId].setFocusPolicy(QtCore.Qt.NoFocus)
        globals()["btnDelete_" + self.taskId].setGeometry(QtCore.QRect(455, 5, 21, 21))
        globals()["btnDelete_" + self.taskId].setText("")
        icon6 = QtGui.QIcon(qta.icon('fa5s.times', color='#707070'))
        globals()["btnDelete_" + self.taskId].setIcon(icon6)
        globals()["btnDelete_" + self.taskId].setObjectName(f"btnDelete_{self.taskName}")
        self.lbltaskTitle.setText(self.translate("MainWindow", self.taskName))
        self.lbltaskDescription.setText(self.translate("MainWindow", self.taskDescription))
        return globals()["mainTaskFrame_" + self.taskId]

    def fetch_tasks(self):
        # Open the file and load the file
        with open("../application/config/task_bindings.yml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            # print(data[self.taskName].clear())
            del data[self.taskName]
            self.tasks = data
            print(self.tasks)
            time.sleep(5)

        return self.tasks


class CheckTasks(QtCore.QThread):
    tasks = QtCore.pyqtSignal(dict)

    def __init__(self, parent, taskList=None):
        QtCore.QThread.__init__(self, parent)
        if taskList is None:
            taskList = []
        self.parent = parent
        self.taskList = taskList
        print("Initialized")

    @pyqtSlot()
    def run(self):
        print("Running: ", self.taskList)
        self.taskList = user.current_user.task_list
        # time.sleep(random.randrange(2, 5))
        # time.sleep(3)
        if not self.taskList:
            self.tasks.emit({'label': True})
        for item in self.taskList:
            print("Task found")
            taskObject = CreateTask(self.parent, item['name'],
                                                      item['description']).createTask()

            print(type(taskObject))
            self.parent.ui.verticalLayout_2.addWidget(taskObject)
            taskObject = {'name': item['name'], 'description': item['description']}
            self.tasks.emit(taskObject)
