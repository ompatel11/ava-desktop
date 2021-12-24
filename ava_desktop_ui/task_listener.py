import threading
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput import keyboard, mouse
import qtawesome as qta


class TaskListener:
    def __init__(self, taskName, main_obj):
        self._mainObject = main_obj
        self.isFinished = bool
        self.final_string = str
        self.taskName = taskName
        self.taskEntries = {str(self.taskName): []}
        self.lastPressedStatus = ""
        self.keyMapping = {
            Key.space: " ",
            Key.alt_l: "Key.alt_l",
            Key.backspace: "Key.backspace",
            Key.enter: "Key.enter",
            Key.ctrl_r: "Key.ctrl_r",
            Key.ctrl_l: "Key.ctrl_l",
            Key.alt_gr: "Key.alt_gr",
            Key.cmd: "Key.cmd",
            Key.shift: "Key.shift",
            Key.tab: "Key.tab",
            Key.left: "Key.left",
            Key.down: "Key.down",
            Key.right: "Key.right",
            Key.up: "Key.up",
            Key.esc: "Key.esc",
            Key.insert: "Key.insert",
            Key.home: "Key.home",
            Key.page_up: "Key.page_up",
            Key.page_down: "Key.page_down",
            Key.pause: "Key.pause",
            Key.scroll_lock: "Key.scroll_lock",
            Key.print_screen: "Key.print_screen",
            Key.f1: "Key.f1",
            Key.f2: "Key.f2",
            Key.f3: "Key.f3",
            Key.f4: "Key.f4",
            Key.f5: "Key.f5",
            Key.f6: "Key.f6",
            Key.f7: "Key.f7",
            Key.f8: "Key.f8",
            Key.f9: "Key.f9",
            Key.f10: "Key.f10",
            Key.f11: "Key.f11",
            Key.f12: "Key.f12",
            Key.num_lock: "Key.num_lock",
            Key.caps_lock: "Key.caps_lock",
        }
        self.start_time = time.time()
        self.break_program = False
        icon4 = QtGui.QIcon(qta.icon('fa5s.stop', color='#3e3c54'))
        self._mainObject.ui.btnTaskListener.setIcon(icon4)
        self._mainObject.ui.btnTaskListener.setIconSize(QtCore.QSize(32, 32))
        self._mainObject.ui.btnTaskListener.setStyleSheet("QPushButton{\n"
                                                          "background-color: rgb(255, 255, 255);\n"
                                                          "border: 2px solid rgb(62, 60, 84);\n"
                                                          "border-radius: 40;\n"
                                                          "}\n"
                                                          "QPushButton:pressed{\n"
                                                          "    background-color: rgb(103, 100, 138);\n"
                                                          "}")

    def setExit(self):
        self.break_program = True
        icon4 = QtGui.QIcon(qta.icon('fa5s.play', color='white'))
        self._mainObject.ui.btnTaskListener.setIcon(icon4)
        self._mainObject.ui.btnTaskListener.setIconSize(QSize(32, 32))
        self._mainObject.ui.btnTaskListener.setStyleSheet("QPushButton{\n"
                                                          "background-color: rgb(62, 60, 84);\n"
                                                          "border: 1px solid white;\n"
                                                          "border-radius: 40;\n"
                                                          "}\n"
                                                          "QPushButton:pressed{\n"
                                                          "    background-color: rgb(103, 100, 138);\n"
                                                          "}")

    def elapsed_time(self):
        """
        :return float(elapsed_time):
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        print(elapsed_time + 1.0)
        self.start_time = current_time
        return elapsed_time

    def startListeners(self):
        """
        Setup Keyboard and Mouse Listeners
        :return None:
        """
        t1 = threading.Thread(target=self.executeListeners)
        t1.start()

    def executeListeners(self):
        self.isFinished = False
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as keyboarListener, mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click) as mouseListener:
            keyboarListener.join()
            mouseListener.join()
        if True:
            print("Break program:", self.break_program)
            try:
                print("While loop ended ", self.taskEntries)
                self.isFinished = True
                # with open('task_bindings.yml', 'a', encoding="utf-8") as yamlfile:
                #     yaml.dump(self.taskEntries, yamlfile, Dumper=yaml.RoundTripDumper, default_flow_style=False)
                return self.taskEntries
            except Exception as e:
                return False

    def on_release(self, key):
        if key == keyboard.Key.end:
            print('end pressed')
            self.break_program = True
            return False
        print("Key released: {0}".format(key))
        print(type(key))
        #  he
        try:
            self.taskEntries[self.taskName].append({"hotKeyRelease": self.keyMapping[key]})
            self.taskEntries[self.taskName].append({"timeSleep": {"sleep": 0.9}})

        except Exception as e:
            pass
            # self.taskEntries[self.taskName].append(key.char)
        print(self.taskEntries)

    def on_press(self, key):
        """
        Records keys pressed by the user
        :param key:
        :return None:
        """
        # if self.lastPressedStatus == key:
        #     return
        if self.break_program:
            print('Exit called')
            self.isFinished = True
            return False
        if key == keyboard.Key.end:
            print('end pressed')
            self.break_program = True
            self.isFinished = True
            return False
        self.lastPressedStatus = key
        print("Key pressed: {0}".format(key))
        print(type(key))

        try:
            if self.keyMapping[key]:
                self.taskEntries[self.taskName].append({"timeSleep": {"sleep": 0.9}})
            self.taskEntries[self.taskName].append({"hotKeyPress": self.keyMapping[key]})

        except Exception as e:
            if keyboard.Controller.ctrl_pressed:
                k = str(key.char)
                bArr = bytearray()
                bArr.extend(map(ord, k))
                print("CTRL Pressed: ", bArr.decode("UTF-8"))
                for b in bArr:
                    print(b, hex(b), chr(b))
                self.taskEntries[self.taskName].append(bArr.decode("UTF-8"))
                return
            self.taskEntries[self.taskName].append(key.char)
        print(self.taskEntries)

    def on_move(self, x, y):
        if self.break_program:
            self.isFinished = False
            return False
        # print("Mouse moved to ({0}, {1})".format(x, y))
        # i = 0
        # if i == 0:
        #     self.taskEntries[self.taskName].append({"moveTo": {"x": x, "y": y}})
        #     i += 1

    def on_click(self, x: int, y: int, button: Button, pressed: bool):
        """
        Records Mouse Click events of user
        :param x:
        :param y:
        :param button:
        :param pressed:
        :return:
        """
        if self.break_program:
            print('Exit called')
            self.isFinished = True
            return False
        if pressed:
            print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
            cliked = {"x": x, "y": y}
            if button == Button.left:
                self.taskEntries[self.taskName].append({"timeSleep": {"sleep": self.elapsed_time()}})
                self.taskEntries[self.taskName].append({"moveTo": {"x": x, "y": y}})
                print("Left")
                self.taskEntries[self.taskName].append({"leftClick": cliked})
                print(self.taskEntries)
            elif button == Button.left:
                self.taskEntries[self.taskName].append({"timeSleep": {"sleep": self.elapsed_time()}})
                print("Elapsed Time = ", self.elapsed_time())
                self.taskEntries[self.taskName].append({"rightClick": cliked})
                print(self.taskEntries)
            else:
                print("Middle mouse button not supported yet")
        else:
            print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))

    def on_scroll(self, x, y, dx, dy):
        print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

# TaskListener("TEST2").startListeners()
