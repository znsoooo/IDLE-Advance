
import os
import re

import tkinter as tk

from idlelib.config import idleConf
from idlelib.mainmenu import menudefs
from idlelib.pyshell import main, PyShellFileList, PyShellEditorWindow
import idlelib.pyshell
import idlelib.editor

from pprint import pprint



##################
## About Cursor ##
##################


def Cur2Lc(cur):
    return tuple(map(int, cur.split('.')))


def Pos2Cur(s, pos):
    ss = s[:pos].split('\n')
    cur = '%d.%d'%(len(ss), len(ss[-1]))
    return cur


def Cur2Pos(s, cur):
    ln, col = Cur2Lc(cur)
    ss = s.split('\n')[:ln]
    ss[-1] = ss[-1][:col] # 如果不还原ss而直接计算前ln行+col,可能造成第1行的转换错误
    pos = len('\n'.join(ss))
    return pos


def Select(text, c1, c2, ins=0):
    text.mark_set('insert', [c1, c2][ins])
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', c1, c2)


def SelectSpan(text, span, ins):
    s = text.get('1.0', 'end')
    p1, p2 = span
    c1, c2 = Pos2Cur(s, p1), Pos2Cur(s, p2)
    Select(text, c1, c2, ins)
    text.see(c1)


#########


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


def PrepFind(s, pat, repl, isre=False, case=True, word=False):
    if not isre: # TODO self test
        sp = '\\^$.*+?|()[]{}' # "\"需要放在最前面，否则会发生2次替换
        for c in sp:
            pat = pat.replace(c, '\\' + c)
        repl = repl.replace('\\', '\\\\')

##    if not case: # TODO 不区分大小写不应替换原始文本的大小写
##        s = s.lower()
##        pat = pat.lower()

    if word:  # "\b"在"去正则化"之后转换
        pat = r'\b' + pat + r'\b'

    return pat, repl


s = bytes(range(128)).decode()
pat, repl = PrepFind('', s, s)
print('PrepFind Test Patt:', s == re.sub(pat, '', s))
print('PrepFind Test Repl:', s == re.sub('1', repl, '1'))


class ReplaceBar(tk.Frame):
    def __init__(self, master=None, text=None):
        tk.Frame.__init__(self, master)

        self.text = text

        s = self

        # TODO 从idle中获取设置
        self.patvar  = tk.StringVar(self, '')     # search pattern
        self.replvar = tk.StringVar(self, '')     # replace string
        self.revar   = tk.BooleanVar(self, False) # regular expression?
        self.casevar = tk.BooleanVar(self, False) # match case?
        self.wordvar = tk.BooleanVar(self, False) # match whole word?
        self.backvar = tk.BooleanVar(self, False) # search backwards?

        self.patvar .trace('w', self.Setting) # TODO 绑定active事件
        self.replvar.trace('w', self.Setting)
        self.revar  .trace('w', self.Setting)
        self.casevar.trace('w', self.Setting)
        self.wordvar.trace('w', self.Setting)
        self.backvar.trace('w', self.Setting)

        tk.Label(self, text='Find:').pack(side='left')
        tk.Entry(self, width=8, textvariable=self.patvar).pack(side='left', fill='x', expand=True)
        tk.Label(self, text='Repl:').pack(side='left')
        tk.Entry(self, width=8, textvariable=self.replvar, validatecommand=self.Find).pack(side='left', fill='x', expand=True)

        self.tip = tk.Label(self, text=' Match: 0')
        self.tip.pack(side='left')

        tk.Checkbutton(self, text='Re',   variable=self.revar)  .pack(side='left')
        tk.Checkbutton(self, text='Case', variable=self.casevar).pack(side='left')
        tk.Checkbutton(self, text='Word', variable=self.wordvar).pack(side='left')

        tk.Button(self, relief='groove', text='<<', command=lambda: self.View(0)).pack(side='left')
        tk.Button(self, relief='groove', text='>>', command=lambda: self.View(1)).pack(side='left')
        tk.Button(self, relief='groove', text='Replace', command=self.Replace).pack(side='left')
        tk.Button(self, relief='groove', text='Replace All', command=self.ReplaceAll).pack(side='left')


    def Setting(self, *kw):
        self.Find()


    def Find(self):
        self.text.tag_remove('hit', '1.0', 'end')
        self.tip.config(text=' Match: 0')

        pat = self.patvar.get()
        if not pat:
            return

        # s = self.text.get('sel.first', 'sel.last')
        s = self.text.get('1.0', 'end')

        repl = self.replvar.get()
        back = self.backvar.get()

        pat, repl = PrepFind(s, pat, repl, self.revar.get(), self.casevar.get(), self.wordvar.get())
        matchs = [m.span() for m in re.finditer(pat, s)]
        self.tip.config(text=' Match: %d'%len(matchs))
        for p1, p2 in matchs:
            self.text.tag_add('hit', Pos2Cur(s, p1), Pos2Cur(s, p2))

        return matchs, s, pat, repl


    def Highlight(self, ):
        # TODO 未完成
        matchs = [m.span() for m in re.finditer(pat, s)]
        self.tip.config(text=' Match: %d'%len(matchs))
        for p1, p2 in matchs:
            self.text.tag_add('hit', Pos2Cur(s, p1), Pos2Cur(s, p2))


    def View(self, next):
        '''next: 1 -> forward, 0 -> backward'''
        # TODO 移动光标到选区边缘后继续查找
        self.backvar.set(not next)
        matchs, s, pat, repl = self.Find()
        if matchs:
            ins = Cur2Pos(s, self.text.index('insert'))
            now = sorted([p1 for p1, p2 in matchs] + [ins]).index(ins) - 1
            new = (now+next) % len(matchs)
            SelectSpan(self.text, matchs[new], next)
            self.tip.config(text=' Match: %d/%d' % (new+1, len(matchs)))


    def Replace(self):
        next = not self.backvar.get()
        if not self.text.get('sel.first', 'sel.last'):
            # TODO 如果选区未完全匹配表达式也不替换
            self.View(next)
            return # 第一次只匹配不替换
        self.ReplaceAll()
        self.View(next)


    def ReplaceAll(self):
        ss = self.text.get('sel.first', 'sel.last')
        if not ss:
            self.text.tag_add('sel', '1.0', 'end')

        s1 = self.text.get('sel.first', 'sel.last')
        matchs, s, pat, repl = self.Find()
        s2 = re.sub(pat, repl, s1)
        self.text.delete('sel.first', 'sel.last')
        self.text.insert('insert', s2) # TODO 光标移动到了最后
        # TODO 替换选中的部分




print(bytes(range(128)))
print(re.sub(rb'\w', b'', bytes(range(128))))



def FindKey(key, path='/lib/idlelib'):
    import sys
    for root, folders, files in os.walk(sys.base_prefix + path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), encoding='u8') as f:
                    s = f.read()
                for m in re.finditer(key, s):
                    print(file, Pos2Cur(s, m.start()), m.group().strip())

# FindKey(r'.*?\bCopy\b.*')
# FindKey(r'.*?\b\.tcl\b.*', path='/lib/tkinter')




def PrintTags(text):
    print(text.tag_names())
    for name in text.tag_names():
        print(name, text.tag_ranges(name))



#########


def GetRecentChangedFiles():
    # TODO 查看修改日期我之前是怎么写的？
    rf_path = os.path.join(idleConf.userdir, 'recent-files.lst')
    with open(rf_path, 'r', encoding='u8') as f:
        rf_list = f.read().splitlines()
    rf_list.sort(key=lambda p: os.stat(p).st_mtime if os.path.isfile(p) else 0, reverse=True)
    return rf_list

##print('\n'.join(GetRecentChangedFiles()))


def OnTest(e):
    print(e)
    print(type(e))
    print(e.widget)
    print(type(e.widget))


def CurrentInTag(text, tag):
    cur = text.index('current')
    pre = text.tag_prevrange(tag, cur)
    nex = text.tag_nextrange(tag, cur)
    if pre and (Cur2Lc(pre[0]) <= Cur2Lc(cur) < Cur2Lc(pre[1])):
        return pre
    if nex and (Cur2Lc(nex[0]) <= Cur2Lc(cur) < Cur2Lc(nex[1])):
        return nex


def MatchSpan(r, s, n):
    # TODO 当无匹配时的返回最近结果
    for m in re.finditer(r, s):
        if m.start() <= n <= m.end():
            return m.span()


def myfixwordbreaks(root):
    tk = root.tk
    tk.eval('bind Text <Double-1> {catch {%W mark set insert sel.first}}') #See  "~\tcl\tk8.6\text.tcl"


def FindParen(s, c1='(', c2=')'):
    lv = 0
    for n, c in enumerate(s):
        if c in c1:
            lv += 1
        elif c in c2:
            lv -= 1
        if lv == 0:
            return n


def SmartSelect(e):
    text = e.widget
    text.tag_remove('hit', '1.0', 'end')

    comment_or_string = CurrentInTag(text, 'COMMENT') or CurrentInTag(text, 'STRING')
    if comment_or_string: # TODO 注释前的空格
        c1, c2 = comment_or_string
        text.mark_set('insert', c1)
        text.tag_remove('sel', '1.0', 'end')
        text.tag_add('sel', c1, c2)
        return

    cur = text.index('current') # 当用insert时光标位置为自动选区的最开始
    # print(cur)
    ln, col = Cur2Lc(cur)

    ss = text.get(cur+' linestart', 'end').split('\n')
    line = ss[0]
    indent = re.match(r' *', line).end()
    empty = not line.split('#')[0].strip()

    if col <= indent: # cursor postion
        for row in range(1, len(ss)):
            begin = ss[row] if empty else ss[row][:indent+1] # empty代表无穷缩进
            if begin.split('#')[0].strip() != '' or empty: # 起始时是empty则只选中一行
                break
        Select(text, 'current linestart', 'current linestart+%dl'%row)

    else:
        c = text.get('current')
        if c == '\n':
            Select(text, 'current linestart', 'current linestart+1l')

        elif c == ' ':
            p1, p2 = MatchSpan(r' +', line, col)
            Select(text, 'current linestart+%dc'%p1, 'current linestart+%dc'%p2)

        elif c in '([{':
            # idle内自建的方法太复杂 idlelib.hyperparser.HyperParser.get_surrounding_brackets
            # TODO 字符串内、转义引号的问题
            c1 = c
            c2 = ')]}'['([{'.index(c1)]
            s = text.get('current', 'end')
            n = FindParen(s, c1, c2)
            Select(text, 'current', 'current+%dc'%(n+1))

        elif c in ')]}':
            c1 = c
            c2 = '([{'[')]}'.index(c1)]
            s = text.get('1.0', 'current+1c')
            n = FindParen(reversed(s), c1, c2)
            Select(text, 'current-%dc'%n, 'current+1c')

        elif c == ',':
            # TODO 两个括号的问题：(a, b())
            s = text.get('current', 'end')
            for n, c in enumerate(s[1:]):
                if c in ',{[()]}\n':
                    Select(text, 'current', 'current+%dc'%(n+1))
                    break

        elif re.match(r'\w', c):
            # TODO 换个颜色（不是hit）（参考：notepad++是深绿和浅绿）
            # TODO 选中后取消
            # TODO 一行中第一个word如果是一个字符无法选中（命中另一个规则）
            p1, p2 = MatchSpan(r'\w+', line, col)
            Select(text, 'current linestart+%dc'%p1, 'current linestart+%dc'%p2)
            word = line[p1:p2]
            s = text.get('1.0', 'end')
            for m in re.finditer(r'\b%s\b' % word, s):
                p1, p2 = m.span()
                text.tag_add('hit', Pos2Cur(s, p1), Pos2Cur(s, p2))

        elif re.match(r'\W', c):
            # 改善“s.split('\n')[:ln]”会匹配”')[:“的糟糕匹配体验
            p1, p2 = MatchSpan(r'[^\w\(\)\[\]\{\}\'" ]+', line, col) # 不"粘"括号空格和引号
            Select(text, 'current linestart+%dc'%p1, 'current linestart+%dc'%p2)


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



def RunSelected(e):
    ss = e.widget.get('sel.first', 'sel.last')
    if ss[-1] != '\n':
        ss += '\n' # 防止选中段尾空行提示信息多出一行引起困惑
    print('Run Selected Code with %d Lines.'%(ss.count('\n'))) # TODO 显示在shell中
    if ss.startswith(' '):
        ss = 'if 1:\n' + ss
    ret = exec(ss) # TODO 运行报错显示在shell中


mymenudef = ('advance', [
    ('Back', '<<my-function>>'),
    ('Forward', '<<my-function>>'),
    None,
    # ('History Clipboard', '<<my-function>>'),
    ('Recent Changed Files', '<<my-function>>'),
    None,
    ('Reload File', '<<my-function>>'),
    None,
    ('Open Folder', '<<my-function>>'),
    ('Open CMD', '<<my-function>>'),
    ('Copy Fullname', '<<my-function>>'),
    None,
    ('Run Selected', '<<my-function>>'),
    None,
    ('!Replace Bar', '<<my-function>>'),
    ])

menudefs.append(mymenudef)


class MyPyShellEditorWindow(PyShellEditorWindow):
    def __init__(self, flist=None, filename=None, key=None, root=None):
        super().__init__(flist, filename, key, root)
        text = self.text

        myfixwordbreaks(self.root)

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
            text.bind('<%s>'%c, SmartPairing)

        text.bind('<F6>', RunSelected)
        text.bind('<Double-Button-1>', SmartSelect)

        text.bind('<<my-function>>', lambda e: print('myfun', e))

        self.recent_clipboard_data = []
        self.recent_clipboard = tk.Menu(self.menubar, tearoff=0)
        self.menudict['advance'].insert_cascade(3, label='Paste from History', underline=0, menu=self.recent_clipboard)

        self.make_rmenu() # make "self.rmenu"
        self.rmenu.insert_cascade(3, label='History', underline=0, menu=self.recent_clipboard)


        try:
            import windnd
            windnd.hook_dropfiles(self.text, func=self.OpenFile)
        except:
            pass


    def createmenubar(self):
        self.menu_specs.append(('advance', 'Advance'))
        super().createmenubar()


    def copy(self, event):
        # super().copy(event) # TODO useless?
        s = self.text.get('sel.first', 'sel.last')
        if s: # 非空字符串
            self.recent_clipboard_add(s)


    def recent_clipboard_add(self, s):
        if s in self.recent_clipboard_data:
            self.recent_clipboard_data.remove(s)
        self.recent_clipboard_data.insert(0, s)

        menu = self.recent_clipboard
        menu.delete(0, 'end')
        for i, s in enumerate(self.recent_clipboard_data):
            callback = self.recent_clipboard_callback(s)
            s1 = s.replace('\n', '\\n')
            if len(s1) > 45:
                s1 = s1[:20] + ' ... ' + s1[-20:]
            menu.add_command(label='len: %d, %s'%(len(s), s1), command=callback, underline=0)


    def recent_clipboard_callback(self, s):
        def f():
            self.root.clipboard_clear()
            self.root.clipboard_append(s)
            self.text.event_generate('<<Paste>>')
            self.recent_clipboard_add(s)
        return f


    def OpenFile(self, files):
        for file_b in files:
            file = file_b.decode('gbk')
            if file.endswith('.py'):
                edit = self.flist.open(file)
                # TODO 由于滚动条存在导致有时候拖拽加载会闪退，增加下面两行可以避免
                edit.text.tag_add("sel", "insert", "insert+1c")
                edit.text.tag_remove("sel", "1.0", "end")



class MyPyShellFileList(idlelib.pyshell.PyShellFileList):
    EditorWindow = MyPyShellEditorWindow





if __name__ == '__main__':
    # import idlexlib.extensionManager
    # import idlexlib.idlexMain
    # help(tk.Tk.bind)

    import os

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
