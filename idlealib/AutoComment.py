"""添加和取消注释"""


import os
import re


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class AutoComment:
    def __init__(self, parent):
        self.text = parent.text
        self.get_region = parent.get_region
        self.set_region = parent.set_region
        self.text.bind('<Control-/>', self.callback)

    def callback(self, evt):
        head, tail, chars, lines = self.get_region()
        lines.pop()

        prefix = os.path.commonprefix(lines)
        m = re.match(r'(\s*)(##|# |#)?', prefix)
        header, comment = m.groups()
        if comment:
            start = len(header + comment)
        else:
            start = len(header)
            header += '# '
        lines = [header + line[start:] for line in lines]

        self.set_region(head, tail, chars, lines + [''])
        return 'break'
