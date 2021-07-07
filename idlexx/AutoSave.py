'''自动备份'''

# TODO 恢复未保存状态

import os

TICK = 7000

class AutoSave:
    def __init__(self, parent):
        self.root = parent.root
        self.io = parent.io
        self.root.after(TICK, self.Backup)

    def Backup(self):
        self.io.writefile(os.path.splitext(self.io.filename)[0] + '.pybak') # TODO 当文本相同时删除备份
        self.root.after(TICK, self.Backup)
