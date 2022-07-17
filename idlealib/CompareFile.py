'''文本比较'''

# TODO 优先比对已经打开的文件（列表）


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import sys
import tkinter as tk

if sys.version_info > (3, 6):
    from idlelib.config import idleConf
else:
    from idlelib.configHandler import idleConf

diff_path = idleConf.GetUserCfgDir() + '/diff.html'


def ReadFile(file):
    with open(file, encoding='u8') as f:
        return f.read()


def HtmlDiff(s1, s2):
    import difflib
    import webbrowser
    d = difflib.HtmlDiff()
    with open(diff_path, 'w', encoding='u8') as f:
        f.write(d.make_file(s1.split('\n'), s2.split('\n')))
    webbrowser.open(diff_path)


class CompareFile(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.text = parent.text
        self.io = parent.io

        parent.add_adv_menu('Compare to File', self.CompareFile, sp=True)
        parent.add_adv_menu('Compare to Clipboard', self.CompareClipboard)

    def CompareFile(self):
        p2 = self.io.askopenfile()
        if p2:
            s1 = self.text.get('1.0', 'end-1c')
            s2 = ReadFile(p2)
            HtmlDiff(s1, s2)

    def CompareClipboard(self):
        s1 = self.text.get('sel.first', 'sel.last')
        s2 = self.text.clipboard_get()
        HtmlDiff(s1, s2)
