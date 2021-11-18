import time

import pyautogui
import yaml
from yaml import SafeLoader
from pynput.keyboard import Key, Controller

keyboard = Controller()
print(list(map(lambda x: x, Key._member_map_.values())))

ReversekeyMapping = {
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
ctrl_keys = {
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


def fetch_commands(ext):
    # Open the file and load the file
    if ext == "word":
        with open("demo.yml") as f:
            yaml.safe_dump()
            data = yaml.load(f, Loader=SafeLoader)
            commands = data[ext]
    else:
        with open("demo.yml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            commands = data[ext]
    return commands


def keys(keyStrokes):
    print("KeyStrokes:-", keyStrokes)
    # pyautogui.write(keyStrokes)
    try:
        keyboard.type(ctrl_keys[keyStrokes])
    except Exception as e:
        keyboard.type(keyStrokes)


def openApp(app):
    print("App opened:-", app)


def leftClick(data):
    print("ClickedAt:-", data["x"])
    pyautogui.leftClick(data["x"], data["y"])


def rightClick(data):
    print("ClickedAt:-", data["x"])
    pyautogui.rightClick(data["x"], data["y"])


def moveTo(data):
    pyautogui.moveTo(data["x"], data["y"])


def timeSleep(data):
    print("Sleeping")
    time.sleep(int(data["sleep"]))


def hotKeyPress(data):
    keyboard.press(ReversekeyMapping[data])
    print("Pressed:", data)


def hotKeyRelease(data):
    print("Inside Release:", data)
    keyboard.release(ReversekeyMapping[data])
    print("Released:", data)


ds = {"open": openApp, "moveTo": moveTo, "leftClick": leftClick, "rightClick": rightClick, "keys": keys,
      "timeSleep": timeSleep, "hotKeyPress": hotKeyPress, "hotKeyRelease": hotKeyRelease}
transcript = 'demo'
rs = fetch_commands(transcript)
print(rs)
for i, val in enumerate(rs):
    print(val)
    try:
        print("In try")
        if type(val) == str:
            keys(val)
            continue
        for innerVal in val.keys():
            print("Inner keys=", innerVal)
            print("Function Call", innerVal)
            print("Data ", val[innerVal])
            ds[innerVal](val[innerVal])
            continue
    except Exception as e:
        print("Error:", e)
        print("In catch")
