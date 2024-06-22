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

        prefix = os.path.commonprefix([line for line in lines[:-1] if line.strip()])
        m = re.match(r'(\s*)(#?)', prefix)
        indent, found_comment = m.groups()
        col = len(indent)

        for row in range(len(lines) - 1):
            if found_comment:
                lines[row] = indent + re.sub(r'^(##|# |#)', '', lines[row][col:])
                lines[row] = lines[row].strip() and lines[row]
            else:
                lines[row] = indent + '# ' + lines[row][col:]

        self.set_region(head, tail, chars, lines)
        return 'break'

    def comment_region_event(self, evt):
        head, tail, chars, lines = self.get_region()
        for row in range(len(lines) - 1):
            indent, code = re.findall(r'(\s*)(.*)', lines[row])[0]
            lines[row] = indent + '# ' + code if code else indent + code
        self.set_region(head, tail, chars, lines)
        return 'break'

    def uncomment_region_event(self, evt):
        head, tail, chars, lines = self.get_region()
        for row in range(len(lines)):
            indent, comment, code = re.findall(r'(\s*)(##|# |#)?(.*)', lines[row])[0]
            lines[row] = indent + code
        self.set_region(head, tail, chars, lines)
        return 'break'
