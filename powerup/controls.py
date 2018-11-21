import pickle, os

buttons = {
    "close": 1,
    "launch": 2,
    "intake": 3,
    "toggle": 4,
    "descend": 5,
    "lift": 6,
}

# xbox


# joystick = {
#     # "shift": 9,
#     # "shift": 1,
#     "forward-axis": 1,
#     "turn-axis": 4,
#     # "turn-axis": 4,
#     # "turn-axis": 2,a
#     "intake": 1,
#     "outtake": 6,
#     "close": 2,
#     "launch": 4,
#     "exchange": 5,
#     "toggle": 3,
#     "descend": 7,
#     "lift": 8,
#     # "goto 0": 8,
#     # "cattywampus": 10,
# }

# joystick

joystick = {
    # "shift": 10,
    "shift": 1,
    "forward-axis": 1,
    # "turn-axis": 4,
    "turn-axis": 2,
    "intake": 3,
    "outtake": 4,

    "close": 5,
    "launch": 6,
    "exchange": 7,
    "toggle": 8,
    "descend": 9,
    "lift": 10,
    "goto 0": 11,
    "cattywampus": 12,
    # "descend": 5,
    # "lift": 6,
}

joystick_save = lambda a: os.path.join(os.path.dirname(__file__), a + '.pickle')


class RecordJoystick:
    def __init__(self):

        self.axes_numbers = [1, 2]
        self.button_numbers = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        self.axes = []
        self.buttons = []

    def getRawAxis(self, axis):
        try:
            return self.axes[-1][axis]
        except:
            return 0

    def getY(self):
        return self.getRawAxis(1)

    def getRawButton(self, button):
        try:
            return self.buttons[-1][button]
        except:
            return 0

    def recordButtons(self, buttons):
        recorded_buttons = {}
        for button in self.button_numbers:
            recorded_buttons[button] = buttons.getRawButton(button)
        self.buttons.append(recorded_buttons)

    def recordAxes(self, axes):
        recorded_axes = {}
        for axis in self.axes_numbers:
            recorded_axes[axis] = axes.getRawAxis(axis)
        self.axes.append(recorded_axes)

    def next(self):
        try:
            self.axes.pop()
            self.buttons.pop()
        except:
            pass

    def finish(self, name):
        self.axes = self.axes[::-1]
        self.buttons = self.buttons[::-1]
        self.save(name)
        
    def save(self, name):
        with open(joystick_save(name), 'wb') as fp:
            pickle.dump(self, fp)
            fp.close()

    def load(self, name):
        with open(joystick_save(name), 'rb') as fp:
            joystick = pickle.load(fp)
            fp.close()
        return joystick

    def __str__(self):
        return "AXES: {} \n\nBUTTONS: {}".format(str('\n'.join(list(map(str, self.axes)))),
                                                 str('\n'.join(list(map(str, self.buttons)))))
