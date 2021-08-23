'''智能选取'''

# TODO shell中的stdout无法匹配

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re

sp = lambda c: eval(c.replace('.',',')) # Good!


def Select(text, c1, c2):
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', c1, c2)
    text.mark_set('insert', c1)


def FixTextSelect(root):
    tk = root.tk
    tk.eval('bind Text <Double-1> {catch {%W mark set insert sel.first}}') # See: "~\tcl\tk8.6\text.tcl"


def CurrentInTag(text, tag):
    cur = text.index('current')
    pre = text.tag_prevrange(tag, cur)
    nex = text.tag_nextrange(tag, cur)
    if pre and (sp(pre[0]) <= sp(cur) < sp(pre[1])):
        return pre
    if nex and (sp(nex[0]) <= sp(cur) < sp(nex[1])):
        return nex


def FindParen(s, c1='(', c2=')'):
    lv = 0
    for n, c in enumerate(s):
        if c in c1:
            lv += 1
        elif c in c2:
            lv -= 1
        if lv == 0:
            return n


def MatchSpan(r, s, n):
    # TODO 当无匹配时的返回最近结果
    for m in re.finditer(r, s):
        if m.start() <= n <= m.end():
            return m.span()


def Selecting(e):
    text = e.widget
    text.tag_remove('hit', '1.0', 'end')

    comment_or_string = CurrentInTag(text, 'COMMENT') or CurrentInTag(text, 'STRING')
    if comment_or_string: # TODO 注释前的空格
        c1, c2 = comment_or_string
        text.mark_set('insert', c1)
        text.tag_remove('sel', '1.0', 'end')
        text.tag_add('sel', c1, c2)
        return

    cur = text.index('current') # 当用insert时光标位置为自动选区的最开始
    # print(cur)
    ln, col = sp(cur)

    ss = text.get(cur+' linestart', 'end').split('\n')
    line = ss[0]
    indent = re.match(r' *', line).end()
    empty = not line.split('#')[0].strip()

    if col <= indent: # cursor postion
        for row in range(1, len(ss)):
            begin = ss[row] if empty else ss[row][:indent+1] # empty代表无穷缩进
            if begin.split('#')[0].strip() != '' or empty: # 起始时是empty则只选中一行
                break
        Select(text, 'current linestart', 'current linestart+%dl' % row)

    else:
        c = text.get('current')
        if c == '\n':
            Select(text, 'current linestart', 'current linestart+1l')

        elif c == ' ':
            p1, p2 = MatchSpan(r' +', line, col)
            Select(text, 'current linestart+%dc' % p1, 'current linestart+%dc' % p2)

        elif c in '([{':
            # idle内自建的方法太复杂 idlelib.hyperparser.HyperParser.get_surrounding_brackets
            # TODO 字符串内、转义引号的问题
            c1 = c
            c2 = ')]}'['([{'.index(c1)]
            s = text.get('current', 'end')
            n = FindParen(s, c1, c2)
            Select(text, 'current', 'current+%dc' % (n + 1))

        elif c in ')]}':
            c1 = c
            c2 = '([{'[')]}'.index(c1)]
            s = text.get('1.0', 'current+1c')
            n = FindParen(reversed(s), c1, c2)
            Select(text, 'current-%dc' % n, 'current+1c')

        elif c == ',':
            # TODO 两个括号的问题：(a, b())
            s = text.get('current', 'end')
            for n, c in enumerate(s[1:]):
                if c in ',{[()]}\n':
                    Select(text, 'current', 'current+%dc' % (n + 1))
                    break

        elif re.match(r'\w', c):
            # TODO 换个颜色（不是hit）（参考：notepad++是深绿和浅绿）
            # TODO 选中后取消
            # TODO 一行中第一个word如果是一个字符无法选中（命中另一个规则）
            p1, p2 = MatchSpan(r'\w+', line, col)
            Select(text, 'current linestart+%dc' % p1, 'current linestart+%dc' % p2)
            word = line[p1:p2]
            s = text.get('1.0', 'end')
            for m in re.finditer(r'\b%s\b' % word, s):
                p1, p2 = m.span()
                text.tag_add('hit', '1.0+%dc' % p1, '1.0+%dc' % p2)

        elif re.match(r'\W', c):
            # 改善“s.split('\n')[:ln]”会匹配”')[:“的糟糕匹配体验
            p1, p2 = MatchSpan(r'[^\w\(\)\[\]\{\}\'" ]+', line, col) # 不"粘"括号空格和引号
            Select(text, 'current linestart+%dc' % p1, 'current linestart+%dc' % p2)


class SmartSelect:
    def __init__(self, parent):
        FixTextSelect(parent.root)
        parent.text.bind('<Double-Button-1>', Selecting)
