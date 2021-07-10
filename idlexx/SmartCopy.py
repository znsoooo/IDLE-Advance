'''仅拷贝Shell的代码'''

# TODO 右键菜单、顶部菜单、拷贝区域范围代码、拷贝本次restart范围的代码

from idlelib.pyshell import PyShell


def GetCodes(text):
    if text.tag_ranges("sel"):
        sted = 'sel.first,sel.last'
    elif text.index('restart'):
        if text.compare('insert', '>', 'restart'):
            sted = 'restart,end'
        else:
            sted = '1.0,restart'
    else:
        sted = '1.0,end'
    st, ed = sted.split(',')

    st_range = text.tag_nextrange('stdin', st)
    ed_range = text.tag_prevrange('stdin', ed)
    ranges = [cur.string for cur in text.tag_ranges('stdin')]
    ranges = [tuple(ranges[i:i + 2]) for i in range(0, len(ranges), 2)]
    if st_range and ed_range:
        ranges = ranges[ranges.index(st_range):ranges.index(ed_range) + 1]
        codes = [text.get(*r) for r in ranges]
        s = ''.join(codes)
        return s
    return ''


class SmartCopy:
    def __init__(self, parent):
        self.text = parent.text
        if isinstance(parent, PyShell):
            self.text.bind('<F2>', self.Copying)

    def Copying(self, e):
        text = self.text
        s = GetCodes(text)
        print(s)

# TODO 增加右键、一键新建操作记录脚本

