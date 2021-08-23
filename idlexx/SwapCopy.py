'''交换复制'''

# TODO 改为Ctrl-V的时候交换
# TODO Shell中没有标色


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


TAG = 'BREAK'

class SwapCopy:
    def __init__(self, parent):
        self.text = parent.text
        self.range = None
        self.text.bind('<Control-Shift-X>', self.Swaping)

    def Swaping(self, e):
        text = self.text
        range = text.tag_ranges('sel')
        if range:
            if self.range:
                (c1, c2), (c3, c4) = self.range, range
                if text.compare(c1, '>', c3): # 先替换前面的会导致后面的坐标错误
                    (c1, c2), (c3, c4) = (c3, c4), (c1, c2)
                if text.compare(c2, '>', c3):
                    self.Clear()
                    return
                s1 = text.get(c1, c2)
                s2 = text.get(c3, c4)
                text.undo_block_start()
                text.delete(c3, c4)
                text.insert(c3, s1)
                text.delete(c1, c2)
                text.insert(c1, s2)
                text.undo_block_stop()
                self.Clear()
            else:
                self.range = range # first
                text.tag_add(TAG, *range)
        else:
            self.Clear()

    def Clear(self):
        self.range = None  # clear setup
        self.text.tag_remove(TAG, '1.0', 'end')
