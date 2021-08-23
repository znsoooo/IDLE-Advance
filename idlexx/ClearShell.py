'''清空Shell'''


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


# TODO 增加菜单 'Clear Shell Window'

from idlelib.pyshell import PyShell


class ClearShell:
    def __init__(self, parent):
        if isinstance(parent, PyShell):
            self.text = parent.per.bottom # TODO 研究一下作用原理
            self.text.bind("<<clear-window>>", self.clear_window)
            self.text.bind("<Control-l>", self.clear_window)

    def clear_window(self, event):
        text = self.text
        text.delete('1.0', 'iomark linestart')


# Ref: ~\idlexlib\extensions\ClearWindow.py
