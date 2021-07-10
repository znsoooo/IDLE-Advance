'''搜索替换工具条'''

# TODO 处理好和纵向滚动条的相对位置问题


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re
import tkinter as tk
from idlexx.test.util import Pos2Cur, Cur2Pos, SelectSpan # TODO 相对导入问题


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


class ReplaceBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.text_frame)

        self.text = parent.text

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

        self.pack(fill='x', side='bottom')

    def Setting(self, *args):
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

    def Highlight(self):
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


if __name__ == '__main__':
    s = bytes(range(128)).decode()
    pat, repl = PrepFind('', s, s)
    print('PrepFind Test Patt:', s == re.sub(pat, '', s))
    print('PrepFind Test Repl:', s == re.sub('1', repl, '1'))
