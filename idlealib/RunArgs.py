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

        parent.add_adv_menu('Run with args', self.Run, sp=True)

    def Run(self): # TODO 有没有更优雅的方法？
        args = askstring('Run with args', 'args:', parent=self.root)
        if args is not None:
            self.text.insert('1.0', "__import__('sys').argv.append({args!r})\n\n".format(args=args))


if __name__ == '__main__': # for test
    import sys
    print(sys.argv)
