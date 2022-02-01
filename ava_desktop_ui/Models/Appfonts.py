from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont


class AppFonts:
    light = 'Poppins Light'
    extra_light = 'Poppins Extra Light'
    bold = 'Poppins'
    semi_bold = 'Poppins SemiBold'

    def getErrorFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(10)
        font.setBold(True)
        return font

    def getHeadingFont(self):
        font = QtGui.QFont()
        font.setFamily(self.light)
        font.setPointSize(36)
        return font

    def getAuthHeadingFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(32)
        font.setBold(True)
        return font

    def getFormHeadingFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(10)
        font.setBold(True)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)
        return font

    def getLinkButtonFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(10)
        font.setBold(True)
        font.setLetterSpacing(QFont.PercentageSpacing, 105)
        return font

    def getTaskTitleFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(18)
        font.setBold(True)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)
        return font

    def getLightFont(self):
        font = QtGui.QFont()
        font.setFamily(self.light)
        font.setPointSize(8)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)
        return font

    def getMenuButtonFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(12)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)
        return font

    def getTaskDescriptionFont(self):
        font = QtGui.QFont()
        font.setFamily(self.light)
        font.setPointSize(12)
        font.setBold(True)
        font.setLetterSpacing(QFont.PercentageSpacing, 108)
        return font

    def getLineEditFont(self):
        font = QtGui.QFont()
        font.setFamily(self.semi_bold)
        font.setPointSize(8)
        font.setLetterSpacing(QFont.PercentageSpacing, 108)
        return font

    def getAuthButtonFont(self):
        font = QtGui.QFont()
        font.setFamily(self.bold)
        font.setPointSize(10)
        font.setBold(True)
        font.setLetterSpacing(QFont.PercentageSpacing, 105)
        return font


appFonts = AppFonts()
