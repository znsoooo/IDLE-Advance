"""快捷反缩进"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class ShiftTab:
    def __init__(self, parent):
        self.text = parent.text
        self.text.bind('<Shift-Tab>', self.callback)

    def callback(self, evt):
        self.text.event_generate('<<dedent-region>>')
        return 'break'
