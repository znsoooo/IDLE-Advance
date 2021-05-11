import re, os
import time
from idlelib.config import idleConf
from idlelib.editor import EditorWindow
from idlelib.mainmenu import menudefs
import tkinter as tk

h = help

from pprint import pprint



class CursorHistory:
    def __init__(self, text):
        self.text = text
        self.pointer = 0
        self.history = ['1.0']


    def Add(self, e):
        # DOTO 当文本变化时平移历史记录
        # TODO 记录文件名+位置
        cur = self.text.index('insert')
        if cur != self.history[self.pointer]:
            self.pointer += 1
            self.history = self.history[:self.pointer] + [cur]


    def Move(self, n):
        if -1 < self.pointer + n < len(self.history):
            self.pointer += n
            text.see(self.history[self.pointer])
            tag = '-1c' if n > 0 else '+1c' # TODO 当用快捷键操作时会多运动一个字符
            text.mark_set('insert', self.history[self.pointer] + tag)



class ReplaceBar(tk.Frame):
    def __init__(self, master=None, text=None):
        tk.Frame.__init__(self, master)

        self.text = text

        # TODO 从idle中获取设置
        self.patvar  = tk.StringVar(self, '')     # search pattern
        self.replvar = tk.StringVar(self, '')     # replace string
        self.revar   = tk.BooleanVar(self, False) # regular expression?
        self.casevar = tk.BooleanVar(self, False) # match case?
        self.wordvar = tk.BooleanVar(self, False) # match whole word?
        self.backvar = tk.BooleanVar(self, False) # search backwards?

        self.patvar .trace('w', self.Setting)
        self.replvar.trace('w', self.Setting)
        self.revar  .trace('w', self.Setting)
        self.casevar.trace('w', self.Setting)
        self.wordvar.trace('w', self.Setting)
        self.backvar.trace('w', self.Setting)

        tk.Label(self, text='Find:').pack(side='left')
        tk.Entry(self, width=8, textvariable=self.patvar).pack(side='left', fill='x', expand=True)
        tk.Label(self, text='Repl:').pack(side='left')
        tk.Entry(self, width=8, textvariable=self.replvar, validatecommand=self.Find).pack(side='left', fill='x', expand=True)

        self.tip = tk.Label(self, text=' Match: 0/0')
        self.tip.pack(side='left')

        tk.Checkbutton(self, text='Re',   variable=self.revar)  .pack(side='left')
        tk.Checkbutton(self, text='Case', variable=self.casevar).pack(side='left')
        tk.Checkbutton(self, text='Word', variable=self.wordvar).pack(side='left')

        tk.Button(self, relief='groove', text='<<', command=self.Prev).pack(side='left')
        tk.Button(self, relief='groove', text='>>', command=self.Next).pack(side='left')
        tk.Button(self, relief='groove', text='Replace', command=self.Replace).pack(side='left')
        tk.Button(self, relief='groove', text='Replace All', command=self.ReplaceAll).pack(side='left')


    def Setting(self, *_):
        self.Find()


    def Find(self, move=0):
        self.text.tag_remove('hit', '1.0', 'end')
        self.tip.config(text=' Match: 0/0')

        pat = self.patvar.get()
        if not pat:
            return

        s    = self.text.get('1.0', 'end')
        cur  = self.text.index('insert')
        pos  = Cur2Pos(s, cur) 

        repl = self.replvar.get()
        back = self.backvar.get()

        if not self.casevar.get():
            s = s.lower()
            pat = pat.lower()

        if self.wordvar.get():
            pat = r'\b' + pat + r'\b'

        if not self.revar.get():
            pat = pat # TODO 转义正则关键词
            repl = repl

        # high light matchs
        cnt = 0
        now = 0
        matchs = []
        for m in re.finditer(pat, s):
            cnt += 1
            p1, p2 = m.span()
            matchs.append((p1, p2))
            if not now and pos <= p1: # 记录第一次pos<=p1的值
                now = cnt # cnt最小是1
            self.text.tag_add('hit', Pos2Cur(s, p1), Pos2Cur(s, p2))

        # show tip
        self.tip.config(text=' Match: %d/%d'%(now, cnt))

        if matchs:
            new = (now - 1 + move) % len(matchs)
            SelectAndSee(self.text, matchs[new])


    def Prev(self):
        self.backvar.set(True)
        self.Find(-1)


    def Next(self):
        self.backvar.set(False)
        self.Find(1)


    def Replace(self):
        self.Find()
        

    def ReplaceAll(self):
        self.Find()




def fixwordbreaks(root):
    # On Windows, tcl/tk breaks 'words' only on spaces, as in Command Prompt.
    # We want Motif style everywhere. See #21474, msg218992 and followup.
    tk = root.tk
##    tk.call('tcl_wordBreakAfter', 'a b', 0) # make sure word.tcl is loaded
    s = r',=\(\)\[\]\{\}'
##    tk.call('set', 'tcl_wordchars', '[%s]'%s)
##    tk.call('set', 'tcl_nonwordchars', '[^%s]'%s) # lsx: Crtl+Del will del until end with nonwordchars
    tk.call('set', 'tcl_wordchars', '\w')
    tk.call('set', 'tcl_nonwordchars', '\W')

# print(re.sub(rb'\w', b'', bytes(range(128))))



##################
## About Cursor ##
##################


def Pos2Cur(s, pos):
    ss = s[:pos].split('\n')
    cur = '%d.%d'%(len(ss), len(ss[-1]))
    return cur


def Cur2Pos(s, cur):
    ln, col = map(int, cur.split('.'))
    ss = s.split('\n')[:ln]
    ss[-1] = ss[-1][:col] # 如果不还原ss而直接计算前ln行+col,可能造成第1行的转换错误
    pos = len('\n'.join(ss))
    return pos


def SelectFromCurrent(text, n):
    text.mark_set('insert', 'current')
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', 'current', 'current+%dc'%(n+1))


def SelectMultiLines(text, ln, rows):
    cur = '%d.0'%ln
    text.mark_set('insert', cur)
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', cur, cur+'+%dl'%rows)


def SelectAndSee(text, span):
    s = text.get('1.0', 'end')
    c1, c2 = Pos2Cur(s, span[0]), Pos2Cur(s, span[1])
    text.mark_set('insert', c1)
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', c1, c2)
    text.see(c1)



#########


def FindKey(key='', root=r'C:\Users\lenovo\AppData\Local\Programs\Python\Python36\Lib\idlelib'):
    for root, folders, files in os.walk(root):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'rb') as f:
                    s = f.read()
                    try:
                        s = s.decode()
                    except:
                        s = s.decode('gbk')
                for line in re.findall(key, s):
                    print(file, line.strip())

# FindKey(r'.*?\bparen\b.*')




def PrintTags():
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


def OnAction(e):
    SaveCursor(text)

def OnDoubleLeftRelease(e):
    print(e)
    SmartSelect(text)


def OnLeftRelease(e):
    CursorSave()


def SearchWords(text):
    # TODO 滚轮控制在多个结果中移动查看，如果选中不是完整单词是否仍进行匹配？
    # TODO 返回当前选中的匹配序号
    # TODO 换个颜色（不是hit）（参考：notepad++是深绿和浅绿）
    # TODO 匹配空格时速度很慢
    text.tag_remove('hit', '1.0', 'end')
    cnt = 0
    if text.tag_ranges('sel'):
        s  = text.get('1.0', 'end')
        s1 = text.selection_get()
        for m in re.finditer(r'\b%s\b'%s1, s): # TODO 当s1中存在正则语法时会错误
            cnt += 1
            p1, p2 = m.span()
            text.tag_add('hit', Pos2Cur(s, p1), Pos2Cur(s, p2))
    return cnt


def SmartSelect(text):
    # TODO 遇到注释文本的问题
    cur = text.index('current') # 当用insert时光标位置为自动选区的最开始
    ln, col = map(int, cur.split('.'))

    ss = text.get('%d.0'%ln, 'end').split('\n')
    line = ss[0]
    indent = re.match(r' *', line).end()
    empty = not line.split('#')[0].strip()

    if col <= indent: # cursor postion
        for row in range(1, len(ss)):
            begin = ss[row] if empty else ss[row][:indent+1] # empty代表无穷缩进
            if begin.split('#')[0].strip() != '' or empty: # 起始时是empty则只选中一行
                break
        SelectMultiLines(text, ln, row)

    else:
        # TODO 智能选取引号内全部内容/智能选取括号内内容/选区不换行/连续选中空格
        s = text.get('current', 'end')
        if s[0] in '([{':
            # TODO 使用idle内建的方法 idlelib.pyparse idlelib.parenmatch
            # 字符串内、转义引号的问题
            # 右括号匹配
            lv = 0
            for i, c in enumerate(s):
                if c in '([{':
                    lv += 1
                elif c in ')]}':
                    lv -= 1
                if lv == 0:
                    SelectFromCurrent(text, i)
                    break

        elif s[0] == ',':
            # TODO 两个括号的问题：(a, b())
            for i, c in enumerate(s[1:]):
                if c in ',)]}\n':
                    SelectFromCurrent(text, i)
                    break

        elif s[0] in '\'"':
            # 转义引号的问题，3引号的问题，选中第二个引号的问题
            # 参考 idlelib.colorizer
            i = s.find(s[0], 1)
            SelectFromCurrent(text, i)

        elif s[0] == '#':
            # TODO 注释前的空格
            i = s.find('\n', 1) - 1
            SelectFromCurrent(text, i)

        elif s[0] == '\n':
            SelectMultiLines(text, ln, 1)

        elif re.match('\W', s[0]):
            m = re.match('[^\w\n]+(\w+)?', s)
            i = m.end() - 1
            SelectFromCurrent(text, i)

##help(tk.Tk.bind)

mymenudef = ('advance', [
   ('Open Folder', '<<my-function>>'),
   ('Open CMD', '<<my-function>>'),
   ('Copy Fullname', '<<my-function>>'),
   None,
   ('Back', '<<my-function>>'),
   ('Forward', '<<my-function>>'),
   None,
   ('Hightlight Word', '<<highlight-word>>'),
   ('Smart Select', '<<smart-select>>'),
   None,
   ('!Spined Replace Bar', '<<my-function>>'),
   None,
   ('Run Selected', '<<my-function>>'),
   None,
   ('History Clipboard', '<<my-function>>'),
   None,
   ('Recent Changed Files', '<<my-function>>'),
   ('Reload File', '<<my-function>>'),
   ])

menudefs.append(mymenudef)







class MyEditorWindow(EditorWindow):
    def __init__(self, root):
        super().__init__(root=root)
        ReplaceBar(self.text_frame, self.text).pack(fill='x', side='bottom')


    def createmenubar(self):
        self.menu_specs.append(('advance', 'Advance'))
        super().createmenubar()






if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    import idlelib.searchengine as searchengine
    from idlelib.searchbase import SearchDialogBase
    from idlelib.replace import ReplaceDialog


    fixwordbreaks(root)
    edit = MyEditorWindow(root=root)
    text = edit.text


    ch = CursorHistory(text)
    text.bind('<ButtonRelease-1>', ch.Add)
    text.bind('<Alt-Left>',  lambda e: ch.Move(-1)) # TODO 兼容Alt+上下
    text.bind('<Alt-Right>', lambda e: ch.Move( 1))

    text.bind('<Control-`>', OnAction)
    # text.bind('<MouseWheel>', print) # for test
    text.bind('<Double-ButtonRelease-1>', OnDoubleLeftRelease)

    text.insert('insert', open(__file__, encoding='u8').read())

    print(text.tag_names())

    root.mainloop()


