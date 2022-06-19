"""显示版本信息和自动升级"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os

import sys
if sys.version_info > (3, 6):
    from idlelib.textview import view_text
else:
    from idlelib.textView import view_text


def read_relative(filename):
    root = os.path.dirname(__file__)
    p1 = os.path.join(root, 'docs', filename)
    p2 = os.path.join(os.path.dirname(root), filename)
    path = p1 if os.path.isfile(p1) else p2
    with open(path, encoding='u8') as f:
        return f.read()


class About:
    def __init__(self, parent):
        self.text = parent.text
        parent.add_adv_menu('About', self.about)

    def about(self):
        view_text(self.text, 'idlea v' + read_relative('version.txt'), read_relative('readme.md'))

    def check(self): # TODO 检查版本是否最新
        pass

    def upgrade(self): # TODO 自动升级/自动获取当前Python的pip
        pass
