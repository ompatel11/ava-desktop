import random
import time
from PyQt5 import QtCore, QtWidgets, QtGui
import yaml
from yaml import SafeLoader


class Task:
    def __init__(self, mainParent, taskHeading: str, taskDescription: str):
        self.taskDescription = taskDescription
        self.taskFrameColor = ["#A6A8BF", "#8A8B98", "#2F3041", "#A4A5AF", "#292838", "#44434d", "#282736"]
        self.currentColor = random.choice(self.taskFrameColor)
        print("Current Color: ", self.currentColor)
        self.taskName = taskHeading
        self.parent = mainParent
        self.taskId = taskHeading
        self.translate = QtCore.QCoreApplication.translate

    def createTaskComponent(self):
        globals()["mainTaskFrame_" + self.taskId] = QtWidgets.QFrame(self.parent.ui.scrollAreaWidgetContents)
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
        self.frame_8.setStyleSheet(f"background-color: {self.currentColor};\n"
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

        self.label_7 = QtWidgets.QLabel(globals()["frame_7_" + self.taskId])
        self.label_7.setGeometry(QtCore.QRect(9, 29, 371, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Banner Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        globals()["frame_6_" + self.taskId].setText(self.translate("main", self.taskName))
        self.label_7.setText(self.translate("main", self.taskDescription))
        return globals()["mainTaskFrame_" + self.taskId]

    def fetch_tasks(self):
        # Open the file and load the file
        with open("application/config/task_bindings.yml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            # print(data[self.taskName].clear())
            del data[self.taskName]
            self.tasks = data
            print(self.tasks)
            time.sleep(5)

        return self.tasks
