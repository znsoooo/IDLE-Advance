import os

import idlelib.editor
from idlelib.editor import EditorWindow
from idlelib.mainmenu import menudefs

from .CompareFile import CompareFile



mymenudef = ('advance', [
    ('Back', '<<my-function>>'),
    ('Forward', '<<my-function>>'),
    None,
    None,
    ('Compare to File', '<<compare-file>>'),
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
        text.bind('<F2>', self.Test)

        # 最近保存
        # self.menu_rc = RecentClosed(self)

        self.load_idlexx_extensions()


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
        #
        # self.menu_rc.Update()

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
        print(self.text.tag_names())



idlelib.editor.EditorWindow = MyEditorWindow
from idlelib.pyshell import main#, PyShell
# import idlelib.pyshell
#
#
# class MyPyShell(PyShell):
#     def __init__(self, flist=None):
#         PyShell.__init__(self, flist)
#         self.text.bind('<F2>', self.Test)
#
#     def Test(self, e):
#         print('shell ontest')
#         text = self.text
#
#         print([v for v in dir(text) if 'tag' in v or 'mark' in v])
#         print(text.mark_names())
#         print(text.tag_names())
#         for name in text.tag_names():
#             print(name, text.tag_ranges(name))
#         print(text.tag_nextrange('stdin', '1.0'))
#         print(text.index('restart'))
#
#         ranges = text.tag_ranges('stdin')
#         codes = []
#         for i in range(0, len(ranges), 2):
#             code = text.get(ranges[i], ranges[i+1]).strip()
#             if code:
#                 codes.append(code)
#         s = '\n'.join(codes)
#         print(s)
#
#
# idlelib.pyshell.PyShell = MyPyShell


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

# pyshell.PyShellEditorWindow -> editor.EditorWindow
# pyshell.PyShell -> outwin.OutputWindow -> editor.EditorWindow
