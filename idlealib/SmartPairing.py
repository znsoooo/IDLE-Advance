'''匹配输入和删除成对括号'''

# TODO 选中单侧括号并修改时同时修改匹配括号

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


LEFT = '([{\'"'
RIGHT = ')]}'
pair = lambda c: ')]}\'"'['([{\'"'.index(c)]


class SmartPairing:
    def __init__(self, parent):
        self.text = parent.text
        for c in LEFT + RIGHT:
            self.text.bind('<%s>' % c, self.PairAdd)  # '<KeyRelease-%s>'%c
        self.text.bind('<BackSpace>', self.PairDelete)

    def PairAdd(self, evt):
        c = evt.char
        text = self.text

        if c in LEFT: # 输入左括号时输入匹配右括号，允许含有选区
            sel = text.tag_ranges('sel')
            left = 'sel.first' if sel else 'insert'
            right = 'sel.last' if sel else 'insert'

            text.undo_block_start()
            text.insert(left, c)
            text.mark_gravity('insert', 'left')
            text.insert(right, pair(c))
            text.mark_gravity('insert', 'right')
            text.undo_block_stop()

            return 'break'

        elif c in RIGHT: # 输入右括号时移动光标但不键入
            if c == text.get('insert'):
                text.mark_set('insert', 'insert+1c')
                return 'break'

    def PairDelete(self, evt): # 删除左括号时同时删除右括号
        text = self.text
        c = text.get('insert-1c')
        if c in LEFT and pair(c) == text.get('insert'):
            text.delete('insert-1c', 'insert+1c')
            return 'break'
