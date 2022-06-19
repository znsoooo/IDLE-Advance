"""大小写转换"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class UpperCase:
    def __init__(self, parent):
        self.text = parent.text
        self.text.bind('<Control-u>', self.callback)

    def callback(self, evt):
        text = self.text
        if text.tag_ranges('sel'):
            old = text.get('sel.first', 'sel.last')
            st = text.index('sel.first')
            ed = text.index('sel.last')
            s1 = old.lower()
            s2 = old.upper()
            if s1 != old:
                self.replace(st, ed, s1)
            elif s2 != old:
                self.replace(st, ed, s2)

    def replace(self, st, ed, s):
        text = self.text
        text.undo_block_start()
        text.delete(st, ed)
        text.insert(st, s)
        text.tag_add('sel', st, ed)
        text.mark_set('insert', st)
        text.undo_block_stop()
