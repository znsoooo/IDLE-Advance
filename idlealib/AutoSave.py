'''自动备份'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
import sys

TICK = 7000


class AutoSave:
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            return

        self.text = parent.text
        self.root = parent.root
        self.io = parent.io
        self.get_saved = parent.get_saved # function

        self.HotFix()

        self.root.after(TICK, self.Backup)

        self.AfterOpen()
        parent.after_save.append(self.AfterSave)
        parent.before_close.append(self.BeforeClose)

    def HotFix(self): # append '\n' at last line **after** cursor
        def new_api():
            self.text.mark_gravity('insert', 'left')
            ret = old_api()
            self.text.mark_gravity('insert', 'right')
            return ret

        if sys.version_info < (3, 7):
            old_api, self.io.fixlastline = self.io.fixlastline, new_api
        else:
            old_api, self.io.fixnewlines = self.io.fixnewlines, new_api

    def Backup(self, loop=True):
        filename = self.io.filename
        if not self.io.text: # will set as None in io.close()
            return # break loop only editor closed
        if filename:
            filename_bak = os.path.splitext(filename)[0] + '.pybak'
            if self.get_saved():
                if os.path.isfile(filename_bak):
                    os.remove(filename_bak)
            else:
                self.io.writefile(filename_bak)
        if loop: # don't stop loop while no filename, new file maybe saved later
            self.root.after(TICK, self.Backup)

    def AfterSave(self):
        self.Backup(False)

    def BeforeClose(self):
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
