from pynput.mouse import Button
from ruamel import yaml
from pynput import keyboard, mouse


class TaskListener:
    def __init__(self, taskName):
        self.final_string = str
        self.taskName = taskName
        self.taskEntries = {str(self.taskName): []}
        self.pressed_keys = []
        self.leftMouseClick = []
        self.leftMouseClickIndex = 0
        self.rightMouseClick = []
        self.rightMouseClickIndex = 0
        self.custom_keys = [keyboard.Key.space, keyboard.Key.down]
        # Setup the listener threads
        self.break_program = False
        self._startListeners()

    def _startListeners(self):
        with keyboard.Listener(on_press=self.on_press) as keyboarListener, mouse.Listener(on_move=self.on_move,
                                                                                          on_click=self.on_click) as mouseListener:
            keyboarListener.join()
            mouseListener.join()
        # task = {
        #     "keys": self.final_string,
        #     "leftClick": self.leftMouseClick,
        # }
        # print(self.taskEntries, task)
        # demo1234 demo12345
        if True:
            # self.taskEntries[self.taskName].append(task)
            # demo12345
            print("While loop ended ", self.taskEntries)
            with open('demo.yml', 'a', encoding="utf-8") as yamlfile:
                yaml.dump(self.taskEntries, yamlfile, Dumper=yaml.RoundTripDumper, default_flow_style=False)

    def on_press(self, key):
        if key == keyboard.Key.end:
            print('end pressed')
            self.break_program = True
            return False
        print("Key pressed: {0}".format(key))
        print(type(key))
        if key == keyboard.Key.space:
            self.pressed_keys.append(" ")
        else:
            self.pressed_keys.append(key.char)
        print(self.pressed_keys)
        self.final_string = ''.join(self.pressed_keys)
        print(self.final_string)
        # demo12345
        self.taskEntries[self.taskName].append(key.char)
        print(self.taskEntries)

    def on_move(self, x, y):
        if self.break_program:
            return False
        # print("Mouse moved to ({0}, {1})".format(x, y)) demo1234

    def on_click(self, x, y, button, pressed):
        if pressed:
            print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
            cliked = {"x": x, "y": y}
            if button == Button.left:
                print("Left")
                self.taskEntries[self.taskName].append({"leftClick": cliked})
                print(self.taskEntries)
            elif button == Button.left:
                self.taskEntries[self.taskName].append({"rightClick": cliked})
                print(self.taskEntries)
            else:
                print("Middle mouse button not supported yet")
        else:
            print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))

    def on_scroll(self, x, y, dx, dy):
        print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


TaskListener("demo5")
