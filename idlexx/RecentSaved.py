'''位置记录'''

import os
import csv
import tkinter as tk
from idlelib.config import idleConf

rc_path = os.path.join(idleConf.userdir, 'recent-saved.lst')
if not os.path.exists(rc_path):
    open(rc_path, 'w').close()


def ReadData():
    with open(rc_path, encoding='u8', newline='') as f:
        data = list(csv.reader(f))
    return data


def SaveData(data):
    with open(rc_path, 'w', encoding='u8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def FindInData(data, file):
    for n, (cur, file2) in enumerate(data):
        if file == file2:
            return n, cur.replace(':', '.')


def Update(file, cur, save=True):
    cur = cur.replace('.', ':')
    data = ReadData()
    ret = FindInData(data, file)
    if ret:
        n = ret[0]
        data[n][0] = cur
        if save:
            data.insert(0, data.pop(n)) # move to first
    else:
        data.insert(0, [cur, file])
    SaveData(data)


class RecentSaved:
    def __init__(self, parent):
        self.parent = parent
        self.OnOpen()
        parent.after_save.append(self.OnSave)
        parent.after_close.append(self.OnClose)

    def OnOpen(self):
        if not self.parent.io.filename:
            return
        data = ReadData()
        ret = FindInData(data, self.parent.io.filename)
        if ret:
            cur = ret[1]
            text = self.parent.text
            text.mark_set('insert', cur)
            text.see(cur)
            text.tag_remove("sel", "1.0", "end")
            text.tag_add("sel", "insert linestart", "insert linestart+1l")
        else:
            data.insert(0, ['1:0', self.parent.io.filename])
            SaveData(data)

    def OnSave(self, save=True):
        if not self.parent.io.filename:
            return
        cur = self.parent.text.index('insert')
        Update(self.parent.io.filename, cur, save)

    def OnClose(self):
        self.OnSave(False)


# class RecentClosed(tk.Menu): # TODO 不是很理想
#     def __init__(self, parent):
#         tk.Menu.__init__(self, parent.menubar, tearoff=0, takefocus=1)
#         self.parent = parent
#         self.data = []
#         self.Update() # TODO 无法做到每次点击窗口时更新
#         self.parent.menubar.bind('<Unmap>', print)
#         parent.menudict['advance'].insert_cascade(3, label='Recent Edit Files', menu=self)
#
#     def Update(self, new_file=None): # TODO 排除已打开文件
#         "Load and update the recent files list and menus"
#         rf_list = ReadData()
#         ulchars = "1234567890ABCDEFGHIJK"
#         rf_list = rf_list[0:len(ulchars)]
#         self.delete(0, 'end')  # clear, and rebuild:
#         for i, (cur, file_name) in enumerate(rf_list):
#             callback = self.Callback(file_name)
#             self.add_command(label=ulchars[i] + " " + file_name, command=callback, underline=0)
#
#     def Callback(self, file):
#         def f():
#             self.parent.io.open(editFile=file)
#         return f

