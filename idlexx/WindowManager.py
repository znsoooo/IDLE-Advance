import os
import tkinter as tk

class WindowManager(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.parent = parent
        self.MakeMenu()
        self.Binding()

    def GetFileList(self):
        filename = self.parent.io.filename
        op_list = self.parent.top.instance_dict.values()
        with open(self.parent.recent_files_path, encoding='u8') as f:
            rf_list = f.read().splitlines()
        now = -1
        opened = []
        closed = []
        for n, file1 in enumerate(rf_list):
            if os.path.samefile(file1, filename):
                now = n
            # 大小写斜杠不同导致不同字符串但是可能是同一个文件 # TODO os.path.normcase(...) Ref: idlelib.filelist.open
            status = any(os.path.samefile(file1, file2) for file2 in op_list)
            if status:
                opened.append(file1)
            else:
                closed.append(file1)
        return now, opened, closed

    def OnRestore(self, *args): # TODO 恢复窗口时恢复记忆位置
        now, opened, closed = self.GetFileList()
        if closed: # not empty
            self.parent.io.open(editFile=closed[0])

    def OnPrev(self, *args):
        now, opened, closed = self.GetFileList()
        new = (now + 1) % len(opened)
        self.parent.io.open(editFile=opened[new])

    def OnNext(self, *args):
        now, opened, closed = self.GetFileList()
        new = (now - 1) % len(opened)
        self.parent.io.open(editFile=opened[new])

    def OnClose(self, *args): # TODO 多次恢复之后检查关闭后激活下一个的循环顺序问题
        self.OnPrev()
        self.parent._close() # TODO 没有保存!! event: '<<close-all-windows>>', '<<close-window>>'

    def OnCloseAll(self, *args):
        for win in list(self.parent.top.instance_dict): # list the dict avoid dict changed during run.
            win._close()

    def MakeMenu(self):
        self.add_command(label='Restore Window', command=self.OnRestore)
        self.add_separator()
        self.add_command(label='Prev Window', command=self.OnPrev)
        self.add_command(label='Next Window', command=self.OnNext)
        self.add_separator()
        self.add_command(label='Close Window', command=self.OnClose)
        self.add_command(label='Close All Windows', command=self.OnCloseAll)

    def Binding(self):
        text = self.parent.text
        text.bind('<Control-Shift-T>', self.OnRestore)
        text.bind('<Control-Prior>', self.OnPrev)
        text.bind('<Control-Next>', self.OnNext)
        text.bind('<Control-w>', self.OnClose)
        text.bind('<Control-Shift-W>', self.OnCloseAll)
