'''光标记录'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class CursorHistory:
    def __init__(self, parent):
        self.text = parent.text
        self.pointer = 0
        self.history = ['1.0'] # TODO 第一次是1.0或上次关闭前记录的位置
        self.Binding()

        if parent.amenu.index('end') is not None:
            parent.amenu.insert_separator(0)
        parent.amenu.insert_command(0, label='Forward', command=lambda: self.Move(1))
        parent.amenu.insert_command(0, label='Back', command=lambda: self.Move(-1))

    def Add(self, e):
        # TODO 当文本变化时平移历史记录
        # TODO 记录文件名+位置
        # TODO 只记录行数
        cur = self.text.index('insert')
        if cur != self.history[self.pointer]:
            self.pointer += 1
            self.history = self.history[:self.pointer] + [cur]

    def Move(self, n):
        if -1 < self.pointer + n < len(self.history):
            self.pointer += n
            self.text.see(self.history[self.pointer])
            self.text.mark_set('insert', self.history[self.pointer])
        return 'break'

    def Binding(self):
        text = self.text
        text.bind('<ButtonRelease-1>', self.Add, add=True)
        text.bind('<Alt-Left>',  lambda e: self.Move(-1))
        text.bind('<Alt-Right>', lambda e: self.Move(1))
