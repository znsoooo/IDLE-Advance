'''自动备份'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os

TICK = 7000


class AutoSave:
    def __init__(self, parent):
        self.text = parent.text
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
            if self.get_saved(): # TODO 当文件关闭后会再运行一次，会在这里获取判断失败
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
        self.io.set_filename = self.io.reset_undo = self.io.updaterecentfileslist = fake

        self.text.undo_block_start()
        self.text.insert('1.0', '') # In order to undo, the cursor can move to the top.
        self.io.loadfile(filename_bak)
        self.text.undo_block_stop()

        self.io.set_filename, self.io.reset_undo, self.io.updaterecentfileslist = temp
