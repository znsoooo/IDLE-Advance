'''Shell多行运行'''


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


# TODO 自动格式化代码之前的空格
# TODO 增加到菜单（开关）


from idlelib.pyshell import PyShell


class RunMultiLine:
    def __init__(self, parent):
        if isinstance(parent, PyShell):
            self.parent = parent
            self.text = parent.text
            # self.text.bind('<Control-m>', self.Setup)
            self.text.bind('<<Paste>>', self.AfterPaste, '+') # Ref: IDLEX TODO 加号的作用是？？？

    def AfterPaste(self, e):
        self.text.after(10, self.Setup)

    def Setup(self, e=0):
        self.codes = self.text.get('iomark', 'end-1c').split('\n')
        self.text.delete('iomark', 'end-1c')
        self.text.after(10, self.Run)

    def Run(self): # See: idlelib.pyshell.PyShell.enter_callback
        p = self.parent
        text = self.text
        if self.codes and not p.canceled:
            while p.executing:
                text.after(10, self.Run)
                return
            code = self.codes.pop(0)
            text.mark_gravity('iomark', 'left') # without this it will run code skipped sometime. un-know reason.
            text.insert('insert', code)
            p.color.recolorize()
            if self.codes: # dont run last code.
                text.event_generate('<Return>')
                text.delete('end-1l', 'end-1c') # delete auto indent spaces.
            text.see('insert')
            text.after(10, self.Run)

