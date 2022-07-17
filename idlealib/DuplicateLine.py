"""重复选中文本/删除当前行"""

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class DuplicateLines:
    def __init__(self, parent):
        self.text = parent.text
        self.text.bind('<Control-d>', self.copy)
        self.text.bind('<Control-D>', self.delete)

    def copy(self, evt):
        if not self.text.tag_ranges('sel'):
            self.text.tag_add('sel', 'insert linestart', 'insert+1l linestart')
        self.text.mark_set('insert', 'sel.first')
        self.text.insert('sel.last', self.text.get('sel.first', 'sel.last'))
        return 'break'

    def delete(self, evt):
        if not self.text.tag_ranges('sel'):
            self.text.tag_add('sel', 'insert linestart', 'insert+1l linestart')
        self.text.delete('sel.first', 'sel.last')
        return 'break'
