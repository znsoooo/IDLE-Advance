'''窗口操作'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
import tkinter as tk


class WindowManager(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.parent = parent
        self.text = parent.text
        self.flist = parent.flist
        self.MakeMenu()
        self.Binding()
        parent.amenu.insert_cascade(3, label='Window Manager', menu=self)

    def OnRestore(self, *args): # TODO 恢复窗口时恢复记忆位置
        with open(self.parent.recent_files_path, encoding='u8') as f:
            rf_list = f.read().splitlines()
        dict = self.flist.dict
        for file in rf_list:
            if os.path.normcase(file) not in dict:
                return self.parent.io.open(editFile=file)

    def OnNext(self, n):
        windows = list(self.flist.inversedict)
        index = windows.index(self.parent)
        window = windows[(index + n) % len(windows)]
        window.top.wakeup()  # See at: idlelib.window.WindowList.add_windows_to_menu
        return 'break' # 避免窗口左右移动

    def OnNew(self, *args):
        self.text.event_generate('<<open-new-window>>')

    def OnClose(self, *args):
        self.OnNext(-1)
        self.text.event_generate('<<close-window>>')

    def OnCloseAll(self, *args):
        self.text.event_generate('<<close-all-windows>>')

    def MakeMenu(self):
        self.add_command(label='New Window',        command=self.OnNew)
        self.add_command(label='Restore Window',    command=self.OnRestore)
        self.add_separator()
        self.add_command(label='Prev Window',       command=lambda: self.OnNext(-1))
        self.add_command(label='Next Window',       command=lambda: self.OnNext(1))
        self.add_separator()
        self.add_command(label='Close Window',      command=self.OnClose)
        self.add_command(label='Close All Windows', command=self.OnCloseAll)

    def Binding(self):
        text = self.text
        text.bind('<Control-t>',       self.OnNew)
        text.bind('<Control-Shift-T>', self.OnRestore)
        text.bind('<Control-Prior>',   lambda e: self.OnNext(-1))
        text.bind('<Control-Next>',    lambda e: self.OnNext(1))
        text.bind('<Control-w>',       self.OnClose)
        text.bind('<Control-Shift-W>', self.OnCloseAll)
