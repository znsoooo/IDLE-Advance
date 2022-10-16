'''匹配输入和删除成对括号'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


LEFT = '([{\'"`'
RIGHT = ')]}'
pair = lambda c: ')]}\'"`'['([{\'"`'.index(c)]


def GetSpan(text):
    sel = text.tag_ranges('sel')
    left = 'sel.first' if sel else 'insert'
    right = 'sel.last' if sel else 'insert'
    return left, right


class SmartPairing:
    def __init__(self, parent):
        self.text = parent.text
        for c in LEFT + RIGHT:
            self.text.bind('<%s>' % c, self.PairAdd)  # '<KeyRelease-%s>'%c
        self.text.bind('<BackSpace>', self.OnBackSpace)

    def PairAdd(self, evt):
        c = evt.char
        text = self.text

        if c in LEFT: # 输入左括号时输入匹配右括号，允许含有选区
            text.undo_block_start()

            if text.tag_ranges('sel'):
                c1 = text.get('sel.first')
                if c1 in LEFT and c1 != c and ((c1 in '([{') ^ (c in '\'"`')):
                    self.PairDelete()

            sel = text.tag_ranges('sel')
            left = 'sel.first' if sel else 'insert'
            right = 'sel.last' if sel else 'insert'

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

    def PairDelete(self): # 删除左括号时同时删除右括号
        text = self.text

        sel = text.tag_ranges('sel')
        left = 'sel.first' if sel else 'insert-1c'
        right = 'sel.last-1c' if sel else 'insert'

        c1 = text.get(left)
        c2 = text.get(right)

        if c1 in LEFT and c2 == pair(c1):
            text.undo_block_start()
            text.delete(right)
            text.delete(left)
            text.undo_block_stop()
            return True

    def OnBackSpace(self, evt):
        if not self.PairDelete():
            self.text.event_generate('<<smart-backspace>>')
        return 'break'
