"""保存时删除后续空格"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re


class TrimTrailing:
    def __init__(self, parent):
        self.text = parent.text
        parent.before_save.append(self.callback)

    def callback(self):
        text = self.text
        index = text.index('insert')
        s1 = text.get('1.0', 'end-1c')
        s2 = s1.replace('\r\n', '\n').replace('\r', '\n')
        s2 = re.sub(' +$', '', s2, flags=re.M)

        if s1 != s2:
            text.undo_block_start()
            text.delete('1.0', 'end-1c')
            text.insert('1.0', s2)
            text.mark_set('insert', index)
            text.see('insert linestart')
            text.undo_block_stop()
