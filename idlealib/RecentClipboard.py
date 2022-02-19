'''历史剪切板'''

# TODO 不能在多个IDLE中共享


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import tkinter as tk


class RecentClipboard(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.text = parent.text
        self.root = parent.root

        self.data = []

        self.Binding()
        self.Add()

        parent.rmenu.insert_cascade(3, label='History', menu=self)
        parent.amenu.insert_cascade(3, label='Paste from History', menu=self)

        try:
            self.Add(parent.top.clipboard_get())
        except: # 当剪切板为图像时无法获取
            pass

        parent.before_copy.append(self.Add)

    def Add(self, s=''):
        s = s or self.text.get('sel.first', 'sel.last')

        if not s: # empty string
            return

        if s in self.data:
            self.data.remove(s)
        self.data.insert(0, s)

        self.delete(0, 'end')
        for i, s in enumerate(self.data): # TODO 限制个数
            label, callback = self.Prep(s)
            self.add_command(label=label, command=callback) # TODO 增加0-9A-Z快捷键

    def Prep(self, s):
        def paste():
            self.root.clipboard_clear()
            self.root.clipboard_append(s)
            self.text.event_generate('<<Paste>>')
            self.Add(s)

        s1 = s.replace('\n', '\\n')
        if len(s1) > 45:
            s1 = s1[:20] + ' ... ' + s1[-20:]
        s2 = 'len: %d, %s' % (len(s), s1)

        return s2, paste

    def Post(self, e):
        x0, y0 = self.text.winfo_rootx(), self.text.winfo_rooty()
        x, y, w, h = self.text.bbox('insert')
        self.post(x0 + x, y0 + y + h)

    def Binding(self):
        self.text.bind('<Control-Shift-V>', self.Post)
