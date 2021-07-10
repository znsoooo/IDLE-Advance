'''历史剪切板'''

# TODO 不能在多个IDLE中共享


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import tkinter as tk


class RecentClipboard(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.parent = parent
        self.data = []
        self.Add()
        self.Binding()

        parent.rmenu.insert_cascade(3, label='History', menu=self)
        parent.menudict['advance'].insert_cascade(3, label='Paste from History', menu=self)

        parent.after_copy.append(self.Add) # TODO 剪切时没有

    def Add(self):
        try:
            s = self.parent.top.clipboard_get()
        except: # 当剪切板为图像时无法获取
            return
        if not s: # 空字符串
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
            self.parent.root.clipboard_clear()
            self.parent.root.clipboard_append(s)
            self.parent.text.event_generate('<<Paste>>')
            self.Add()

        s1 = s.replace('\n', '\\n')
        if len(s1) > 45:
            s1 = s1[:20] + ' ... ' + s1[-20:]
        s2 = 'len: %d, %s' % (len(s), s1)

        return s2, paste

    def Post(self, e):
        self.post(e.x_root, e.y_root) # TODO 参考calltip_w.py获取光标的当前位置并弹出窗口

    def Binding(self):
        text = self.parent.text
        text.bind('<Control-Shift-V>', self.Post)
