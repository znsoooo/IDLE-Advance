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
PY36 = sys.version_info > (3, 6)
if PY36:
    from idlelib import searchengine
    from idlelib.replace import ReplaceDialog
    from idlelib.search import _setup
else:
    import idlelib.SearchEngine as searchengine
    from idlelib.ReplaceDialog import ReplaceDialog
    from idlelib.SearchDialog import _setup


jn = lambda x,y: '%i.%i'%(x,y) # Good!
lc = lambda s: jn(s.count('\n')+1, len(s)-s.rfind('\n')-1) # Good!


class ReplaceBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.text_frame)

        self.root = parent.root
        self.text = parent.text
        self.text.replace_bar = self # hook

        self.engine = engine = searchengine.get(self.root)
        self.replace = replace = ReplaceDialog(self.root, engine)

        # hot fix for `dialog.open(text)` effect called in `idlelib.replace.replace`
        replace.text = self.text
        replace.ok = 1
        replace.bell = parent.top.bell

        # class `SearchDialog` is separate with `ReplaceDialog`
        search = _setup(self.text)
        search.open = self.Open

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
        self.t1 = t1

        self.tip = tk.Label(self, text=' Match: 0')
        self.tip.pack(side='left')

        tk.Checkbutton(self, text='Re', variable=engine.revar)  .pack(side='left')
        tk.Checkbutton(self, text='Cc', variable=engine.casevar).pack(side='left')
        tk.Checkbutton(self, text='Wd', variable=engine.wordvar).pack(side='left')

        tk.Button(self, relief='groove', text='<<', command=lambda: self.Find(0)).pack(side='left')
        tk.Button(self, relief='groove', text='>>', command=lambda: self.Find(1)).pack(side='left')
        tk.Button(self, relief='groove', text='Replace', command=self.Replace).pack(side='left')
        tk.Button(self, relief='groove', text='Replace All', command=self.ReplaceAll).pack(side='left')

        self.text.bind("<<replace>>", self.OnReplace)

        self.text.bind('<Key-Escape>', self.Hide)
        t1.bind('<Escape>', self.Hide)
        t2.bind('<Escape>', self.Hide)

    def OnReplace(self, evt):
        self.text.event_generate('<<find>>')
        return 'break'

    def Open(self, text, string=None):
        bar = text.replace_bar
        if PY37:
            bar.grid(row=3, column=1, sticky='nsew')
        else:
            bar.pack(fill='x', side='bottom')

        if string:
            bar.engine.setpat(string)
        bar.t1.focus()
        bar.t1.select_range(0, 'end')  # don't use `t1.select_to('end')`. 选中区域为空时，输入字符后无法删除（移动光标后可以删除）
        bar.t1.icursor('end')

    def Hide(self, evt):
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
            self.text.tag_add('hit', lc(s[:p1]), lc(s[:p2])) # 如果使用`1.0+nc`字符偏移会命中Squeezer导致错位

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
