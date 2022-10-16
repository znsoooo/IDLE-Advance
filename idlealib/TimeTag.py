'''插入时间戳注释'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import time


class TimeTag:
    def __init__(self, parent):
        self.text = parent.text

        parent.text.bind('<F4>', self.Insert)

    def Insert(self, evt):
        tag = time.strftime(' # %Y-%m-%d %H:%M:%S')
        header = self.text.get('insert linestart', 'insert')
        if not header.strip():
            tag = tag[1:] + '\n' + header
        self.text.insert('insert', tag)
