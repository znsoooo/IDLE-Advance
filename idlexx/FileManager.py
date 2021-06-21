import os
import subprocess
import tkinter as tk
from tkinter.simpledialog import askstring

class FileManager(tk.Menu):
    def __init__(self, root, text, io):
        tk.Menu.__init__(self, root, tearoff=0)
        n = io.filename or os.getcwd() + '\\' # 当新建文件时 io.filename==None 尾部加分隔符避免获取路径出错
        text_insert   = lambda s: (lambda: text.insert('insert', s))
        clipboard_set = lambda s: (lambda: (root.clipboard_clear(), root.clipboard_append(s)))

        self.add_command(label='Copy Fullname', command=clipboard_set(n))
        self.add_command(label='Copy Filename', command=clipboard_set(os.path.basename(n)))
        self.add_command(label='Copy Dirname',  command=clipboard_set(os.path.dirname(n)))
        self.add_separator()
        self.add_command(label='Insert Fullname', command=text_insert("r'%s'"%n))
        self.add_command(label='Insert Filename', command=text_insert("'%s'"%os.path.basename(n)))
        self.add_command(label='Insert Dirname',  command=text_insert("r'%s'"%os.path.dirname(n)))
        self.add_separator()
        self.add_command(label='Open in Explorer', command=lambda: subprocess.Popen('explorer %s'%os.path.dirname(n)))
        self.add_command(label='Open in CMD',      command=lambda: os.system('start'))
        # self.add_command(label='Run in CMD',       command=lambda: os.system('start "%s"'%io.filename)) # TODO
        self.add_separator()
        self.add_command(label='Rename File', command=lambda: self.Rename(text, io))
        self.add_command(label='Reload File', command=lambda: self.Reload(io))

        text.bind('<F2>', lambda e: self.Rename(text, io))


        # TODO rename, reload, copy, backup


    def Rename(self, text, io):
        basename = os.path.basename(io.filename)
        filename2 = askstring('Rename', 'Input new filename:', initialvalue=basename, parent=text) # 允许输入相对路径
        if filename2:
            if filename2[-3:].lower() != '.py':
                filename2 += '.py'
            dirname2 = os.path.dirname(filename2)
            if dirname2: # 只输入文件名的时候路径为 ''
                os.makedirs(dirname2, exist_ok=True)
            os.rename(io.filename, filename2) # TODO 切换目录时工作路径未变化
            io.set_filename(os.path.abspath(filename2)) # TODO save状态变化

    def Reload(self, io): # TODO 重载记忆位置
        io.loadfile(io.filename)  # TODO rename也可以用这个方法
