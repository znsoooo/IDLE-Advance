"""IDLE Advance Extensions

运行__main__.py获得一个加载所有插件的IDLE-Advance的示例文件。
运行__init__.py获得一个打开自身脚本并加载所有插件的editor的例子。
分别运行idlealib目录下的扩展文件，可以得到一个打开自身的editor或shell的例子。
如果需要停用部分扩展，将对应的脚本移出目录后重启IDLE即可。

See also: https://github.com/znsoooo/IDLE-Advance

MIT license. Copyright (c) 2021-2024 Shixian Li (znsoooo). All Rights Reserved.

"""


import os
import sys

PY36 = sys.version_info > (3, 6)
# `abspath` for open in cmd like `python __init__.py` to open script.
EXTENSIONS = os.listdir(os.path.dirname(os.path.abspath(__file__)))

__author__  = 'Shixian Li <lsx7@sina.com>'
__credits__ = 'See at: https://github.com/znsoooo/IDLE-Advance'
__date__    = '20240622'
__version__ = '1.2.10'

__all__ = ['run', 'test_editor', 'test_shell', 'PY36']


# - Functions ----------------------------------------


def fix_path():
    # To fix open shell (call run() without sys.argv) or self.load_extension(name) will not work.
    import sys
    path = os.path.dirname(__file__)
    if path not in sys.path:
        sys.path.insert(0, path)


def wrap_function(func, before=(), after=()):
    def wrapper(*args, **kwargs):
        # print(func.__name__) # for test
        [f() for f in before]
        ret = func(*args, **kwargs)
        [f() for f in after]
        return ret
    return wrapper


# - idleConf ----------------------------------------


if not PY36:
    from functools import partial
    from idlelib.configHandler import idleConf

    idleConf.GetOption = partial(idleConf.GetOption, warn_on_default=False)

    # idleConf.userCfg['extensions'].set('ZzDummy', 'enable', 'true') # fix do not show many warning in py34 and py35
    #
    # if idleConf.userCfg['extensions'].has_option('ZzDummy', 'enable'):
    #     ret = idleConf.userCfg['extensions'].Get('ZzDummy', 'enable', type='bool')
    #     print(ret)
    #
    # print(idleConf.GetOption('extensions', 'ZzDummy', 'enable', default=True, type='bool'))
    # sys.exit(0)

    # idleConf._GetOption, idleConf.GetOption = idleConf.GetOption, print
    # def GetOption(configType, section, option, *args, **kw):
    #     if section.lower() == 'ZzDummy'.lower():
    #         print((configType, section, option))
    #         return False
    #     ret = idleConf._GetOption(configType, section, option, *args, **kw)
    #     return ret
    # idleConf.GetOption = GetOption


# - Calltip ----------------------------------------


if PY36:
    import idlelib.calltip
    from idlelib.calltip import Calltip
else:
    import idlelib.CallTips
    from idlelib.CallTips import CallTips as Calltip


# idlelib.calltip._MAX_LINES = 999
# idlelib.calltip._MAX_COLS = 999


class MyCalltip(Calltip):
    def __init__(self, editwin=None):
        super().__init__(editwin)
        editwin.ctip = self # make hook

    # def fetch_tip(self, expression):
    #     self.expression = expression
    #     self.argspec = super().fetch_tip(expression)
    #     return self.argspec


if PY36:
    idlelib.calltip.Calltip = MyCalltip
else:
    idlelib.CallTips.CallTips = MyCalltip


# - AutoComplete ----------------------------------------


if sys.version_info < (3, 8):
    if PY36:
        import idlelib.autocomplete
        from idlelib.autocomplete import AutoComplete
    else:
        import idlelib.AutoComplete
        from idlelib.AutoComplete import AutoComplete

    import keyword

    class MyAutoComplete(AutoComplete):
        def fetch_completions(self, what, mode):
            ret = super().fetch_completions(what, mode)
            ATTRS = int(sys.version_info < (3, 7))
            if mode == ATTRS and what == '':
                for lst in ret[:2]:
                    lst.extend(v for v in keyword.kwlist if v not in lst) # `None/True/False` are repetitive.
                    lst.sort()
            return ret

    if PY36:
        idlelib.autocomplete.AutoComplete = MyAutoComplete
    else:
        idlelib.AutoComplete.AutoComplete = MyAutoComplete


# - IOBinding ----------------------------------------


if PY36:
    import idlelib.iomenu
    from idlelib.iomenu import IOBinding
else:
    import idlelib.IOBinding
    from idlelib.IOBinding import IOBinding


class MyIOBinding(IOBinding):
    def __init__(self, editwin):
        # F5保存时，调用idlelib.runscript.getfilename()，设置自动保存时进入self.editwin.io.save(None)进行保存
        self.save = wrap_function(self.save, editwin.before_save, editwin.after_save)
        IOBinding.__init__(self, editwin)


if PY36:
    idlelib.iomenu.IOBinding = MyIOBinding
else:
    idlelib.IOBinding.IOBinding = MyIOBinding


# - EditorWindow ----------------------------------------


# editor.EditorWindow -> pyshell.PyShellEditorWindow
# editor.EditorWindow -> outwin.OutputWindow -> pyshell.PyShell

if PY36:
    import idlelib.editor
    from idlelib.editor import EditorWindow
else:
    import idlelib.EditorWindow
    from idlelib.EditorWindow import EditorWindow


class MyEditorWindow(EditorWindow):
    def __init__(self, *args):
        if ('advance', 'Advance') not in self.menu_specs:
            self.menu_specs.append(('advance', 'Advance'))

        self.before_copy = []
        self.after_save  = []
        self.before_save = []
        self.before_close = []

        # must before text binding, so before `EditorWindow.__init__()`
        self.cut = wrap_function(self.cut, before=self.before_copy)  # same as `copy`
        self.copy = wrap_function(self.copy, before=self.before_copy)
        self._close = wrap_function(self._close, before=self.before_close)  # "<<close-window>>"事件不命中点击窗口关闭事件

        EditorWindow.__init__(self, *args)
        self.text.tag_lower('hit', 'sel') # fix can't highlight text in sys.stdout

        self.amenu = self.menudict['advance']
        self.make_rmenu() # make "self.rmenu"

        self.recent_files_menu['postcommand'] = self.update_recent_files_list  # fix list not refresh when open another IDLE.

        self.text.bind('<ButtonRelease-1>', lambda e: self.text.event_generate('<<set-line-and-column>>')) # fix event can't multi-binding to `ButtonRelease-1`
        self.load_adv_extensions()
        self.text.bind('<F12>', self.test)

    def add_adv_menu(self, label, sub, index='end', sp=False):
        menu = self.menudict['advance']
        if sp and menu.index('end') is not None:
            menu.insert_separator(index)
        if callable(sub):
            menu.insert_command(index, label=label, command=sub)
        else:
            menu.insert_cascade(index, label=label, menu=sub)

    def load_extension(self, name):
        # for PY34 always raise error.
        if name == 'ZzDummy':
            return
        return super().load_extension(name)

    def load_adv_extensions(self):
        for file in EXTENSIONS:
            name, ext = os.path.splitext(os.path.basename(file))
            if name[:2] != '__' and ext.lower() == '.py':
                try:
                    self.load_extension(name) # TODO 支持任意位置文件导入
                except Exception as e:
                    print("Fail to load extension 'idlealib.%s':\n  %s" % (name, e), file=sys.stderr)
                    # import traceback
                    # traceback.print_exc()

        menu = self.menudict['advance']
        if menu.type('end') == 'separator':
            menu.delete('end')

    def test(self, e):
        print('editor on test')
        print('mark_names:', self.text.mark_names())
        print('tag_names:', self.text.tag_names())
        print('functions:', ' '.join(v for v in dir(self.text) if 'tag' in v or 'mark' in v))

        print('wrapped functions:')
        for f1 in ('copy', 'save', 'close'):
            for f2 in ('before', 'after'):
                f3 = f2 + '_' + f1
                if hasattr(self, f3):
                    print(f3 + ':', ['%s.%s' % (f.__module__, f.__name__) for f in getattr(self, f3)])


if PY36:
    idlelib.editor.EditorWindow = MyEditorWindow
else:
    idlelib.EditorWindow.EditorWindow = MyEditorWindow


# - Main ----------------------------------------


# must after hot patch
if PY36:
    from idlelib.pyshell import main
else:
    from idlelib.PyShell import main


def run(ext=None, filename=None):
    if ext:
        EXTENSIONS.clear()
        EXTENSIONS.append(ext)
    fix_path()
    if filename:
        sys.argv.append(filename) # Idea from "~\Lib\tkinter\__main__.py"
    main()


def test_editor(script):
    run(script, script)


def test_shell(script):
    run(script)


if __name__ == '__main__':
    run(None, __file__)


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
