import os
from tkinter.messagebox import askyesno


def mtime(file):
    if file:
        return str(int(os.stat(file).st_mtime * 1e7))  # TODO 查看修改日期我之前是怎么写的？
    else:
        return 0


class Reloader:
    def __init__(self, parent):
        self.parent = parent
        self.mt = mtime(self.parent.io.filename)

    def Refresh(self):
        self.mt = mtime(self.parent.io.filename)

    def ReloadFile(self): # TODO 重载记忆位置
        self.parent.io.loadfile(self.parent.io.filename)  # TODO rename也可以用这个方法

    def OnFocusIn(self, e):
        mt = mtime(self.parent.io.filename)
        if self.mt != mt:
            self.mt = mt  # 激活窗口最多只提示一次，下一次提示在本地文件再次发生修改
            if askyesno('Refresh?', 'Find text changed, do you need to refresh?', parent=self.parent.text):  # TODO 参考notepad的窗口提示文本
                self.ReloadFile()
