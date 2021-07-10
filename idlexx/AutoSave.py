'''自动备份'''

import os
from tkinter.messagebox import showinfo

TICK = 7000

class AutoSave:
    def __init__(self, parent):
        self.root = parent.root
        self.io = parent.io
        self.get_saved = parent.get_saved # function

        self.root.after(TICK, self.Backup)

        self.AfterOpen()
        parent.after_save.append(self.AfterSave)
        parent.after_close.append(self.AfterClose)

    def Backup(self, loop=True):
        filename = self.io.filename
        if filename:
            filename_bak = os.path.splitext(filename)[0] + '.pybak'
            if self.get_saved():
                if os.path.isfile(filename_bak):
                    os.remove(filename_bak)
            else:
                self.io.writefile(filename_bak)
        if loop:
            self.root.after(TICK, self.Backup)

    def AfterSave(self):
        self.Backup(False)

    def AfterClose(self):
        self.Backup(False)

    def AfterOpen(self): # TODO 恢复存档
        filename = self.io.filename
        if filename:
            filename_bak = os.path.splitext(filename)[0] + '.pybak'
            if os.path.isfile(filename_bak):
                self.FakeLoadFile(filename_bak)

    def FakeLoadFile(self, filename_bak): # is that too.. dirty?
        fake = lambda *args: None
        temp = self.io.set_filename, self.io.reset_undo, self.io.updaterecentfileslist
        self.io.set_filename, self.io.reset_undo, self.io.updaterecentfileslist = fake, fake, fake
        self.io.loadfile(filename_bak)
        self.io.set_filename, self.io.reset_undo, self.io.updaterecentfileslist = temp
