class CursorHistory:
    def __init__(self, text):
        self.text = text
        self.pointer = 0
        self.history = ['1.0']
        self.Binding()

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

    def Binding(self):
        text = self.text
        text.bind('<ButtonRelease-1>', self.Add) # TODO 会抹掉CodeBrowser.py中的鼠标点击事件（右下角行号不更新）
        text.bind('<Alt-Left>',  lambda e: self.Move(text, -1)) # TODO 兼容Alt+上下
        text.bind('<Alt-Right>', lambda e: self.Move(text,  1))