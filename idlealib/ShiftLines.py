"""平移多行"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class ShiftLines:
    def __init__(self, parent):
        self.text = parent.text
        self.text.bind('<Alt-Up>', self.callback)
        self.text.bind('<Alt-Down>', self.callback)

    def callback(self, evt):
        text = self.text
        if not text.tag_ranges('sel'):
            text.tag_add('sel', 'insert linestart', 'insert+1l linestart')
        else:
            text.tag_add('sel', 'sel.first linestart', 'sel.last-1c+1l linestart')
        text.mark_set('insert', 'sel.first')
        text.undo_block_start()
        if evt.keysym == 'Up':
            s = text.get('sel.first-1l', 'sel.first')
            text.delete('sel.first-1l', 'sel.first')
            text.insert('sel.last', s)
        else:
            s = text.get('sel.last', 'sel.last+1l')
            text.delete('sel.last', 'sel.last+1l')
            text.insert('sel.first', s)
        text.undo_block_stop()
        return 'break'
