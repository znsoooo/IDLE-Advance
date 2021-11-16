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

        print(os.getcwd())

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


'F:\lsx\coding\idle\idlealib\scripts'
'scripts\readme.md'
"F:\lsx\代码说明.docx"
"notepad 1.txt"
"C:\\"
"cmd /k ipconfig"

# todo 相对文件夹打不开
