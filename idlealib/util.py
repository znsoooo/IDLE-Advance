'''文本索引转换函数'''

def Cur2Lc(cur):
    return tuple(map(int, cur.split('.')))


def Pos2Cur(s, pos):
    ss = s[:pos].split('\n')
    cur = '%d.%d'%(len(ss), len(ss[-1]))
    return cur


def Cur2Pos(s, cur):
    ln, col = Cur2Lc(cur)
    ss = s.split('\n')[:ln]
    ss[-1] = ss[-1][:col] # 如果不还原ss而直接计算前ln行+col,可能造成第1行的转换错误
    pos = len('\n'.join(ss))
    return pos


def Select(text, c1, c2, ins=0):
    text.mark_set('insert', [c1, c2][ins])
    text.tag_remove('sel', '1.0', 'end')
    text.tag_add('sel', c1, c2)


def SelectSpan(text, span, ins):
    s = text.get('1.0', 'end')
    p1, p2 = span
    c1, c2 = Pos2Cur(s, p1), Pos2Cur(s, p2)
    Select(text, c1, c2, ins)
    text.see(c1)


