"""添加和取消注释"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
import re
import sys


class AutoComment:
    def __init__(self, parent):
        self.text = parent.text

        if sys.version_info < (3, 7):
            self.get_region = parent.get_region
            self.set_region = parent.set_region
        else:
            self.get_region = parent.fregion.get_region
            self.set_region = parent.fregion.set_region

        self.text.bind('<Control-/>', self.auto_comment_region_event)
        self.text.bind('<<comment-region>>', self.comment_region_event)
        self.text.bind('<<uncomment-region>>', self.uncomment_region_event)

    def auto_comment_region_event(self, evt):
        head, tail, chars, lines = self.get_region()
        lines.pop()

        prefix = os.path.commonprefix(lines)
        m = re.match(r'(\s*)(#?)', prefix)
        header, comment = m.groups()
        length = len(header)
        if comment:
            lines = [header + re.sub(r'^(##|# |#)', '', line[length:]) for line in lines]
        else:
            lines = [header + '# ' + line[length:] for line in lines]

        self.set_region(head, tail, chars, lines + [''])
        return 'break'

    def comment_region_event(self, evt):
        head, tail, chars, lines = self.get_region()
        for pos in range(len(lines) - 1):
            indent, code = re.findall(r'(\s*)(.*)', lines[pos])[0]
            lines[pos] = indent + '# ' + code if code else indent + code
        self.set_region(head, tail, chars, lines)
        return 'break'

    def uncomment_region_event(self, evt):
        head, tail, chars, lines = self.get_region()
        for pos in range(len(lines)):
            indent, comment, code = re.findall(r'(\s*)(##|# |#)?(.*)', lines[pos])[0]
            lines[pos] = indent + code
        self.set_region(head, tail, chars, lines)
        return 'break'
