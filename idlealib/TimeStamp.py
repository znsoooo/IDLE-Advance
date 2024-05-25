'''插入时间戳注释'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import re
import time


class TimeStamp:
    def __init__(self, parent):
        self.text = parent.text

        parent.text.bind('<F4>', self.Insert)

    def Insert(self, evt):
        if evt.state != 8:  # if not press any modifier keys
            return

        line = self.text.get('insert linestart', 'insert lineend')
        indent = re.match(r'^\s*', line).group()

        stamp = time.strftime('# %Y-%m-%d %H:%M:%S')
        line2 = indent + stamp + '\n'

        self.text.insert('insert linestart', line2)
