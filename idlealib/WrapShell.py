"""Shell换行"""


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


class WrapShell:
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            self.text = parent.per.text  # TODO 研究一下作用原理

            parent.rmenu.add_separator()
            parent.rmenu.add_command(label='Wrap shell', command=self.ChangeWrap)
            parent.add_adv_menu('Wrap shell', self.ChangeWrap)

    def ChangeWrap(self):
        if self.text['wrap'] == 'none':
            self.text['wrap'] = 'char'
        else:
            self.text['wrap'] = 'none'
