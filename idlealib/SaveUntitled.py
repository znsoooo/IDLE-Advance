"""自动保存Untitled"""

# Will make `.autosave` dir.  TODO 把各个插件的文件读写需求情况写明


import os

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import time

import sys
if sys.version_info > (3, 6):
    from idlelib.config import idleConf
    from idlelib.runscript import ScriptBinding
else:
    from idlelib.configHandler import idleConf
    from idlelib.ScriptBinding import ScriptBinding


class SaveUntitled:
    def __init__(self, parent):
        self.io = parent.io
        self.get_saved = parent.get_saved  # function

        self.sb = ScriptBinding(parent)
        parent.text.bind("<<check-module>>", self.sb.check_module_event)
        parent.text.bind("<<run-module>>", self.run_module_event)

    def run_module_event(self, evt):
        autosave = idleConf.GetOption('main', 'General', 'autosave', type='bool')
        if autosave and not self.io.filename and not self.get_saved():
            self.io.filename = os.path.abspath(time.strftime('.autosave/Untitled@%Y%m%d_%H%M%S.py'))
            os.makedirs('.autosave', exist_ok=True)
            self.io.save(None)
        self.sb.run_module_event(evt)
