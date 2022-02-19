"""纵向选择"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


from tkinter.simpledialog import askstring

# See: "~\tcl\tk8.6\text.tcl"
tcl1 = 'bind Text <B1-Motion> {set tk::Priv(x) %x; set tk::Priv(y) %y; tk::TextSelectTo %W %x %y}'
tcl2 = 'bind Text <B1-Motion> {tk::TextButton1 %W %x %y; %W tag remove sel 0.0 end}'

sp = lambda c: eval(c.replace('.',',')) # Good!
jn = lambda x,y: '%i.%i'%(x,y) # Good!
sort = lambda p1, p2: ((min(p1[0], p2[0]), min(p1[1], p2[1])), (max(p1[0], p2[0]), max(p1[1], p2[1])))


def enable(func):
    def wrapper(self, *args, **kwargs):
        if self.enable:
            return func(self, *args, **kwargs)
    return wrapper


class SelectVertical:
    def __init__(self, parent):
        self.text = parent.text
        self.root = parent.root

        self.enable = False

        self.text.bind('<Button-1>',        self.down)
        self.text.bind('<ButtonRelease-1>', self.up)
        self.text.bind('<B1-Motion>',       self.move)

        # self.text.bind('<KeyPress-Alt_L>',   self.setup)
        # self.text.bind('<KeyRelease-Alt_L>', self.cancel)

        parent.rmenu.add_separator()
        parent.rmenu.add_command(label='Select Vertical', command=self.setup)
        parent.add_adv_menu('Select Vertical', self.setup)

    def index(self, tag):
        return eval(self.text.index(tag).replace('.', ','))

    def setup(self, evt=-1):
        self.root.eval(tcl2)
        self.enable = True

    def cancel(self, evt=-1):
        self.root.eval(tcl1)
        self.enable = False

    def _down(self):
        self.p1 = self.index('insert')

    @enable
    def down(self, evt):
        self.text.after_idle(self._down)

    @enable
    def up(self, evt):
        self.p2 = self.index('insert')
        self.text.after_idle(self.select, self.p1, self.p2)
        if self.p1[0] != self.p2[0]: # multi-line selected
            s = askstring('Change to?', 'Input text:', parent=self.root)
            self.replace(self.p1, self.p2, s)
            self.text.focus() # grab focus after askstring dialog
            self.cancel()

    @enable
    def move(self, evt):
        p2 = self.index('insert')
        self.text.after_idle(self.select, self.p1, p2)

    def span(self, p1, p2):
        p1, p2 = sort(p1, p2)
        for r in range(p1[0], p2[0] + 1):
            yield jn(r, p1[1]), jn(r, p2[1])

    def select(self, p1, p2):
        for c1, c2 in self.span(p1, p2):
            self.text.tag_add('sel', c1, c2)

    def replace(self, p1, p2, new):
        text = self.text
        if new is None: # click cancel
            s = [text.get(c1, c2) for c1, c2 in self.span(p1, p2)]
            text.clipboard_clear()
            text.clipboard_append('\n'.join(s))
        else:
            text.undo_block_start()
            [text.delete(c1, c2) for c1, c2 in self.span(p1, p2)]
            text.undo_block_stop()
        if new: # do copy
            text.undo_block_start()
            [text.insert(c1, new) for c1, c2 in self.span(p1, p2)]
            text.undo_block_stop()
