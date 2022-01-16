'''重载文件'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
from tkinter.messagebox import askyesno


def mtime(file):
    return os.path.getmtime(file) if file else 0


class AutoReload:
    def __init__(self, parent):
        self.root = parent.root
        self.io = parent.io
        self.set_saved = parent.set_saved

        self.mt = mtime(self.io.filename)
        parent.text_frame.bind('<FocusIn>', self.OnFocusIn)
        parent.after_save.append(self.Refresh)
        parent.add_adv_menu('Reload', self.ReloadFile)

    def Refresh(self):
        self.mt = mtime(self.io.filename)

    def ReloadFile(self): # TODO 重载记忆位置
        self.io.loadfile(self.io.filename)  # TODO rename也可以用这个方法

    def OnFocusIn(self, e):
        mt = mtime(self.io.filename)
        if self.mt != mt:
            self.mt = mt  # 激活窗口最多只提示一次，下一次提示在本地文件再次发生修改
            if askyesno('Reload', '"%s"\n\nThis script has been modified by another program.\nDo you want to reload it?' % self.io.filename, parent=self.root):
                self.ReloadFile()
            else:
                self.set_saved(False) # 设置为未保存状态
