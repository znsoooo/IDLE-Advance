'''搜索替换工具条'''

# TEST TEXT
# A quick brown fox
# JuMp oVeR THE lazy dog
# 1377
# [a-z]+

# TODO 处理好和纵向滚动条的相对位置问题
# TODO shell中的stdout无法匹配


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)

import sys
PY37 = sys.version_info > (3, 7)

import re
import tkinter as tk
from tkinter.messagebox import showinfo


def SelectSpan(text, span, ins):
    c1, c2 = '1.0+%dc' % span[0], '1.0+%dc' % span[1]
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', c1, c2)
    text.mark_set('insert', [c1, c2][ins])
    text.see(c1)


def PrepFind(pat, repl, isre=False, case=True, word=False):
    flag = re.M
    if not isre:
        pat = re.escape(pat)
        repl = re.escape(repl)
    if not case:
        flag |= re.I
    if word:  # surround "\b" after escape
        pat = r'\b%s\b' % pat
    return pat, repl, flag


class ReplaceBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.text_frame)

        self.root = parent.root

        self.show = True

        self.text = parent.text

        # TODO 从idle中获取设置
        self.patvar  = tk.StringVar(self, '')     # search pattern
        self.replvar = tk.StringVar(self, '')     # replace string
        self.revar   = tk.BooleanVar(self, False) # regular expression?
        self.casevar = tk.BooleanVar(self, False) # match case?
        self.wordvar = tk.BooleanVar(self, False) # match whole word?
        self.backvar = tk.BooleanVar(self, False) # search backwards?

        self.patvar .trace('w', self.Find) # TODO 绑定active事件
        self.replvar.trace('w', self.Find)
        self.revar  .trace('w', self.Find)
        self.casevar.trace('w', self.Find)
        self.wordvar.trace('w', self.Find)
        self.backvar.trace('w', self.Find)

        t1 = tk.Entry(self, width=8, textvariable=self.patvar)
        t2 = tk.Entry(self, width=8, textvariable=self.replvar)
        tk.Label(self, text='Find:').pack(side='left')
        t1.pack(side='left', fill='x', expand=True)
        tk.Label(self, text='Repl:').pack(side='left')
        t2.pack(side='left', fill='x', expand=True)

        self.tip = tk.Label(self, text=' Match: 0')
        self.tip.pack(side='left')

        tk.Checkbutton(self, text='Cc', variable=self.casevar).pack(side='left')
        tk.Checkbutton(self, text='Wd', variable=self.wordvar).pack(side='left')
        tk.Checkbutton(self, text='Re', variable=self.revar)  .pack(side='left')

        tk.Button(self, relief='groove', text='<<', command=lambda: self.View(0)).pack(side='left')
        tk.Button(self, relief='groove', text='>>', command=lambda: self.View(1)).pack(side='left')
        tk.Button(self, relief='groove', text='Replace', command=self.Replace).pack(side='left')
        tk.Button(self, relief='groove', text='Replace All', command=self.ReplaceSelected).pack(side='left')

        self.text.bind('<<replace-bar-show>>', self.Flip)
        self.text.event_add('<<replace-bar-show>>', '<Key-Escape>') # add event but not clear exist bindings.
        t1.bind('<Escape>', self.Flip)
        t2.bind('<Escape>', self.Flip)

        self.Flip(-1)

    def Flip(self, evt):
        self.show = not self.show
        if self.show:
            if PY37:
                self.grid(row=3, column=1, sticky='nsew')
            else:
                self.pack(fill='x', side='bottom')
            self.Find()
        else:
            if PY37:
                self.grid_forget()
            else:
                self.forget()
            self.text.tag_remove('hit', '1.0', 'end')
            self.text.focus()

    def Find(self, *args):
        self.text.tag_remove('hit', '1.0', 'end')
        self.tip.config(text=' Match: 0')

        pat = self.patvar.get()
        if not pat:
            return
        pat, repl, flag = PrepFind(pat, self.replvar.get(), self.revar.get(), self.casevar.get(), self.wordvar.get())

        # s = self.text.get('sel.first', 'sel.last')
        s = self.text.get('1.0', 'end-1c')
        matchs = [m.span() for m in re.finditer(pat, s, flag)]
        self.Highlight(matchs)

        return matchs, pat, repl, flag

    def Highlight(self, matchs):
        for p1, p2 in matchs:
            self.text.tag_add('hit', '1.0+%dc' % p1, '1.0+%dc' % p2)
        self.tip.config(text=' Match: %d' % len(matchs))

    def View(self, next):
        """next: 1 -> forward, 0 -> backward"""
        # TODO 移动光标到选区边缘后继续查找
        self.backvar.set(not next)
        matchs, pat, repl, flag = self.Find()
        if matchs:
            ins = len(self.text.get('1.0', 'insert')) # cursor offset
            now = sorted([p1 for p1, p2 in matchs] + [ins]).index(ins) - 1
            new = (now + next) % len(matchs)
            SelectSpan(self.text, matchs[new], next)
            self.tip.config(text=' Match: %d/%d' % (new + 1, len(matchs)))

    def Replace(self):
        next = not self.backvar.get()
        if self.text.get('sel.first', 'sel.last'):
            self.ReplaceSelected()
        self.View(next)
        # TODO 如果选区未完全匹配表达式也不替换
        # TODO 第一次只匹配不替换

    def ReplaceSelected(self):
        text = self.text

        save = text.index('insert')
        ss = text.get('sel.first', 'sel.last')
        if not ss:
            text.tag_add('sel', '1.0', 'end-1c')

        s1 = text.get('sel.first', 'sel.last')
        matchs, pat, repl, flag = self.Find()
        s2, n = re.subn(pat, repl, s1, flags=flag)

        text.undo_block_start()
        text.delete('sel.first', 'sel.last')
        text.insert('insert', s2) # TODO 光标移动到了最后
        text.undo_block_stop()

        showinfo('Replace', '%d places was replaced in selected text.' % n, parent=self.root)

