'''智能选取'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re

sp = lambda c: eval(c.replace('.',',')) # Good!
jn = lambda x,y: '%i.%i'%(x,y) # Good!
lc = lambda s: jn(s.count('\n')+1, len(s)-s.rfind('\n')-1) # Good!

is_code = lambda s: s.split('#')[0].strip()


def FixTextSelect(root):
    tk = root.tk
    tk.eval('bind Text <Double-1> {catch {%W mark set insert sel.first}}') # See: "~\tcl\tk8.6\text.tcl"


def Select(text, c1, c2):
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', c1, c2)
    text.mark_set('insert', c1)


def FindParen(s, c1='(', c2=')'):
    n1 = n2 = 0
    for n, c in enumerate(s):
        n1 += c in c1
        n2 += c in c2
        if n1 and n1 == n2:
            return n


def MatchSpan(r, s, n):
    for m in re.finditer(r, s):
        if m.start() <= n <= m.end():
            return m.span()


def LineType(line):
    indent = re.match(r' *', line).end()
    code = line[indent:]
    if code.startswith('#'):
        return indent, 'comment'
    elif code:
        return indent, 'code'
    else:
        return indent, 'empty'


def Selecting(e):
    text = e.widget
    text.tag_remove('hit', '1.0', 'end')

    if 'STRING' in text.tag_names('current'):
        st, ed = text.tag_prevrange('STRING', 'current+1c') # See: `idlelib.squeezer.Squeezer.squeeze_current_text_event`
        ed2 = text.index(ed + '-1c')
        cur = text.index('current')
        if cur in (st, ed2):
            return Select(text, st, ed)

    cur = text.index('current') # 当用insert时光标位置为自动选区的最开始
    col = sp(cur)[1]
    line = text.get('current linestart', 'current lineend')

    c = text.get('current') # charset: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    if c == ':':
        if is_code(line[col+1:]):
            Select(text, 'current', 'current+1c')
        else:
            indent = re.match(r' *', line).end()
            ss = text.get('current linestart+1l', 'end').split('\n')
            n = 1
            for r, row in enumerate(ss):
                indent2, typ = LineType(row)
                if typ == 'code' and indent2 <= indent:
                    break
                if typ != 'empty' and indent2 > indent:
                    n = r + 2
            Select(text, 'current linestart', 'current linestart+%dl' % n)

    elif c == ' ':
        indent = re.match(r' *', line).end()
        if col < indent:
            ss = text.get('current linestart+1l', 'end').split('\n')
            for n1, row in enumerate(ss):
                indent2, typ = LineType(row)
                if typ == 'empty':
                    break
            ss = text.get('1.0', 'current linestart-1c').split('\n')
            for n0, row in enumerate(reversed(ss)):
                indent2, typ = LineType(row)
                if typ == 'empty':
                    break
            Select(text, 'current linestart-%dl' % n0, 'current linestart+%dl' % (n1 + 1))
        else:
            p1, p2 = MatchSpan(r' +', line, col)
            Select(text, 'current linestart+%dc' % p1, 'current linestart+%dc' % p2)

    elif re.match(r'\w', c):
        p1, p2 = MatchSpan(r'\w+', line, col)
        Select(text, 'current linestart+%dc' % p1, 'current linestart+%dc' % p2)
        word = line[p1:p2]
        s = text.get('1.0', 'end')
        for m in re.finditer(r'\b%s\b' % word, s):
            p1, p2 = m.span()
            text.tag_add('hit', lc(s[:p1]), lc(s[:p2])) # 如果使用`1.0+nc`字符偏移会命中Squeezer导致错位

    elif c == '\n':
        Select(text, 'current linestart', 'current+1c')

    elif c == '#': # for # test # text #
        if 'COMMENT' in text.tag_names('current') and \
           text.index('current') == text.tag_prevrange('COMMENT', 'current+1c')[0]:
            p1, p2 = MatchSpan(r' *#', line, col)
            if p1 > 0:
                Select(text, 'current linestart+%dc' % p1, 'current lineend')
            else:
                Select(text, 'current linestart', 'current linestart+1l')
        else:
            Select(text, 'current', 'current+1c')

    elif c in '\'"`': # quote in comment
        s = text.get('current+1c', 'end')
        n = s.find(c)
        Select(text, 'current', 'current+%dc' % (n + 2))

    elif c in '([{':
        # idle内自建的方法太复杂 idlelib.hyperparser.HyperParser.get_surrounding_brackets
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

    elif c == '\\': # "\ooo" "\xhh" "\uxxxx" "\Uxxxxxxxx"
        c2 = text.get('current+1c')
        n = {'x': 4, 'u': 6, 'U': 10}.get(c2, 2)
        Select(text, 'current', 'current+%dc' % n)

    elif c == '.':
        s = text.get('current+1c', 'current lineend')
        n = re.match('\s*\w*', s).end()
        Select(text, 'current', 'current+%dc' % (n + 1))

    elif c == ',': # for test: (a, b(c, d=5), e); for a, b in c; a, b = c, 'd'
        s = text.get('current+1c', 'end')
        n1 = n2 = 0
        for n, c1 in enumerate(s):
            if n1 == n2 and c1 in ',)]}':
                break
            n1 += c1 in '([{'
            n2 += c1 in ')]}'
        Select(text, 'current', 'current+%dc' % (n + 1))

    else: # charset: !$%&*+,-/;<=>?@^|~  for test: s.split('\n')[:ln]
        p1, p2 = MatchSpan(r'[^\w()[\]{}\'" ]+', line, col) # 不"粘"括号空格和引号
        Select(text, 'current linestart+%dc' % p1, 'current linestart+%dc' % p2)
        # Select(text, 'current', 'current+1c')


class SmartSelect:
    def __init__(self, parent):
        FixTextSelect(parent.root)
        parent.text.bind('<Double-Button-1>', Selecting)
