'''搜索替换工具条'''

# TEST TEXT
# A quick brown fox
# JuMp oVeR THE lazy dog
# 1377
# [a-z]+

# TODO 处理好和纵向滚动条的相对位置问题


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re
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
sp = lambda c: eval(c.replace('.',',')) # Good!
lc = lambda s: jn(s.count('\n')+1, len(s)-s.rfind('\n')-1) # Good!


class ReplaceBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.text_frame)

        self.root = parent.root
        self.text = parent.text
        self.text.replace_bar = self # hook

        self.engine = engine = searchengine.get(self.root)
        self.replace = replace = ReplaceDialog(self.root, engine)
        self.show = False

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

        t1.bind('<FocusIn>', self.Update)
        self.text.bind('<Key-Escape>', self.Hide)
        t1.bind('<Escape>', self.Hide)
        t2.bind('<Escape>', self.Hide)

    def OnReplace(self, evt):
        self.text.event_generate('<<find>>')
        return 'break'

    def Open(self, text, string=None):
        # remove selection to avoid replacing only itself in `replace_all` function
        text.tag_remove('sel', '1.0', 'end-1c')

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
        bar.show = True
        bar.Update()

    def Hide(self, evt):
        if PY37:
            self.grid_forget()
        else:
            self.forget()
        self.text.tag_remove('hit', '1.0', 'end')
        self.text.focus()
        self.show = False

    def Update(self, *args):
        if not self.show:
            return

        self.text.tag_remove('hit', '1.0', 'end')
        self.tip.config(text=' Match: 0')

        # banning show error report temporarily
        _report_error = self.engine.report_error
        self.engine.report_error = lambda *v: None
        prog = self.engine.getprog()
        self.engine.report_error = _report_error

        if not prog:
            return

        s = self.text.get('1.0', 'end-1c')
        insert = len(self.text.get('1.0', 'insert'))
        matchs = [m.span() for m in re.finditer(prog.pattern, s, prog.flags | re.M)] # fix matches the end of lines
        self.tip.config(text=' Match: %d' % len(matchs))
        if len(matchs) < 1000:
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
        # Ref: idlelib.replace.replace_all
        text = self.text

        prog = self.engine.getprog()
        if not prog: return

        res = self.engine.search_text(text, prog)
        if not res: return

        text.undo_block_start()

        sel_first = text.index('sel.first')
        line, col = sp(text.index('sel.first') or '1.0')
        line3, col3 = sp(text.index('sel.last') or text.index('end-1c'))
        text.tag_remove('sel', '1.0', 'end')
        text.tag_remove('hit', '1.0', 'end')

        repl = self.replace.replvar.get()
        while 1:
            res = self.engine.search_forward(text, prog, line, col, 0)
            if not res: break

            line, m = res
            new = self.replace._replace_expand(m, repl)
            if new is None: break

            col1, col2 = m.span()
            col = col1 + len(new)
            if (line, col2) > (line3, col3):
                break
            if line == line3:
                col3 += col - col2

            first = jn(line, col1)
            last  = jn(line, col2)
            text.delete(first, last)
            text.insert(first, new)

        if sel_first:
            text.tag_add('sel', sel_first, jn(line3, col3))

        text.undo_block_stop()

        self.text.after(5, self.Update) # TODO unknown reason
