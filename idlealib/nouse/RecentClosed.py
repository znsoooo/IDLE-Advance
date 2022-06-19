'''最近关闭列表'''

# TODO 合并到 RecentSaved.py


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
import csv
import tkinter as tk

import sys
if sys.version_info > (3, 6):
    from idlelib.config import idleConf
else:
    from idlelib.configHandler import idleConf

userdir = idleConf.GetUserCfgDir()
rc_path = os.path.join(userdir, 'recent-saved.lst')
if not os.path.exists(rc_path):
    open(rc_path, 'w').close()


def ReadData():
    with open(rc_path, encoding='u8', newline='') as f:
        data = list(csv.reader(f))
    return data


class RecentClosed(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0, postcommand=self.Update)
        self.io = parent.io
        parent.amenu.insert_cascade(3, label='Recent Edit Files', menu=self)

    def Update(self): # TODO 排除已打开文件
        rf_list = ReadData()
        ulchars = "1234567890ABCDEFGHIJK"
        rf_list = rf_list[0:len(ulchars)]
        self.delete(0, 'end')
        for i, (cur, file_name) in enumerate(rf_list):
            f = self.Callback(file_name)
            self.add_command(label=ulchars[i] + " " + file_name, command=f, underline=0)

    def Callback(self, file):
        def f():
            self.io.open(editFile=file)
        return f

