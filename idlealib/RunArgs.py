"""带参数运行"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


from tkinter.simpledialog import askstring


class RunArgs:
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            return

        self.text = parent.text
        self.root = parent.root
        self.flist = parent.flist

        self.args = None

        parent.add_adv_menu('Run with args', self.Run, sp=True)

    def AppendArgs(self, interp):
        if self.args is not None:
            code = "__import__('sys').argv.extend(%r.split())" % self.args
            interp.runcommand(code)
            self.args = None

    def Run(self):
        args = askstring('Run with args', 'args:', parent=self.root)
        if args is not None:
            self.args = args
            shell = self.flist.open_shell()
            _runcode = shell.interp.runcode
            shell.interp.runcode = lambda code: [self.AppendArgs(shell.interp), _runcode(code)]
            self.text.event_generate('<<run-module>>')


if __name__ == '__main__': # for test
    import sys
    print(sys.argv)
