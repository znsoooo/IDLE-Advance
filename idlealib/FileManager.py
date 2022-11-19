'''文件操作'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
from os.path import dirname, basename
import subprocess
import tkinter as tk
from tkinter.simpledialog import askstring


class FileManager(tk.Menu):
    def __init__(self, parent):
        self.text = parent.text
        self.io = parent.io
        root = parent.root

        tk.Menu.__init__(self, root, tearoff=0)

        path = lambda: self.io.filename or os.getcwd() + os.sep # `io.filename` get `None` when in new file
        copy = lambda s: (root.clipboard_clear(), root.clipboard_append(s))
        insert = lambda s: self.text.insert('insert', s)

        self.add_command(label='Copy Fullname', command=lambda: copy(path()))
        self.add_command(label='Copy Filename', command=lambda: copy(basename(path())))
        self.add_command(label='Copy Dirname',  command=lambda: copy(dirname(path())))
        self.add_separator()
        self.add_command(label='Insert Fullname', command=lambda: insert("r'%s'" % path()))
        self.add_command(label='Insert Filename', command=lambda: insert("'%s'"  % basename(path())))
        self.add_command(label='Insert Dirname',  command=lambda: insert("r'%s'" % dirname(path())))
        self.add_separator()
        self.add_command(label='Open in Explorer', command=lambda: subprocess.Popen('explorer /select, "%s"' % path().replace('/', '\\')))
        self.add_command(label='Open in CMD',      command=lambda: subprocess.Popen('cmd /s /k pushd "%s"' % dirname(path())))
        # self.add_command(label='Run in CMD',       command=lambda: os.system('start "%s"'%io.filename)) # TODO
        self.add_separator()
        self.add_command(label='Rename File', command=self.Rename)
        self.add_command(label='Reload File', command=self.Reload)

        self.text.bind('<F2>', self.Rename)

        parent.amenu.insert_cascade(3, label='File Manager', menu=self)

    def Rename(self):
        basename2 = basename(self.io.filename)
        filename2 = askstring('Rename', 'Input new filename:', initialvalue=basename2, parent=self.text) # 允许输入相对路径
        if filename2:
            if filename2[-3:].lower() != '.py':
                filename2 += '.py'
            dirname2 = dirname(filename2)
            if dirname2: # 只输入文件名的时候路径为 ''
                os.makedirs(dirname2, exist_ok=True)
            os.rename(self.io.filename, filename2) # TODO 切换目录时工作路径未变化
            self.io.set_filename(os.path.abspath(filename2)) # TODO save状态变化

    def Reload(self): # TODO 重载记忆位置
        self.io.loadfile(self.io.filename)  # TODO rename也可以用这个方法
