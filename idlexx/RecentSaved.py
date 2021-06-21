'''
File Format:
mtime, cursor, filename
'''

# TODO 最后修改日期是否还用用途？顺序替代？

import os
import csv
from idlelib.config import idleConf

rc_path = os.path.join(idleConf.userdir, 'recent-saved.lst')
if not os.path.exists(rc_path):
    open(rc_path, 'w').close()


def mtime(file):
    return str(int(os.stat(file).st_mtime * 1e7)) # TODO 查看修改日期我之前是怎么写的？


def GetList():
    with open(rc_path, encoding='u8', newline='') as f:
        data = list(csv.reader(f))
    return data


def SetList(data): # TODO 位置标记换成冒号
    data.sort()
    with open(rc_path, 'w', encoding='u8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return data


def FindInData(data, file): # TODO 区分第一次打开和打开记录为1.0
    for row in data:
        if file == row[2]:
            return row
    data.append(['0', '1.0', file]) # change in place
    return data[-1]


def Update(file, cur, save=True):
    data = GetList()
    row = FindInData(data, file) # <data> maybe change in place
    if save:
        row[0] = mtime(file)
    row[1] = cur
    SetList(data)


def ReloadCursor(text, file):
    data = GetList()
    cur = FindInData(data, file)[1]
    text.mark_set('insert', cur)
    text.see(cur)
    text.tag_remove("sel", "1.0", "end")
    text.tag_add("sel", "insert linestart", "insert linestart+1l")


def SaveCursor(text, file, save=True):
    cur = text.index('insert')
    Update(file, cur, save)


class RecentSaved:
    def __init__(self, parent):
        self.parent = parent

    def OnOpen(self):
        ReloadCursor(self.parent.text, self.parent.io.filename)

    def OnSave(self):
        SaveCursor(self.parent.text, self.parent.io.filename)

    def OnClose(self):
        SaveCursor(self.parent.text, self.parent.io.filename, False)


# TODO 最近保存文件列表（排除已打开文件）
def GetRecentChangedFiles():
    # TODO 查看修改日期我之前是怎么写的？
    rf_path = os.path.join(idleConf.userdir, 'recent-files.lst')
    with open(rf_path, 'r', encoding='u8') as f:
        rf_list = f.read().splitlines()
    rf_list.sort(key=lambda p: os.stat(p).st_mtime if os.path.isfile(p) else 0, reverse=True)
    return rf_list

