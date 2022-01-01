import os
import time
import pyautogui
import yaml
from yaml import SafeLoader
from pynput.keyboard import Key, Controller

keyboard = Controller()


class RunTask:
    def __init__(self, transcript):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.taskJsonFilePath = os.path.join(ROOT_DIR, '../application/config/tasks.json')
        self.taskBindingsFilePath = os.path.join(ROOT_DIR, '../application/config/task_bindings.yml')
        self.transcript = transcript
        self.functionMapping = {"moveTo": self.moveTo, "leftClick": self.leftClick, "rightClick": self.rightClick,
                                "keys": self.keys,
                                "timeSleep": self.timeSleep, "hotKeyPress": self.hotKeyPress,
                                "hotKeyRelease": self.hotKeyRelease}
        self.ReversekeyMapping = {
            " ": Key.space,
            "Key.backspace": Key.backspace,
            "Key.enter": Key.enter,
            "Key.ctrl_r": Key.ctrl_r,
            "Key.ctrl_l": Key.ctrl_l,
            "Key.alt_l": Key.alt_l,
            "Key.alt_gr": Key.alt_gr,
            "Key.cmd": Key.cmd,
            "Key.shift": Key.shift,
            "Key.tab": Key.tab,
            "Key.left": Key.left,
            "Key.down": Key.down,
            "Key.right": Key.right,
            "Key.up": Key.up,
            "Key.esc": Key.esc,
            "Key.insert": Key.insert,
            "Key.home": Key.home,
            "Key.page_up": Key.page_up,
            "Key.page_down": Key.page_down,
            "Key.pause": Key.pause,
            "Key.scroll_lock": Key.scroll_lock,
            "Key.print_screen": Key.print_screen,
            "Key.f1": Key.f1,
            "Key.f2": Key.f2,
            "Key.f3": Key.f3,
            "Key.f4": Key.f4,
            "Key.f5": Key.f5,
            "Key.f6": Key.f6,
            "Key.f7": Key.f7,
            "Key.f8": Key.f8,
            "Key.f9": Key.f9,
            "Key.f10": Key.f10,
            "Key.f11": Key.f11,
            "Key.f12": Key.f12,
            "Key.num_lock": Key.num_lock,
            "Key.caps_lock": Key.caps_lock,
        }

        self.ctrl_keys = {
            "\x01": "a",
            "\x02": "b",
            "\x03": "c",
            "\x04": "d",
            "\x05": "e",
            "\x06": "f",
            "\x07": "g",
            "\x08": "h",
            "\x09": "i",
            "\n": "j",
            "\v": "k",
            "\f": "l",
            "\r": "m",
            "\x0E": "n",
            "\x0F": "o",
            "\x10": "p",
            "\x11": "q",
            "\x12": "r",
            "\x13": "s",
            "\x14": "t",
            "\x15": "u",
            "\x16": "v",
            "\x17": "w",
            "\x18": "x",
            "\x19": "y",
            "\x1A": "z",
        }

    def enumerateData(self):
        rs = self.fetch_commands(self.transcript)
        print(rs)
        for i, val in enumerate(rs):
            print(val)
            try:
                print("In try")
                if type(val) == str:
                    self.keys(val)
                    continue
                for innerVal in val.keys():
                    print("Inner keys=", innerVal)
                    print("Function Call", innerVal)
                    print("Data ", val[innerVal])
                    self.functionMapping[innerVal](val[innerVal])
                    continue
            except Exception as e:
                print("Error:", e)
                print("In catch")

    def fetch_commands(self, ext):
        # Open the file and load the file
        if ext == "word":
            with open(self.taskBindingsFilePath) as f:
                data = yaml.load(f, Loader=SafeLoader)
                commands = data[ext]
        else:
            with open(self.taskBindingsFilePath) as f:
                data = yaml.load(f, Loader=SafeLoader)
                commands = data[ext]
                print(commands)
                time.sleep(5)
        return commands

    def keys(self, keyStrokes):
        print("KeyStrokes:-", keyStrokes)
        # pyautogui.write(keyStrokes)
        try:
            keyboard.type(self.ctrl_keys[keyStrokes])
        except Exception as e:
            keyboard.type(keyStrokes)

    def leftClick(self, data):
        print("ClickedAt:-", data["x"])
        pyautogui.leftClick(data["x"], data["y"])

    def rightClick(self, data):
        print("ClickedAt:-", data["x"])
        pyautogui.rightClick(data["x"], data["y"])

    def moveTo(self, data):
        pyautogui.moveTo(data["x"], data["y"])

    def timeSleep(self, data):
        print("Sleeping")
        time.sleep(float(data["sleep"]))

    def hotKeyPress(self, data):
        keyboard.press(self.ReversekeyMapping[data])
        print("Pressed:", data)

    def hotKeyRelease(self, data):
        print("Inside Release:", data)
        keyboard.release(self.ReversekeyMapping[data])
        print("Released:", data)


# d1 = RunTask("Open Mail")
# d1.enumerateData()
