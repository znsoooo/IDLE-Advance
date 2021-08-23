'''当选区为空时复制/剪切复制当前行'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class CopyNoSelect:
    def __init__(self, parent):
        self.text = parent.text
        parent.before_copy.insert(0, self.FixNoSelect) # make sure run first

    def FixNoSelect(self):
        if not self.text.tag_ranges("sel"):
            self.text.tag_add('sel', 'insert linestart', 'insert+1l linestart')
            self.text.mark_set('insert', 'insert linestart')
