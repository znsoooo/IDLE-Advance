"""自动保存Untitled"""


import os
import time

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


PATH = '.pybak/autosave.py'


class SaveUntitled:
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            return

        self.text = parent.text
        self.io = parent.io
        self.get_saved = parent.get_saved  # function

        parent.before_close.append(self.Backup)
        self.Reload()

    def Backup(self):
        if self.io.filename is None: # is untitled script?
            s = self.text.get('1.0', 'end-1c').rstrip()
            if s:
                os.makedirs('.pybak', exist_ok=True)
                with open(PATH, 'a') as f:
                    f.write(time.strftime('# autosave @ %Y-%m-%d %H:%M:%S\n') + s + '\n\n')
            elif os.path.isfile(PATH):
                os.remove(PATH)

    def Reload(self):
        if self.io.filename is None: # is untitled script?
            if os.path.isfile(PATH):
                with open(PATH) as f:
                    s = f.read()
                self.text.insert('1.0', s)
                self.text.mark_set('insert', '1.0')
                os.remove(PATH)
