'''搜索替换工具条'''

# TEST TEXT
# A quick brown fox
# JuMp oVeR THE lazy dog
# 1377
# [a-z]+

# TODO 处理好和纵向滚动条的相对位置问题
# TODO shell中的stdout无法匹配
# TODO pat == '' 时报错提示


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import tkinter as tk

import sys
PY37 = sys.version_info > (3, 7)
if sys.version_info > (3, 6):
    from idlelib import searchengine
    from idlelib.replace import ReplaceDialog
else:
    # TODO 兼容 PY34
    from idlelib.SearchDialog import _setup


class ReplaceBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.text_frame)

        self.root = parent.root
        self.text = parent.text

        self.engine = engine = searchengine.get(self.root)
        self.replace = replace = ReplaceDialog(self.root, engine)

        # hot fix for `dialog.open(text)` effect called in `idlelib.replace.replace`
        replace.text = self.text
        replace.ok = 1
        replace.bell = parent.top.bell

        engine.patvar .trace('w', self.Update)
        engine.revar  .trace('w', self.Update)
        engine.casevar.trace('w', self.Update)
        engine.wordvar.trace('w', self.Update)

        t1 = tk.Entry(self, width=8, textvariable=engine.patvar)
        t2 = tk.Entry(self, width=8, textvariable=replace.replvar)
        tk.Label(self, text='Find:').pack(side='left')
        t1.pack(side='left', fill='x', expand=True)
        tk.Label(self, text='Repl:').pack(side='left')
        t2.pack(side='left', fill='x', expand=True)

        self.tip = tk.Label(self, text=' Match: 0')
        self.tip.pack(side='left')

        tk.Checkbutton(self, text='Re', variable=engine.revar)  .pack(side='left')
        tk.Checkbutton(self, text='Cc', variable=engine.casevar).pack(side='left')
        tk.Checkbutton(self, text='Wd', variable=engine.wordvar).pack(side='left')

        tk.Button(self, relief='groove', text='<<', command=lambda: self.Find(0)).pack(side='left')
        tk.Button(self, relief='groove', text='>>', command=lambda: self.Find(1)).pack(side='left')
        tk.Button(self, relief='groove', text='Replace', command=self.Replace).pack(side='left')
        tk.Button(self, relief='groove', text='Replace All', command=self.ReplaceAll).pack(side='left')

        self.text.bind('<<replace-bar-show>>', self.Flip)
        self.text.event_add('<<replace-bar-show>>', '<Key-Escape>') # add event but not clear exist bindings.
        t1.bind('<Escape>', self.Flip)
        t2.bind('<Escape>', self.Flip)

        self.show = False
        self.Flip(-1)

    def Flip(self, evt):
        self.show = not self.show
        if self.show:
            if PY37:
                self.grid(row=3, column=1, sticky='nsew')
            else:
                self.pack(fill='x', side='bottom')
            self.Update()
        else:
            if PY37:
                self.grid_forget()
            else:
                self.forget()
            self.text.tag_remove('hit', '1.0', 'end')
            self.text.focus()

    def Update(self, *args):
        self.text.tag_remove('hit', '1.0', 'end')
        self.tip.config(text=' Match: 0')

        if not self.engine.getpat():
            return

        s = self.text.get('1.0', 'end-1c')
        insert = len(self.text.get('1.0', 'insert'))
        prog = self.engine.getprog()
        matchs = [m.span() for m in prog.finditer(s)]
        self.tip.config(text=' Match: %d' % len(matchs))
        for n, (p1, p2) in enumerate(matchs):
            if p1 <= insert < p2:
                self.tip.config(text=' Match: %d/%d' % (n + 1, len(matchs)))
            self.text.tag_add('hit', '1.0+%dc' % p1, '1.0+%dc' % p2)

    def Find(self, forward):
        self.engine.wrapvar.set(True)
        self.engine.backvar.set(not forward)
        self.replace.find_it()
        self.Update()

    def Replace(self):
        self.replace.default_command()
        self.text.after(5, self.Update) # TODO unknown reason

    def ReplaceAll(self):
        # TODO 替换选区部分内容
        self.replace.replace_all()
        self.text.after(5, self.Update) # TODO unknown reason
