"""自动保存Untitled"""


import os

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


PATH = '~autosave.py'


class SaveUntitled:
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            return

        self.text = parent.text
        self.io = parent.io
        self.get_saved = parent.get_saved  # function

        parent.after_close.append(self.Backup)
        self.Reload()

    def Backup(self):
        # print('Backup')
        if self.io.filename is None: # is untitled script?
            if self.text.get('1.0', 'end-1c'):
                self.io.writefile(PATH)
            elif os.path.isfile(PATH):
                os.remove(PATH)

    def Reload(self):
        # print('Reload')
        if self.io.filename is None: # is untitled script?
            if os.path.isfile(PATH):
                self.FakeLoadFile(PATH)
                os.remove(PATH)

    def FakeLoadFile(self, filename): # is that too.. dirty?
        fake = lambda *args: None
        temp = self.io.set_filename, self.io.reset_undo, self.io.updaterecentfileslist
        self.io.set_filename = self.io.reset_undo = self.io.updaterecentfileslist = fake

        self.text.undo_block_start()
        self.text.insert('1.0', '') # In order to undo, the cursor can move to the top.
        self.io.loadfile(filename)
        self.text.undo_block_stop()

        self.io.set_filename, self.io.reset_undo, self.io.updaterecentfileslist = temp
