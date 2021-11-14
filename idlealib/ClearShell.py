"""清空Shell"""

# TODO 删除一次Squeezer后再次Squeeze会报错（但不影响其他）


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


from idlelib.pyshell import PyShell


class ClearShell:
    def __init__(self, parent):
        if isinstance(parent, PyShell):
            self.text = parent.per.bottom # TODO 研究一下作用原理

            parent.rmenu.add_separator()
            parent.rmenu.add_command(label='Clear shell', command=self.Clear)
            parent.add_adv_menu('Clear shell', self.Clear)

    def Clear(self):
        find = False
        for tag in ['stdout', 'stderr']:
            ranges = self.text.tag_ranges(tag)
            for i in range(len(ranges), 0, -2):
                st, ed = ranges[i-2], ranges[i-1]
                self.text.delete(st.string + 'linestart', ed) # `linestart` for delete Squeezed text
                find = True

        if not find:
            self.text.delete('1.0', 'iomark linestart')


# Ref: ~\idlexlib\extensions\ClearWindow.py
