import os

import tkinter as tk

from idlelib.mainmenu import menudefs
from idlelib.pyshell import main, PyShellFileList, PyShellEditorWindow, PyShell
import idlelib.pyshell

import idlelib.editor

from .ReplaceBar import ReplaceBar
from .SmartSelect import SmartSelect, FixTextSelect
from .WindowManager import WindowManager
from .RecentClipboard import RecentClipboard
from .CompareFile import CompareFile
from .RunSelected import RunSelected
from .CursorHistory import CursorHistory
from .FileManager import FileManager

from .RecentSaved import RecentSaved, RecentClosed
from .ReloadFile import Reloader


def SmartPairing(e):
    # TODO 第一次输入右括号时移动光标但不键入
    # TODO 删除左括号时删除右括号（如果有的话）
    # TODO 有选区时输入括号不清除选区（包括光标位置）
    text = e.widget
    pair = ')]}\'"'['([{\'"'.index(e.char)]
    ss = e.widget.get('sel.first', 'sel.last')
    if ss:
        text.delete('sel.first', 'sel.last')
    text.mark_gravity('insert', 'left')
    text.insert('insert', pair)
    text.insert('insert', ss)
    text.mark_gravity('insert', 'right')


def UniqueFile(file):
    root = os.path.split(file)[0]
    n = 1
    while os.path.exists(file):
        n += 1
        file = '%s.%d.pybak'%(root, n)
    return file


def AddXScrollbar(frame, text):
    # TODO 会导致拖拽打开文件时闪退
    hbar = tk.Scrollbar(frame, orient='h')
    hbar['command'] = text.xview
    text['xscrollcommand'] = hbar.set
    hbar.pack(fill='x', side='bottom')
    # TODO 参考 idlelib.textview.ViewWindow 的 AutoHiddenScrollbar 方法


mymenudef = ('advance', [
    ('Back', '<<my-function>>'),
    ('Forward', '<<my-function>>'),
    None,
    None,
    ('Compare to File', '<<compare-file>>'),
    ])

menudefs.append(mymenudef)

PyShellEditorWindow.menu_specs.append(('advance', 'Advance')) # 如果写在方法里会导致多次运行时不断追加菜单

class MyPyShellEditorWindow(PyShellEditorWindow):
    def __init__(self, flist=None, filename=None, key=None, root=None):
        PyShellEditorWindow.__init__(self, flist, filename, key, root)
        text = self.text
        self.make_rmenu() # make "self.rmenu"

        FixTextSelect(self.root)
        ReplaceBar(self.text_frame, text)
        AddXScrollbar(self.text_frame, text)

        # 光标位置
        CursorHistory(text)

        for c in '([{\'"':
            text.bind('<%s>'%c, SmartPairing) # '<KeyRelease-%s>'%c
        text.bind('<Double-Button-1>', SmartSelect)
        text.bind('<<compare-file>>', self.OnCompareFile)

        # 快速正反搜索
        text.bind('<F3>', self.OnSearchForward)
        text.bind('<Shift-F3>', self.OnSearchBackward)

        # 历史剪切板功能
        self.menu_clip = RecentClipboard(self)
        self.rmenu.insert_cascade(3, label='History', menu=self.menu_clip)
        self.menudict['advance'].insert_cascade(3, label='Paste from History', menu=self.menu_clip)

        # 窗口操作
        menu_windows = WindowManager(self)
        self.menudict['advance'].insert_cascade(3, label='Window Manager', menu=menu_windows)

        # 文件操作
        menu_files = FileManager(self.root, self.text, self.io)
        self.menudict['advance'].insert_cascade(3, label='File Manager', menu=menu_files)

        # 位置记录
        self.menu_recorder = RecentSaved(self)
        self.menu_recorder.OnOpen()
        self.text.bind("<<save-window>>", self.OnSave)

        # 最近保存
        self.menu_rc = RecentClosed(self)
        self.menudict['advance'].insert_cascade(3, label='Recent Edit Files', menu=self.menu_rc)

        # 运行选中
        menu_runner = RunSelected(self) # TODO 添加到顶层菜单
        self.menudict['advance'].insert_cascade(3, label='Run Selected', menu=menu_runner)

        # 重载文件
        self.reloader = Reloader(self)
        self.text_frame.bind('<FocusIn>', self.reloader.OnFocusIn)

        try:
            import windnd
            windnd.hook_dropfiles(self.text, func=self.DragOpen)
        except:
            pass

        text.bind('<F2>', self.Test)


    def Test(self, e):
        print('editor ontest')
        print(self.text.tag_names())

    def copy(self, event):
        super().copy(event)
        self.menu_clip.Add()

    def _close(self): # TODO 退出未保存前保存备份（.pybak）
        print('handle with edit _close:', self.io.filename)
        super()._close()
        # raise # TODO 是否还有别的方法阻止清空剪切

    def close(self):
        # "<<close-window>>"事件不命中点击窗口关闭事件
        print('handle with edit close:', self.io.filename)
        self.menu_recorder.OnClose()
        super().close()

    def OnSearchForward(self, e):
        engin = idlelib.editor.search._setup(self.text)
        engin.engine.backvar.set(False)
        engin.find_again(self.text)

    def OnSearchBackward(self, e):
        engin = idlelib.editor.search._setup(self.text)
        engin.engine.backvar.set(True)
        engin.find_again(self.text)


    def OnSave(self, e): # TODO 重写save时的备份策略，参考notepad++的备份频率
        self.io.save(e) # TODO 如果文件未修改则不备份、关闭前备份、关闭未保存备份、定时器备份
        self.io.writefile(UniqueFile(self.io.filename))
        self.menu_recorder.OnSave()
        self.menu_rc.Update()
        self.reloader.Refresh()

    def OnCompareFile(self, e):
        file1 = self.io.filename
        file2 = self.io.askopenfile()
        if file2:
            CompareFile(self.text, file1, file2)

    def DragOpen(self, files): # TODO 恢复记忆位置
        for file_b in files:
            file = file_b.decode('gbk')
            if file.endswith('.py'):
                edit = self.flist.open(file)
                # TODO 由于滚动条存在导致有时候拖拽加载会闪退，增加下面两行可以避免
                edit.text.tag_add("sel", "insert", "insert+1c")
                edit.text.tag_remove("sel", "1.0", "end")

                # TODO 是否可以
                # self.io.open(editFile=file)


class MyPyShell(PyShell):
    def __init__(self, flist=None):
        PyShell.__init__(self, flist)
        self.text.bind('<F2>', self.Test)

    def Test(self, e):
        print('shell ontest')
        print(self.text.tag_names())
        for name in self.text.tag_names():
            print(name, self.text.tag_ranges(name))



idlelib.pyshell.PyShell = MyPyShell


class MyPyShellFileList(PyShellFileList):
    EditorWindow = MyPyShellEditorWindow


def run(filename=__file__):
    if filename:
        import sys
        sys.argv.append(filename) # Idea from "~\Lib\tkinter\__main__.py"
        # sys.argv.append(r'F:\lsx\coding\监控\udp.py')
    idlelib.pyshell.PyShellFileList = MyPyShellFileList
    main()



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
