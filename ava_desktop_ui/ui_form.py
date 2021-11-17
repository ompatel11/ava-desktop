# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from widgets.QtWaitingSpinner import QtWaitingSpinner


class Ui_main(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        MainWindow.setEnabled(True)
        MainWindow.resize(500, 689)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.central_frame = QtWidgets.QFrame(MainWindow)
        self.central_frame.setGeometry(QtCore.QRect(180, 300, 500, 500))
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.central_frame.sizePolicy().hasHeightForWidth())
        # self.central_frame.sizePolicy(sizePolicy)
        self.central_frame.setObjectName("central_frame")
        self.central_frame.raise_()
        spinner = QtWaitingSpinner(self.central_frame)
        self.stackPanel = QtWidgets.QStackedWidget(MainWindow)
        self.stackPanel.setGeometry(QtCore.QRect(10, 50, 471, 621))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.stackPanel.setFont(font)
        self.stackPanel.setStyleSheet("border:none\n"
                                      "")
        self.stackPanel.setObjectName("stackPanel")
        self.LoginPage = QtWidgets.QWidget()
        self.LoginPage.setObjectName("LoginPage")
        self.txtEmail_login = QtWidgets.QLineEdit(self.LoginPage)
        self.txtEmail_login.setGeometry(QtCore.QRect(81, 270, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(10)
        self.txtEmail_login.setFont(font)
        self.txtEmail_login.setStyleSheet("border-style: outset;\n"
                                          "border-width: 1px;\n"
                                          "background-color: rgb(231, 231, 231);\n"
                                          "border-radius: 8px;\n"
                                          "border-color: rgb(194,194,194);\n"
                                          "padding: 4px;")
        self.txtEmail_login.setText("")
        self.txtEmail_login.setObjectName("txtEmail_login")
        self.label_3 = QtWidgets.QLabel(self.LoginPage)
        self.label_3.setGeometry(QtCore.QRect(110, 20, 251, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:rgb(63, 61, 84)")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.btnFacebook = QtWidgets.QPushButton(self.LoginPage)
        self.btnFacebook.setGeometry(QtCore.QRect(154, 110, 55, 50))
        self.btnFacebook.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnFacebook.setAutoFillBackground(False)
        self.btnFacebook.setStyleSheet("color: #333;\n"
                                       "border: 0px solid  rgb(231, 231, 231);\n"
                                       "background-color: rgb(231, 231, 231);\n"
                                       "border-radius: 12px;\n"
                                       "color:rgb(240, 240, 240)")
        self.btnFacebook.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icons/icons8-facebook-circled-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFacebook.setIcon(icon)
        self.btnFacebook.setIconSize(QtCore.QSize(32, 32))
        self.btnFacebook.setFlat(False)
        self.btnFacebook.setObjectName("btnFacebook")
        self.chkRememberme = QtWidgets.QCheckBox(self.LoginPage)
        self.chkRememberme.setGeometry(QtCore.QRect(90, 410, 111, 19))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.chkRememberme.setFont(font)
        self.chkRememberme.setStyleSheet("color: rgb(124, 122, 133);")
        self.chkRememberme.setObjectName("chkRememberme")
        self.label_4 = QtWidgets.QLabel(self.LoginPage)
        self.label_4.setGeometry(QtCore.QRect(180, 180, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(194, 194, 194);\n"
                                   "padding-bottom: 4px;\n"
                                   "font-weight: 600;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.txtPassword_login = QtWidgets.QLineEdit(self.LoginPage)
        self.txtPassword_login.setGeometry(QtCore.QRect(81, 360, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(10)
        self.txtPassword_login.setFont(font)
        self.txtPassword_login.setStyleSheet("border-style: outset;\n"
                                             "border-width: 1px;\n"
                                             "background-color: rgb(231, 231, 231);\n"
                                             "border-radius: 8px;\n"
                                             "border-color: rgb(194,194,194);\n"
                                             "padding: 4px;")
        self.txtPassword_login.setText("")
        self.txtPassword_login.setObjectName("txtPassword_login")
        self.btnForgotpwd = QtWidgets.QPushButton(self.LoginPage)
        self.btnForgotpwd.setGeometry(QtCore.QRect(280, 410, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnForgotpwd.setFont(font)
        self.btnForgotpwd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnForgotpwd.setStyleSheet("color: rgb(63, 61, 84);\n"
                                        "border: 0px;\n"
                                        "background-color: rgb(255, 255, 255);")
        self.btnForgotpwd.setObjectName("btnForgotpwd")
        self.lblEmail_2 = QtWidgets.QLabel(self.LoginPage)
        self.lblEmail_2.setGeometry(QtCore.QRect(81, 242, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblEmail_2.setFont(font)
        self.lblEmail_2.setStyleSheet("color: rgb(63, 61, 85);")
        self.lblEmail_2.setObjectName("lblEmail_2")
        self.lblPassword_2 = QtWidgets.QLabel(self.LoginPage)
        self.lblPassword_2.setGeometry(QtCore.QRect(81, 320, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblPassword_2.setFont(font)
        self.lblPassword_2.setStyleSheet("color: rgb(63, 61, 85);")
        self.lblPassword_2.setObjectName("lblPassword_2")
        self.btnLogin = QtWidgets.QPushButton(self.LoginPage)
        self.btnLogin.setGeometry(QtCore.QRect(80, 450, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnLogin.setFont(font)
        self.btnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnLogin.setAutoFillBackground(False)
        self.btnLogin.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(63, 61, 84);\n"
                                    "border: 2px solid  rgb(63, 61, 94);\n"
                                    "border-radius: 8px;\n"
                                    "padding: 4px;\n"
                                    "box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);\n"
                                    "")
        self.btnLogin.setAutoDefault(False)
        self.btnLogin.setDefault(False)
        self.btnLogin.setFlat(True)
        self.btnLogin.setObjectName("btnLogin")
        self.btnGoogle = QtWidgets.QPushButton(self.LoginPage)
        self.btnGoogle.setGeometry(QtCore.QRect(254, 110, 55, 50))
        self.btnGoogle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGoogle.setAutoFillBackground(False)
        self.btnGoogle.setStyleSheet("color: #333;\n"
                                     "border: 0px solid  rgb(231, 231, 231);\n"
                                     "background-color: rgb(231, 231, 231);\n"
                                     "border-radius: 12px;\n"
                                     "color:rgb(240, 240, 240)")
        self.btnGoogle.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icons/icons8-google-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnGoogle.setIcon(icon1)
        self.btnGoogle.setIconSize(QtCore.QSize(32, 32))
        self.btnGoogle.setObjectName("btnGoogle")
        self.label_10 = QtWidgets.QLabel(self.LoginPage)
        self.label_10.setGeometry(QtCore.QRect(140, 500, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(124, 122, 133);")
        self.label_10.setObjectName("label_10")
        self.btnSignupPage = QtWidgets.QPushButton(self.LoginPage)
        self.btnSignupPage.setGeometry(QtCore.QRect(280, 505, 50, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnSignupPage.setFont(font)
        self.btnSignupPage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSignupPage.setStyleSheet("color: rgb(63, 61, 84);\n"
                                         "border: 0px;\n"
                                         "background-color: rgb(255, 255, 255);")
        self.btnSignupPage.setCheckable(False)
        self.btnSignupPage.setAutoExclusive(False)
        self.btnSignupPage.setDefault(False)
        self.btnSignupPage.setObjectName("btnSignupPage")
        self.frame_3 = QtWidgets.QFrame(self.LoginPage)
        self.frame_3.setGeometry(QtCore.QRect(50, 188, 120, 2))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 2))
        self.frame_3.setMaximumSize(QtCore.QSize(200, 2))
        self.frame_3.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_6 = QtWidgets.QFrame(self.LoginPage)
        self.frame_6.setGeometry(QtCore.QRect(301, 188, 120, 2))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 2))
        self.frame_6.setMaximumSize(QtCore.QSize(200, 2))
        self.frame_6.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.lblError_login = QtWidgets.QLabel(self.LoginPage)
        self.lblError_login.setGeometry(QtCore.QRect(80, 210, 310, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblError_login.setFont(font)
        self.lblError_login.setStyleSheet("QLabel{\n"
                                          "color: rgb(250,0,0);\n"
                                          "line-spacing: 2px;\n"
                                          "}")
        self.lblError_login.setText("")
        self.lblError_login.setObjectName("lblError_login")
        self.stackPanel.addWidget(self.LoginPage)
        self.SignupPage = QtWidgets.QWidget()
        self.SignupPage.setObjectName("SignupPage")
        self.label_2 = QtWidgets.QLabel(self.SignupPage)
        self.label_2.setGeometry(QtCore.QRect(180, 180, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(194, 194, 194);\n"
                                   "padding-bottom: 4px;\n"
                                   "font-weight: 600;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.txtEmail_signup = QtWidgets.QLineEdit(self.SignupPage)
        self.txtEmail_signup.setGeometry(QtCore.QRect(81, 270, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(10)
        self.txtEmail_signup.setFont(font)
        self.txtEmail_signup.setStyleSheet("border-style: outset;\n"
                                           "border-width: 1px;\n"
                                           "background-color: rgb(231, 231, 231);\n"
                                           "border-radius: 8px;\n"
                                           "border-color: rgb(194,194,194);\n"
                                           "padding: 4px;")
        self.txtEmail_signup.setText("")
        self.txtEmail_signup.setObjectName("txtEmail_signup")
        self.btnFacebook = QtWidgets.QPushButton(self.SignupPage)
        self.btnFacebook.setGeometry(QtCore.QRect(154, 110, 55, 50))
        self.btnFacebook.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnFacebook.setAutoFillBackground(False)
        self.btnFacebook.setStyleSheet("color: #333;\n"
                                       "border: 0px solid  rgb(231, 231, 231);\n"
                                       "background-color: rgb(231, 231, 231);\n"
                                       "border-radius: 12px;\n"
                                       "color:rgb(240, 240, 240)")
        self.btnFacebook.setText("")
        self.btnFacebook.setIcon(icon)
        self.btnFacebook.setIconSize(QtCore.QSize(32, 32))
        self.btnFacebook.setObjectName("btnFacebook")
        self.label = QtWidgets.QLabel(self.SignupPage)
        self.label.setGeometry(QtCore.QRect(110, 20, 251, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(63, 61, 84)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.txtPassword_signup = QtWidgets.QLineEdit(self.SignupPage)
        self.txtPassword_signup.setGeometry(QtCore.QRect(81, 360, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(10)
        self.txtPassword_signup.setFont(font)
        self.txtPassword_signup.setStyleSheet("border-style: outset;\n"
                                              "border-width: 1px;\n"
                                              "background-color: rgb(231, 231, 231);\n"
                                              "border-radius: 8px;\n"
                                              "border-color: rgb(194,194,194);\n"
                                              "padding: 4px;")
        self.txtPassword_signup.setText("")
        self.txtPassword_signup.setObjectName("txtPassword_signup")
        self.lblEmail = QtWidgets.QLabel(self.SignupPage)
        self.lblEmail.setGeometry(QtCore.QRect(81, 242, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblEmail.setFont(font)
        self.lblEmail.setStyleSheet("color: rgb(63, 61, 85);")
        self.lblEmail.setObjectName("lblEmail")
        self.lblPassword = QtWidgets.QLabel(self.SignupPage)
        self.lblPassword.setGeometry(QtCore.QRect(81, 320, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblPassword.setFont(font)
        self.lblPassword.setStyleSheet("color: rgb(63, 61, 85);")
        self.lblPassword.setObjectName("lblPassword")
        self.btnSignup = QtWidgets.QPushButton(self.SignupPage)
        self.btnSignup.setGeometry(QtCore.QRect(80, 515, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnSignup.setFont(font)
        self.btnSignup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSignup.setStyleSheet("QPushButton{\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "background-color: rgb(63, 61, 84);\n"
                                     "border: 2px solid  rgb(63, 61, 94);\n"
                                     "border-radius: 8px;\n"
                                     "padding: 4px;\n"
                                     "box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);\n"
                                     "}\n"
                                     "QPushButton:pressed{\n"
                                     "color: rgb(255, 30, 32);\n"
                                     "}")
        self.btnSignup.setObjectName("btnSignup")
        self.btnGoogle = QtWidgets.QPushButton(self.SignupPage)
        self.btnGoogle.setGeometry(QtCore.QRect(254, 110, 55, 50))
        self.btnGoogle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGoogle.setAutoFillBackground(False)
        self.btnGoogle.setStyleSheet("color: #333;\n"
                                     "border: 0px solid  rgb(231, 231, 231);\n"
                                     "background-color: rgb(231, 231, 231);\n"
                                     "border-radius: 12px;\n"
                                     "color:rgb(240, 240, 240)")
        self.btnGoogle.setText("")
        self.btnGoogle.setIcon(icon1)
        self.btnGoogle.setIconSize(QtCore.QSize(32, 32))
        self.btnGoogle.setObjectName("btnGoogle")
        self.label_9 = QtWidgets.QLabel(self.SignupPage)
        self.label_9.setGeometry(QtCore.QRect(140, 565, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(124, 122, 133);")
        self.label_9.setObjectName("label_9")
        self.btnLoginPage = QtWidgets.QPushButton(self.SignupPage)
        self.btnLoginPage.setGeometry(QtCore.QRect(290, 570, 40, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnLoginPage.setFont(font)
        self.btnLoginPage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnLoginPage.setStyleSheet("color: rgb(63, 61, 84);\n"
                                        "border: 0px;\n"
                                        "background-color: rgb(255, 255, 255);")
        self.btnLoginPage.setCheckable(False)
        self.btnLoginPage.setAutoExclusive(False)
        self.btnLoginPage.setDefault(False)
        self.btnLoginPage.setObjectName("btnLoginPage")
        self.frame_4 = QtWidgets.QFrame(self.SignupPage)
        self.frame_4.setGeometry(QtCore.QRect(301, 188, 120, 2))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 2))
        self.frame_4.setMaximumSize(QtCore.QSize(120, 2))
        self.frame_4.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.frame_5 = QtWidgets.QFrame(self.SignupPage)
        self.frame_5.setGeometry(QtCore.QRect(50, 188, 120, 2))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 2))
        self.frame_5.setMaximumSize(QtCore.QSize(120, 2))
        self.frame_5.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.lblPassword_3 = QtWidgets.QLabel(self.SignupPage)
        self.lblPassword_3.setGeometry(QtCore.QRect(81, 410, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblPassword_3.setFont(font)
        self.lblPassword_3.setStyleSheet("color: rgb(63, 61, 85);")
        self.lblPassword_3.setObjectName("lblPassword_3")
        self.txtConfirmPassword_signup = QtWidgets.QLineEdit(self.SignupPage)
        self.txtConfirmPassword_signup.setGeometry(QtCore.QRect(81, 450, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(10)
        self.txtConfirmPassword_signup.setFont(font)
        self.txtConfirmPassword_signup.setStyleSheet("border-style: outset;\n"
                                                     "border-width: 1px;\n"
                                                     "background-color: rgb(231, 231, 231);\n"
                                                     "border-radius: 8px;\n"
                                                     "border-color: rgb(194,194,194);\n"
                                                     "padding: 4px;")
        self.txtConfirmPassword_signup.setText("")
        self.txtConfirmPassword_signup.setObjectName("txtConfirmPassword_signup")
        self.lblError_signup = QtWidgets.QLabel(self.SignupPage)
        self.lblError_signup.setGeometry(QtCore.QRect(80, 210, 310, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblError_signup.setFont(font)
        self.lblError_signup.setStyleSheet("QLabel{\n"
                                           "color: rgb(250,0,0);\n"
                                           "line-spacing: 2px;\n"
                                           "}")
        self.lblError_signup.setText("")
        self.lblError_signup.setObjectName("lblError_signup")
        self.stackPanel.addWidget(self.SignupPage)
        self.MainPage = QtWidgets.QWidget()
        self.MainPage.setObjectName("MainPage")
        self.btnMicrophoneControl = QtWidgets.QPushButton(self.MainPage)
        self.btnMicrophoneControl.setGeometry(QtCore.QRect(196, 21, 80, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMicrophoneControl.sizePolicy().hasHeightForWidth())
        self.btnMicrophoneControl.setSizePolicy(sizePolicy)
        self.btnMicrophoneControl.setMaximumSize(QtCore.QSize(100, 100))
        self.btnMicrophoneControl.setStyleSheet("background-color: rgb(62, 60, 84);\n"
                                                "border: 1px solid white;\n"
                                                "border-radius: 40;")
        self.btnMicrophoneControl.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icons/Icon ionic-ios-mic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMicrophoneControl.setIcon(icon2)
        self.btnMicrophoneControl.setIconSize(QtCore.QSize(32, 32))
        self.btnMicrophoneControl.setObjectName("btnMicrophoneControl")
        self.label_5 = QtWidgets.QLabel(self.MainPage)
        self.label_5.setGeometry(QtCore.QRect(20, 150, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lblLiveTranscript = QtWidgets.QLabel(self.MainPage)
        self.lblLiveTranscript.setGeometry(QtCore.QRect(20, 190, 441, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.lblLiveTranscript.setFont(font)
        self.lblLiveTranscript.setStyleSheet("color:rgb(63, 61, 84);\n"
                                             "")
        self.lblLiveTranscript.setObjectName("lblLiveTranscript")
        self.stackPanel.addWidget(self.MainPage)
        self.SettingsPage = QtWidgets.QWidget()
        self.SettingsPage.setObjectName("SettingsPage")
        self.stackPanel.addWidget(self.SettingsPage)
        self.title_bar_2 = QtWidgets.QFrame(MainWindow)
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
        self.btnSettings.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icons/Icon ionic-ios-settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSettings.setIcon(icon3)
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
        self.btnWindowMinimize.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Icons/Icon awesome-window-minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnWindowMinimize.setIcon(icon4)
        self.btnWindowMinimize.setIconSize(QtCore.QSize(8, 8))
        self.btnWindowMinimize.setObjectName("btnWindowMinimize")
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
                                          "    \n"
                                          "    background-color: rgb(255, 0, 0);\n"
                                          "}")
        self.btnWindowClose.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Icons/Icon ionic-ios-close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnWindowClose.setIcon(icon5)
        self.btnWindowClose.setIconSize(QtCore.QSize(8, 8))
        self.btnWindowClose.setObjectName("btnWindowClose")
        self.horizontalLayout_3.addWidget(self.btnWindowClose)
        self.horizontalLayout.addWidget(self.frame_btns)

        self.retranslateUi(MainWindow)
        self.stackPanel.setCurrentIndex(0)
        # self.btnSignupPage.clicked.connect(self.stackPanel.raise)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.btnFacebook, self.btnGoogle)
        MainWindow.setTabOrder(self.btnGoogle, self.txtEmail_login)
        MainWindow.setTabOrder(self.txtEmail_login, self.txtPassword_login)
        MainWindow.setTabOrder(self.txtPassword_login, self.chkRememberme)
        MainWindow.setTabOrder(self.chkRememberme, self.btnForgotpwd)
        MainWindow.setTabOrder(self.btnForgotpwd, self.btnLogin)
        MainWindow.setTabOrder(self.btnLogin, self.btnSignupPage)
        MainWindow.setTabOrder(self.btnSignupPage, self.btnFacebook)
        MainWindow.setTabOrder(self.btnFacebook, self.btnGoogle)
        MainWindow.setTabOrder(self.btnGoogle, self.txtEmail_signup)
        MainWindow.setTabOrder(self.txtEmail_signup, self.txtPassword_signup)
        MainWindow.setTabOrder(self.txtPassword_signup, self.txtConfirmPassword_signup)
        MainWindow.setTabOrder(self.txtConfirmPassword_signup, self.btnSignup)
        MainWindow.setTabOrder(self.btnSignup, self.btnLoginPage)
        MainWindow.setTabOrder(self.btnLoginPage, self.btnSettings)
        MainWindow.setTabOrder(self.btnSettings, self.btnWindowMinimize)
        MainWindow.setTabOrder(self.btnWindowMinimize, self.btnWindowClose)
        MainWindow.setTabOrder(self.btnWindowClose, self.btnMicrophoneControl)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.txtEmail_login.setPlaceholderText(_translate("MainWindow", "email@example.com"))
        self.label_3.setText(_translate("MainWindow", "Log in"))
        self.chkRememberme.setText(_translate("MainWindow", "Remember Me"))
        self.label_4.setText(_translate("MainWindow", "or via E-mail"))
        self.txtPassword_login.setPlaceholderText(_translate("MainWindow", "Password"))
        self.btnForgotpwd.setText(_translate("MainWindow", "Forgot Password?"))
        self.lblEmail_2.setText(_translate("MainWindow", "Email"))
        self.lblPassword_2.setText(_translate("MainWindow", "Password"))
        self.btnLogin.setText(_translate("MainWindow", "Log in"))
        self.label_10.setText(_translate("MainWindow", "Don\'t  have an account?"))
        self.btnSignupPage.setText(_translate("MainWindow", "Signup"))
        self.label_2.setText(_translate("MainWindow", "or via E-mail"))
        self.txtEmail_signup.setPlaceholderText(_translate("MainWindow", "email@example.com"))
        self.label.setText(_translate("MainWindow", "Sign Up"))
        self.txtPassword_signup.setPlaceholderText(_translate("MainWindow", "Password"))
        self.lblEmail.setText(_translate("MainWindow", "Email"))
        self.lblPassword.setText(_translate("MainWindow", "Password"))
        self.btnSignup.setText(_translate("MainWindow", "Sign Up"))
        self.label_9.setText(_translate("MainWindow", "Already have an account?"))
        self.btnLoginPage.setText(_translate("MainWindow", "Login"))
        self.lblPassword_3.setText(_translate("MainWindow", "Confirm Password"))
        self.txtConfirmPassword_signup.setPlaceholderText(_translate("MainWindow", "Confirm Password"))
        self.label_5.setText(_translate("MainWindow", "Transcript"))
        self.lblLiveTranscript.setText(_translate("MainWindow", "boilerplate code"))

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_main()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
