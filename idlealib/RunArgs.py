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

        parent.add_adv_menu('Run with args', self.Run, sp=True)

    def Run(self):
        args = askstring('Run with args', 'args:', parent=self.root)
        if args is not None:
            cmd = "__import__('sys').argv.extend(%r.split())" % args
            shell = self.flist.open_shell()
            interp = shell.interp
            interp.runcommand(cmd)
            interp._runcode = interp.runcode
            interp.runcode = lambda evt: [interp.runcommand(cmd), interp._runcode(evt)]
            self.text.event_generate('<<run-module>>')


if __name__ == '__main__': # for test
    import sys
    print(sys.argv)
