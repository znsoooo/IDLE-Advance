'''匹配成对括号'''

# TODO 快速删除

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


def Pairing(e):
    # TODO 第一次输入右括号时移动光标但不键入
    # TODO 删除左括号时删除右括号（如果有的话）
    # TODO 有选区时输入括号不清除选区（包括光标位置）
    text = e.widget
    pair = ')]}\'"'['([{\'"'.index(e.char)]
    ss = e.widget.get('sel.first', 'sel.last')
    if ss:
        text.delete('sel.first', 'sel.last')
    text.mark_gravity('insert', 'left')
    text.insert('insert', pair)
    text.insert('insert', ss)
    text.mark_gravity('insert', 'right')


class SmartPairing:
    def __init__(self, parent):
        text = parent.text
        for c in '([{\'"':
            text.bind('<%s>' % c, Pairing)  # '<KeyRelease-%s>'%c
