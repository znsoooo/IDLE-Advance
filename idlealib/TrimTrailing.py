"""保存时删除后续空格"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re


class TrimTrailing:
    def __init__(self, parent):
        self.text = parent.text
        parent.before_save.append(self.callback)

    def get_line(self, index):
        return int(self.text.index(index).split('.')[0])

    def callback(self):
        text = self.text

        ln_end = self.get_line('end-1c')
        ln_ins = self.get_line('insert')
        if text.tag_ranges('sel'):
            ln_ins = -1

        text.undo_block_start()

        for ln in range(1, ln_end + 1):
            # skip current line or in selection mode
            if ln != ln_ins:
                s = text.get('%d.0' % ln, '%d.end' % ln)
                m = re.search(' +$', s)
                if m:
                    text.delete('%d.%d' % (ln, m.start()), '%d.end' % ln)

        text.undo_block_stop()
