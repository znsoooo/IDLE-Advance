'''运行选中'''

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import tkinter as tk

SRC_ST = '1.0'
SRC_ED = 'end'
SEL_ST = 'sel.first'
SEL_ED = 'sel.last'
INS_ST = 'insert'


class RunSelected(tk.Menu):
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            return

        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.text = parent.text
        self.flist = parent.flist
        self.rmenu = parent.rmenu
        self.MakeMenu(4)
        self.Binding()
        parent.amenu.insert_cascade(3, label='Run Selected', menu=self) # TODO 单元测试时插入偏差

    def Run(self, st, ed):
        code = self.text.get(st, ed)

        if not code:
            self.text.tag_add('sel', 'insert linestart', 'insert+1l linestart')
            self.text.mark_set('insert', 'insert linestart')
            code = self.text.get(st, ed)

        if code.startswith(' '):
            code = 'if 1:\n' + code

        # ref: idlexlib.extensions.RunSelection
        msg = '# Run Region [%s-%s]\n' % (self.text.index(st), self.text.index(ed))
        shell = self.flist.open_shell()
        console = shell.interp.tkconsole
        console.text.insert('insert', msg.replace('.', ':'))
        shell.interp.runcode(code)
        # TODO 报错位置和真实行号对应

    def MakeMenu(self, pos):
        self.add_command(label='Run Selected',    command=lambda: self.Run(SEL_ST, SEL_ED))
        self.add_command(label='Run to Cursor',   command=lambda: self.Run(SRC_ST, INS_ST))
        self.add_command(label='Run from Cursor', command=lambda: self.Run(INS_ST, SRC_ED))
        self.add_command(label='Run this Script', command=lambda: self.Run(SRC_ST, SRC_ED))

        rmenu = self.rmenu # reverse order
        rmenu.insert_command(pos, label='Run this Script', command=lambda: self.Run(SRC_ST, SRC_ED))
        rmenu.insert_command(pos, label='Run from Cursor', command=lambda: self.Run(INS_ST, SRC_ED))
        rmenu.insert_command(pos, label='Run to Cursor',   command=lambda: self.Run(SRC_ST, INS_ST))
        rmenu.insert_command(pos, label='Run Selected',    command=lambda: self.Run(SEL_ST, SEL_ED))
        rmenu.insert_separator(pos)

    def Binding(self):
        text = self.text
        text.bind('<Shift-F5>', lambda e: self.Run(SEL_ST, SEL_ED) if text.tag_ranges('sel') else self.Run(SRC_ST, SRC_ED))
        text.bind('<Shift-F6>', lambda e: self.Run(SRC_ST, INS_ST))
        text.bind('<Shift-F7>', lambda e: self.Run(INS_ST, SRC_ED))
