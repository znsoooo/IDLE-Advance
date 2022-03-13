"""显示版本信息和自动升级"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


from os.path import dirname, join, isfile
from tkinter.messagebox import showinfo

p1 = join(dirname(__file__), 'docs/version.txt')
p2 = join(dirname(dirname(__file__)), 'version.txt')


class About:
    def __init__(self, parent):
        self.text = parent.text
        parent.add_adv_menu('About', self.about)

    def about(self): # TODO 添加readme文档、项目链接
        path = p1 if isfile(p1) else p2
        with open(path) as f:
            version = f.read()
            showinfo('Version', version, parent=self.text)

    def check(self): # TODO 检查版本是否最新
        pass

    def upgrade(self): # TODO 自动升级/自动获取当前Python的pip
        pass
