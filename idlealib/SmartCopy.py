'''仅拷贝Shell的代码'''

# TODO 添加顶部菜单


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


def GetCodes(text):
    if text.tag_ranges('sel'):
        sted = 'sel.first,sel.last'
    elif text.index('restart'):
        if text.compare('insert', '>', 'restart'):
            sted = 'restart,end'
        else:
            sted = '1.0,restart'
    else:
        sted = '1.0,end'
    st, ed = sted.split(',')
    if not text.tag_ranges('sel'):
        text.tag_add('sel', st, ed) # Select the area to see the selection.

    st_range = text.tag_nextrange('stdin', st)
    ed_range = text.tag_prevrange('stdin', ed)
    ranges = [cur.string for cur in text.tag_ranges('stdin')]
    ranges = [tuple(ranges[i:i + 2]) for i in range(0, len(ranges), 2)]
    if st_range and ed_range:
        ranges = ranges[ranges.index(st_range):ranges.index(ed_range) + 1]
        codes = [text.get(*r) for r in ranges]
        s = ''.join(codes)
        return s.strip()
    return ''


class SmartCopy:
    def __init__(self, parent):
        if not hasattr(parent, 'write'): # is not shell?
            return

        self.text = parent.text
        self.io = parent.io
        self.flist = parent.flist

        n = 5
        parent.rmenu.insert_separator(n)
        parent.rmenu.insert_command(n, label='Export to File', command=self.New)
        parent.rmenu.insert_command(n, label='Copy Code', command=self.Copy)

    def Copy(self):
        self.text.clipboard_clear()
        self.text.clipboard_append(GetCodes(self.text))

    def New(self): # See: idlelib.editor.EditorWindow.new_callback
        dirname, basename = self.io.defaultfilename()
        editwin = self.flist.new(dirname)
        editwin.text.insert('1.0', GetCodes(self.text))
