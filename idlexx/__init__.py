import os
import re
import subprocess
import time

import tkinter as tk

from idlelib.config import idleConf
from idlelib.mainmenu import menudefs
from idlelib.pyshell import main, PyShellFileList, PyShellEditorWindow
import idlelib.pyshell
import idlelib.editor
from idlelib import window

from pprint import pprint

from .ReplaceBar import ReplaceBar
from .SmartSelect import SmartSelect, FixTextSelect
from .WindowManager import WindowManager
from .RecentClipboard import RecentClipboard



def OnTest(e):
    print(e)
    print(type(e))
    print(e.widget)
    print(type(e.widget))


class CursorHistory:
    def __init__(self, text):
        self.text = text
        self.pointer = 0
        self.history = ['1.0']



    def Add(self, e):
        # TODO 当文本变化时平移历史记录
        # TODO 记录文件名+位置
        # TODO 只记录行数
        cur = self.text.index('insert')
        if cur != self.history[self.pointer]:
            self.pointer += 1
            self.history = self.history[:self.pointer] + [cur]


    def Move(self, text, n):
        if -1 < self.pointer + n < len(self.history):
            self.pointer += n
            text.see(self.history[self.pointer])
            tag = '-1c' if n > 0 else '+1c' # TODO 当用快捷键操作时会多运动一个字符
            text.mark_set('insert', self.history[self.pointer] + tag)


#########


def GetRecentChangedFiles():
    # TODO 查看修改日期我之前是怎么写的？
    rf_path = os.path.join(idleConf.userdir, 'recent-files.lst')
    with open(rf_path, 'r', encoding='u8') as f:
        rf_list = f.read().splitlines()
    rf_list.sort(key=lambda p: os.stat(p).st_mtime if os.path.isfile(p) else 0, reverse=True)
    return rf_list

##print('\n'.join(GetRecentChangedFiles()))




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


class FileManager(tk.Menu):
    def __init__(self, root, text, io):
        tk.Menu.__init__(self, root, tearoff=0)
        n = io.filename or os.getcwd() + '\\' # 当新建文件时 io.filename==None 尾部加分隔符避免获取路径出错
        text_insert   = lambda s: (lambda: text.insert('insert', s))
        clipboard_set = lambda s: (lambda: (root.clipboard_clear(), root.clipboard_append(s)))

        self.add_command(label='Copy Fullname', command=clipboard_set(n))
        self.add_command(label='Copy Filename', command=clipboard_set(os.path.basename(n)))
        self.add_command(label='Copy Dirname',  command=clipboard_set(os.path.dirname(n)))
        self.add_separator()
        self.add_command(label='Insert Fullname', command=text_insert("r'%s'"%n))
        self.add_command(label='Insert Filename', command=text_insert("'%s'"%os.path.basename(n)))
        self.add_command(label='Insert Dirname',  command=text_insert("r'%s'"%os.path.dirname(n)))
        self.add_separator()
        self.add_command(label='Open in Explorer', command=lambda: subprocess.Popen('explorer %s'%os.path.dirname(n)))
        self.add_command(label='Open in CMD',      command=lambda: os.system('start'))
        # self.add_command(label='Run in CMD',       command=lambda: os.system('start "%s"'%io.filename)) # TODO
        self.add_separator()
        self.add_command(label='Reload File', command=lambda: io.loadfile(io.filename))


        # TODO rename, reload, copy


class RunSelected(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.parent = parent
        self.MakeMenu(4)
        self.Binding()

    def Run(self, mode):
        '''mode: -1, 0, 1'''
        c1 = ['sel.first', 'insert', '1.0'][mode]
        c2 = ['sel.last',  'end', 'insert'][mode]

        code = self.parent.text.get(c1, c2)
        if code.startswith(' '):
            code = 'if 1:\n' + code

        # ref: idlexlib.extensions.RunSelection
        msg = '# Run Region [%s-%s]\n' % (self.parent.text.index(c1), self.parent.text.index(c2))
        shell = self.parent.flist.open_shell()
        console = shell.interp.tkconsole
        console.text.insert('insert', msg)
        shell.interp.runcode(code)
        # TODO 报错位置和真实行号对应

    def MakeMenu(self, pos):
        rmenu = self.parent.rmenu
        rmenu.insert_cascade(pos, label='Run from Cursor', command=lambda: self.Run(1))
        rmenu.insert_cascade(pos, label='Run to Cursor', command=lambda: self.Run(-1))
        rmenu.insert_cascade(pos, label='Run Selected', command=lambda: self.Run(0))
        rmenu.insert_separator(pos)

    def Binding(self):
        text = self.parent.text
        text.bind('<F6>', lambda e: self.Run(-1))
        text.bind('<F7>', lambda e: self.Run(0))
        text.bind('<F8>', lambda e: self.Run(1))


mymenudef = ('advance', [
    ('Back', '<<my-function>>'),
    ('Forward', '<<my-function>>'),
    None,
    None,
    ('Recent Changed Files', '<<my-function>>'),
    None,
    ('Reload File', '<<my-function>>'),
    None,
    ('Run Selected', '<<run-selected>>'),
    None,
    ('Compare to File', '<<compare-file>>'), # TODO 支持选择py或全部格式文件
    None,
    ('!Replace Bar', '<<my-function>>'),
    ])

menudefs.append(mymenudef)


from . import RecentSaved as rs

# from idlelib.iomenu import IOBinding
#
# class MyIOBinding(IOBinding):
#     def open(self, event=None, editFile=None): # 这里是None
#         print('handle with io open:', editFile)
#         IOBinding.open(self, event=None, editFile=None)
#
#     def close(self):
#         print('handle with io close:', self.filename)
#         IOBinding.close(self)
#
#     def save(self, event): # TODO 重写save时的备份策略，参考notepad++的命名规则和备份频率
#         print('handle with io save:', self.filename)
#         ret = super().save(event)
#         return ret
#
# PyShellEditorWindow.IOBinding = MyIOBinding



PyShellEditorWindow.menu_specs.append(('advance', 'Advance')) # 如果写在方法里会导致多次运行时不断追加菜单

class MyPyShellEditorWindow(PyShellEditorWindow):
    # class IOBinding(IOBinding):
    #     def close(self):
    #         print('handle with io close:', self.filename)
    #         IOBinding.close(self)

    def __init__(self, flist=None, filename=None, key=None, root=None):
        PyShellEditorWindow.__init__(self, flist, filename, key, root)
        text = self.text

        FixTextSelect(self.root)

        ReplaceBar(self.text_frame, text).pack(fill='x', side='bottom')

        # TODO 会导致拖拽打开文件时闪退
        hbar = tk.Scrollbar(self.text_frame, orient='h')
        hbar['command'] = text.xview
        hbar.pack(fill='x', side='bottom')
        text['xscrollcommand'] = hbar.set
        # TODO 参考 idlelib.textview.ViewWindow 的 AutoHiddenScrollbar 方法


        ch = CursorHistory(text)
        text.bind('<ButtonRelease-1>', ch.Add) # TODO 会抹掉CodeBrowser.py中的鼠标点击事件（右下角行号不更新）
        text.bind('<Alt-Left>',  lambda e: ch.Move(e.widget, -1)) # TODO 兼容Alt+上下
        text.bind('<Alt-Right>', lambda e: ch.Move(e.widget,  1))


        for c in '([{\'"':
            text.bind('<%s>'%c, SmartPairing) # '<KeyRelease-%s>'%c

        # text.bind('<MouseWheel>', print) # for test
        text.bind('<F2>', self.OnTest)

        text.bind('<Double-Button-1>', SmartSelect)
        self.text_frame.bind('<FocusIn>', self.ReloadFile) # TODO 提示了3次？

        text.bind('<<my-function>>', lambda e: print('myfun', e))

        text.bind('<<compare-file>>', self.OnCompareFile)

        self.make_rmenu() # make "self.rmenu"

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

        RunSelected(self)

        rs.OnOpen(self.text, self.io.filename)

        self.text.bind("<<save-window>>", self.OnSave)

        print('On text init:', self.io.filename) # On Open

        self.mtime = rs.mtime(self.io.filename)

        try:
            import windnd
            windnd.hook_dropfiles(self.text, func=self.DragOpen)
        except:
            pass


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
        rs.OnSave(self.text, self.io.filename, save=False)
        super().close()

    def OnSave(self, e):
        self.io.save(e) # TODO 如果文件未修改则不备份、关闭前备份、关闭未保存备份、备份文件名参考notepad++和Photoshop和Autium Designer、编号命名备份、定时器备份
        self.io.writefile(os.path.splitext(self.io.filename)[0] + time.strftime('.%Y-%m-%d_%H-%M-%S.pybak'))
        rs.OnSave(self.text, self.io.filename)
        self.mtime = rs.mtime(self.io.filename)

    def OnTest(self, e):
        self.io.loadfile(__file__)
        # self.io.loadfile('run.py')


    def OnCompareFile(self, e): # TODO 移植到不依赖输入，支持任意文件接口
        import difflib
        import webbrowser
        from idlelib.textview import ViewWindow, Button # Button is ttk.Button

        file1 = self.io.filename
        file2 = self.io.askopenfile()
        if file2:
            with open(file1, encoding='u8') as f:
                ss1 = f.read().split('\n')
            with open(file2, encoding='u8') as f:
                ss2 = f.read().split('\n')
            title = 'Different between %s and %s'%(os.path.basename(file1), os.path.basename(file2)) # TODO 我之前时怎么命名的？

            d = difflib.Differ()
            ss3 = d.compare(ss1, ss2)
            text = '\n'.join(ss3)
            dlg = ViewWindow(self.text, title, text, wrap='none', _utest=True)
            dlg.viewframe.button_ok.forget() # ok按钮用的是ViewFrame里的控件!

            def show_html():
                d = difflib.HtmlDiff()
                with open(title + '.html', 'w', encoding='u8') as f:
                    f.write(d.make_file(ss1, ss2))
                webbrowser.open(title + '.html')

            toolbar = tk.Frame(dlg)
            Button(toolbar, text='HTML',  command=show_html).pack(side='left')
            Button(toolbar, text='Close', command=dlg.viewframe.ok).pack(side='left')
            toolbar.pack()

            dlg.wait_window()



    def DragOpen(self, files):
        for file_b in files:
            file = file_b.decode('gbk')
            if file.endswith('.py'):
                edit = self.flist.open(file)
                # TODO 由于滚动条存在导致有时候拖拽加载会闪退，增加下面两行可以避免
                edit.text.tag_add("sel", "insert", "insert+1c")
                edit.text.tag_remove("sel", "1.0", "end")

                # TODO 是否可以
                # self.io.open(editFile=file)


    def ReloadFile(self, e):
        mtime = rs.mtime(self.io.filename)
        if self.mtime != mtime:
            self.mtime = mtime # 激活窗口最多只提示一次，下一次提示在本地文件再次发生修改
            from tkinter.messagebox import askyesno # TODO package移到前面
            if askyesno('Refresh?', 'Find text changed, do you need to refresh?', parent=self.text): # TODO 参考notepad的窗口提示文本
                self.io.loadfile(self.io.filename)  # TODO rename也可以用这个方法



class MyPyShellFileList(PyShellFileList):
    EditorWindow = MyPyShellEditorWindow

    def open(self, filename, action=None): # TODO 重写open时的位置恢复策略
        print('handle with shell open:', filename)
        ret = super().open(filename, action)
        return ret # 没有ret导致open返回结果恒为None，在某些时候会多启动一个空窗口不符合预期


def run(filename=__file__):
    if filename:
        import sys
        sys.argv.append(filename) # Idea from "~\Lib\tkinter\__main__.py"
        # sys.argv.append(r'F:\lsx\coding\监控\udp.py')
    idlelib.pyshell.PyShellFileList = MyPyShellFileList
    main()


# import idlexlib.extensionManager
# import idlexlib.idlexMain


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
