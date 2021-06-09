import os
import re
import subprocess

import tkinter as tk

from idlelib.config import idleConf
from idlelib.mainmenu import menudefs
from idlelib.pyshell import main, PyShellFileList, PyShellEditorWindow
import idlelib.pyshell
import idlelib.editor
from idlelib import window

from pprint import pprint


def OnTest(e):
    from idlelib.textview import ViewWindow
    dlg = ViewWindow(e.widget, 'title', 'text')

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
        n = io.filename
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

        # TODO rename, reload, copy




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
    ('Compare to File', '<<my-function>>'), # TODO 支持选择py或全部格式文件
    None,
    ('!Replace Bar', '<<my-function>>'),
    ])

menudefs.append(mymenudef)




PyShellEditorWindow.menu_specs.append(('advance', 'Advance')) # 如果写在方法里会导致多次运行时不断追加菜单

class MyPyShellEditorWindow(PyShellEditorWindow):
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

        # text.bind('<MouseWheel>', print) # for test

        ch = CursorHistory(text)
        text.bind('<ButtonRelease-1>', ch.Add) # TODO 会抹掉CodeBrowser.py中的鼠标点击事件（右下角行号不更新）
        text.bind('<Alt-Left>',  lambda e: ch.Move(e.widget, -1)) # TODO 兼容Alt+上下
        text.bind('<Alt-Right>', lambda e: ch.Move(e.widget,  1))


        for c in '([{\'"':
            text.bind('<%s>'%c, SmartPairing) # '<KeyRelease-%s>'%c

        text.bind('<F6>', self.RunSelected)
        text.bind('<F2>', OnTest)
        text.bind('<Double-Button-1>', SmartSelect)
        self.text_frame.bind('<FocusIn>', self.ReloadFile)

        text.bind('<<my-function>>', lambda e: print('myfun', e))

        # 历史剪切板功能
        self.menu_clip = RecentClipboard(self)
        self.make_rmenu() # make "self.rmenu"
        self.rmenu.insert_cascade(3, label='History', menu=self.menu_clip)
        self.menudict['advance'].insert_cascade(3, label='Paste from History', menu=self.menu_clip)

        # 窗口操作
        menu_windows = WindowManager(self)
        self.menudict['advance'].insert_cascade(3, label='Window Manager', menu=menu_windows)

        # 文件操作
        menu_files = FileManager(self.root, self.text, self.io)
        self.menudict['advance'].insert_cascade(3, label='File Manager', menu=menu_files)


        try:
            import windnd
            windnd.hook_dropfiles(self.text, func=self.OpenFile)
        except:
            pass


    def copy(self, event):
        super().copy(event)
        self.menu_clip.Add()

    def _close(self):
        super()._close()
        # raise # TODO 是否还有别的方法阻止清空剪切



    def OpenFile(self, files):
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
        # TODO 未完成
        print(self.io.filename)


    def RunSelected(self, e): # ref: idlexlib.extensions.RunSelection
        code = self.text.get('sel.first', 'sel.last')
        if code.startswith(' '):
            code = 'if 1:\n' + code
        msg = '# Run Region [%s-%s]\n' % (self.text.index('sel.first'), self.text.index('sel.last'))
        shell = self.flist.open_shell()
        console = shell.interp.tkconsole
        console.text.insert('insert', msg)
        shell.interp.runcode(code)



class MyPyShellFileList(idlelib.pyshell.PyShellFileList):
    EditorWindow = MyPyShellEditorWindow


from .ReplaceBar import ReplaceBar
from .SmartSelect import SmartSelect, FixTextSelect
from .WindowManager import WindowManager
from .RecentClipboard import RecentClipboard


def run(filename=__file__):
    if filename:
        import sys
        sys.argv.append(filename) # Idea from "~\Lib\tkinter\__main__.py"
        # sys.argv.append(r'F:\lsx\coding\监控\udp.py')
    idlelib.pyshell.PyShellFileList = MyPyShellFileList
    main()



if __name__ == '__main__':
    # import idlexlib.extensionManager
    # import idlexlib.idlexMain


    if 'main':
        import sys
        sys.argv.append(__file__) # Idea from "~\Lib\tkinter\__main__.py"
        # sys.argv.append(r'F:\lsx\coding\监控\udp.py')
        idlelib.pyshell.PyShellFileList = MyPyShellFileList
        main()

    else:
        root = tk.Tk()
        root.withdraw()
        myfixwordbreaks(root)

        if 'use_flist':
            idlelib.pyshell.use_subprocess = True # 什么用途?
            flist = PyShellFileList(root)
            edit = MyPyShellEditorWindow(flist)
            edit.text.insert('insert', open(__file__, encoding='u8').read())

        print(edit.text.tag_names())

        root.mainloop()


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
