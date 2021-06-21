import tkinter as tk

class RunSelected(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.parent = parent
        self.MakeMenu(4)
        self.Binding()

    def Run(self, mode):
        '''mode: -1, 0, 1'''
        c1 = ['sel.first', 'insert', '1.0'][mode]
        c2 = ['sel.last',  'end', 'insert'][mode]

        code = self.parent.text.get(c1, c2)
        if code.startswith(' '):
            code = 'if 1:\n' + code

        # ref: idlexlib.extensions.RunSelection
        msg = '# Run Region [%s-%s]\n' % (self.parent.text.index(c1), self.parent.text.index(c2))
        shell = self.parent.flist.open_shell()
        console = shell.interp.tkconsole
        console.text.insert('insert', msg)
        shell.interp.runcode(code)
        # TODO 报错位置和真实行号对应

    def MakeMenu(self, pos):
        rmenu = self.parent.rmenu
        rmenu.insert_cascade(pos, label='Run from Cursor', command=lambda: self.Run(1))
        rmenu.insert_cascade(pos, label='Run to Cursor', command=lambda: self.Run(-1))
        rmenu.insert_cascade(pos, label='Run Selected', command=lambda: self.Run(0))
        rmenu.insert_separator(pos)

    def Binding(self):
        text = self.parent.text
        text.bind('<F6>', lambda e: self.Run(-1))
        text.bind('<F7>', lambda e: self.Run(0))
        text.bind('<F8>', lambda e: self.Run(1))
