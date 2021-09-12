# Copyright (c) 2021 Lishixian (znsoooo). All Rights Reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT


'''
运行__main__.py获得一个加载所有插件的IDLE-Advance的示例文件。
运行__init__.py获得一个打开自身脚本并加载所有插件的editor的例子。
分别运行idlealib目录下的扩展文件，可以得到一个打开自身的editor或shell的例子。
如果需要停用部分扩展，将对应的脚本移出目录后重启IDLE即可。
'''


import os

import idlelib.calltip

EXTENSIONS = []

# idlelib.calltip._MAX_LINES = 999
# idlelib.calltip._MAX_COLS = 999


class Calltip(idlelib.calltip.Calltip):
    def __init__(self, editwin=None):
        super().__init__(editwin)
        editwin.ctip = self # make hook

    # def fetch_tip(self, expression):
    #     self.expression = expression
    #     self.argspec = super().fetch_tip(expression)
    #     return self.argspec


idlelib.calltip.Calltip = Calltip



import keyword
import idlelib.autocomplete


class MyAutoComplete(idlelib.autocomplete.AutoComplete):
    def fetch_completions(self, what, mode):
        ret = super().fetch_completions(what, mode)
        if mode == idlelib.autocomplete.COMPLETE_ATTRIBUTES and what == '':
            for lst in ret[:2]:
                lst.extend(v for v in keyword.kwlist if v not in lst) # `None/True/False` are repetitive.
                lst.sort()
        return ret


idlelib.autocomplete.AutoComplete = MyAutoComplete




def FixPath():
    # To fix open shell (call run() without sys.argv) or self.load_extension(name) will not work.
    import sys
    path = os.path.dirname(__file__)
    if path not in sys.path:
        sys.path.insert(0, path)


import idlelib.editor
from idlelib.editor import EditorWindow
from idlelib.mainmenu import menudefs

# editor.EditorWindow -> pyshell.PyShellEditorWindow
# editor.EditorWindow -> outwin.OutputWindow -> pyshell.PyShell


mymenudef = ('advance', [])

menudefs.append(('advance', []))


class MyEditorWindow(EditorWindow):
    def __init__(self, *args):
        if ('advance', 'Advance') not in self.menu_specs:
            self.menu_specs.append(('advance', 'Advance'))

        EditorWindow.__init__(self, *args)

        self.amenu = self.menudict['advance']
        self.make_rmenu() # make "self.rmenu"

        self.before_copy = []
        self.after_save  = []
        self.after_close = []

        text = self.text
        text.bind('<<save-window>>', self.save) # fix all event handle in this class.
        text.bind('<F12>', self.Test)

        self.recent_files_menu['postcommand'] = self.update_recent_files_list # fix list not refresh when open another IDLE.

        self.load_adv_extensions()

    def cut(self, event):
        [f() for f in self.before_copy] # same as `copy`
        return super().cut(event)

    def copy(self, event):
        [f() for f in self.before_copy]
        return super().copy(event)

    def _close(self):
        print('handle with edit _close:', self.io.filename)
        super()._close()
        # raise # TODO 是否还有别的方法阻止清空剪切

    def close(self):
        # "<<close-window>>"事件不命中点击窗口关闭事件
        print('handle with edit close:', self.io.filename)
        [f() for f in self.after_close]
        super().close()

    def save(self, e):
        self.io.save(e)
        [f() for f in self.after_save]

    def add_adv_menu(self, label, sub, index='end', sp=False):
        menu = self.menudict['advance']
        if sp and menu.index('end') is not None:
            menu.insert_separator(index)
        if callable(sub):
            menu.insert_command(index, label=label, command=sub)
        else:
            menu.insert_cascade(index, label=label, menu=sub)

    def load_adv_extensions(self):
        for file in EXTENSIONS:
            name, ext = os.path.splitext(os.path.basename(file))
            if ext == '.py' and name not in ['__init__', '__main__']:
                try:
                    self.load_extension(name) # TODO 支持任意位置文件导入
                except:
                    print('Failed to import IDLE-Adv extension: %s' % name)
                    import traceback
                    traceback.print_exc()

        menu = self.menudict['advance']
        if menu.type('end') == 'separator':
            menu.delete('end')

    def Test(self, e):
        print('editor on test')
        print('mark_names:', self.text.mark_names())
        print('tag_names:', self.text.tag_names())
        print('functions:', ' '.join(v for v in dir(self.text) if 'tag' in v or 'mark' in v))


idlelib.editor.EditorWindow = MyEditorWindow
from idlelib.pyshell import main  # must after hot patch


def run(filename=None, exts=()):
    FixPath()
    EXTENSIONS.extend(exts)
    if not EXTENSIONS:
        EXTENSIONS.extend(file for file in os.listdir(os.path.dirname(__file__)))
    if filename:
        import sys
        sys.argv.append(filename) # Idea from "~\Lib\tkinter\__main__.py"
    main()


def test_editor(script_file):
    run(script_file, [script_file])


def test_shell(script_file):
    run(None, [script_file])


if __name__ == '__main__':
    run(__file__)


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
