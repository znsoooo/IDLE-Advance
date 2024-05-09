'''快速打开选中的文本'''

import os

if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class QuickOpen:
    def __init__(self, parent):
        self.text = parent.text
        self.top = parent.top

        parent.rmenu.add_separator()
        # parent.rmenu.add_command(label='Open', command=self.Open)
        parent.rmenu.add_command(label='Start', command=self.Start)

        # parent.add_adv_menu('Quick Open', self.Open)
        parent.add_adv_menu('Quick Start', self.Start)

    # def Open(self):
    #     if not self.text.tag_ranges('sel'):
    #         return
    #     s = self.text.get('sel.first', 'sel.last')
    #     os.popen('explorer ' + s)

    def Start(self):
        if not self.text.tag_ranges('sel'):
            return
        s = self.text.get('sel.first', 'sel.last')
        os.popen('start ' + s)


TEST = r"""
    C:\Windows\System32\calc.exe
    C:\Windows\System32\
    .\docs\LICENSE.txt
    .\docs\
    notepad new.txt
    cmd /k ipconfig
"""
