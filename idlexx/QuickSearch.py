'''快速正反搜索'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


# TODO 所有的搜搜窗口都不热点捕捉但是置前（不仅仅是F3启动）

from idlelib import search


class QuickSearch:
    def __init__(self, parent):
        self.text = parent.text
        self.text.bind('<F3>',       lambda e: self.FindPrev(False))
        self.text.bind('<Shift-F3>', lambda e: self.FindPrev(True))

    def FindPrev(self, back):
        searchdialog = search._setup(self.text)
        searchdialog.engine.backvar.set(back)
        searchdialog.find_again(self.text)
        searchdialog.top.grab_release() # 取消grab_set()窗口置顶
