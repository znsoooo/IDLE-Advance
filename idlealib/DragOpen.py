'''拖拽打开'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class DragOpen:
    def __init__(self, parent):
        self.flist = parent.flist
        try:
            import windnd
            windnd.hook_dropfiles(parent.text, func=self.DragOpen)
        except ImportError as e:
            print('%s: %s' % (__name__, e))

    def DragOpen(self, files): # TODO 恢复记忆位置
        for file_b in files:
            file = file_b.decode('gbk')
            edit = self.flist.open(file)
            if edit:
                # TODO 由于滚动条存在导致有时候拖拽加载会闪退，增加下面两行可以避免
                edit.text.tag_add('sel', 'insert', 'insert+1c')
                edit.text.tag_remove('sel', '1.0', 'end')

                # TODO 是否可以
                # self.io.open(editFile=file)
