"""重复选中文本"""

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class DuplicateLines:
    def __init__(self, parent):
        self.text = parent.text
        self.text.bind('<Control-D>', self.callback)

    def callback(self, evt):
        if not self.text.tag_ranges('sel'):
            self.text.tag_add('sel', 'insert linestart', 'insert+1l linestart')
        # else:
        #     self.text.tag_add('sel', 'sel.first linestart', 'sel.last-1c+1l linestart')
        self.text.mark_set('insert', 'sel.first')
        self.text.insert('sel.last', self.text.get('sel.first', 'sel.last'))
