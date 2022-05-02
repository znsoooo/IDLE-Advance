'''位置记录'''

# TODO 未保存文档但更新位置，可能导致光标位置指向错误？


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
import csv

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
        self.text = parent.text
        self.io = parent.io
        self.AfterOpen()
        parent.after_save.append(self.OnSave)
        parent.before_close.append(self.OnClose)

    def AfterOpen(self):
        if not self.io.filename:
            return
        data = ReadData()
        ret = FindInData(data, self.io.filename)
        if ret:
            cur = ret[1]
            text = self.text
            text.mark_set('insert', cur)
            text.see('insert linestart') # See line start to prevent XScrollBar at right.
            text.tag_remove('sel', '1.0', 'end')
            text.tag_add('sel', 'insert linestart', 'insert linestart+1l')
        else:
            data.insert(0, ['1:0', self.io.filename])
            SaveData(data)

    def OnSave(self, save=True):
        if not self.io.filename:
            return
        cur = self.text.index('insert')
        Update(self.io.filename, cur, save)

    def OnClose(self):
        self.OnSave(False)
