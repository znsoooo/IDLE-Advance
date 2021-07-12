'''重载文件'''

# TODO F5运行的时候保存了吗？提示文件有更新


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
from tkinter.messagebox import askyesno


def mtime(file):
    if file:
        return str(int(os.stat(file).st_mtime * 1e7))  # TODO 查看修改日期我之前是怎么写的？
    else:
        return 0


class AutoReload:
    def __init__(self, parent):
        self.root = parent.root
        self.io = parent.io

        self.mt = mtime(self.io.filename)
        parent.text_frame.bind('<FocusIn>', self.OnFocusIn)
        parent.after_save.append(self.Refresh)

    def Refresh(self):
        self.mt = mtime(self.io.filename)

    def ReloadFile(self): # TODO 重载记忆位置
        self.io.loadfile(self.io.filename)  # TODO rename也可以用这个方法

    def OnFocusIn(self, e):
        mt = mtime(self.io.filename)
        if self.mt != mt:
            self.mt = mt  # 激活窗口最多只提示一次，下一次提示在本地文件再次发生修改
            if askyesno('Refresh?', 'Find text changed, do you need to refresh?', parent=self.root):  # TODO 参考notepad的窗口提示文本
                self.ReloadFile()
