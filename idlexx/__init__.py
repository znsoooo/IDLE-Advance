import os

### test
import idlelib.calltip

# idlelib.calltip._MAX_LINES = 999
# idlelib.calltip._MAX_COLS = 999

class Calltip(idlelib.calltip.Calltip):
    def __init__(self, editwin=None):
        super().__init__(editwin)
        editwin.ctip = self

    # def fetch_tip(self, expression):
    #     self.expression = expression
    #     self.argspec = super().fetch_tip(expression)
    #     return self.argspec


idlelib.calltip.Calltip = Calltip

###

import idlelib.editor
from idlelib.editor import EditorWindow
from idlelib.mainmenu import menudefs


mymenudef = ('advance', [
    ('Back', '<<my-function>>'),
    ('Forward', '<<my-function>>'),
    None,
    None,
    ('Compare to File', '<<compare-file>>'),
    None,
    ('Share QRCode', '<<share-qrcode>>'),
    ])

menudefs.append(mymenudef)


class MyEditorWindow(EditorWindow):
    def __init__(self, *args):
        if ('advance', 'Advance') not in self.menu_specs:
            self.menu_specs.append(('advance', 'Advance'))

        EditorWindow.__init__(self, *args)

        self.make_rmenu() # make "self.rmenu"

        self.after_copy = []
        self.after_save = []
        self.after_close = []

        text = self.text
        text.bind("<<save-window>>", self.save) # fix all event handle in this class.
        text.bind('<F12>', self.Test)

        self.load_idlexx_extensions()

        # 最近保存 TODO 无法在激活菜单时更新
        # self.menu_rc = RecentClosed(self)

    def copy(self, event): # TODO 没有对应剪切
        super().copy(event)
        for fun in self.after_copy:
            fun()

    def _close(self): # TODO 退出未保存前保存备份（.pybak）
        print('handle with edit _close:', self.io.filename)
        super()._close()
        # raise # TODO 是否还有别的方法阻止清空剪切

    def close(self):
        # "<<close-window>>"事件不命中点击窗口关闭事件
        print('handle with edit close:', self.io.filename)
        for fun in self.after_close:
            fun()
        super().close()

    def save(self, e): # TODO 重写save时的备份策略，参考notepad++的备份频率
        self.io.save(e) # TODO 如果文件未修改则不备份、关闭前备份、关闭未保存备份、定时器备份
        for fun in self.after_save:
            fun()

    def load_idlexx_extensions(self):
        for file in os.listdir(os.path.dirname(__file__)):
            name, ext = os.path.splitext(file)
            if ext == '.py' and name not in ['__init__', 'util', 'run', 'test']: # TODO 简化排除表达
                try:
                    self.load_extension(name)
                except Exception as e:
                    print("Failed to import IDLEXX extension: %s" % name)
                    import traceback
                    traceback.print_exc()

    def Test(self, e):
        print('editor ontest')
        print('mark_names:', self.text.mark_names())
        print('tag_names:', self.text.tag_names())


idlelib.editor.EditorWindow = MyEditorWindow
from idlelib.pyshell import main  # must after hot patch


def run(filename=__file__):
    if filename:
        import sys
        sys.argv.append(filename) # Idea from "~\Lib\tkinter\__main__.py"
    main()


import idlelib.run
'''
TODO 参考历史文件的打开方法，用于拖拽打开和恢复打开文件
def __recent_file_callback(self, file_name):
    def open_recent_file(fn_closure=file_name):
        self.io.open(editFile=fn_closure)
    return open_recent_file

# 打开文件并定位位置（恢复打开）
outwin.py:
self.flist.gotofileline(filename, lineno)
'''

# TODO 当不在instance_dict中将不会刷新（新启动的idle线程）
'''
def update_recent_files_list(self, new_file=None):
    ...
    # for each edit window instance, construct the recent files menu
    for instance in self.top.instance_dict:
        menu = instance.recent_files_menu
'''

# editor.EditorWindow -> pyshell.PyShellEditorWindow
# editor.EditorWindow -> outwin.OutputWindow -> pyshell.PyShell
