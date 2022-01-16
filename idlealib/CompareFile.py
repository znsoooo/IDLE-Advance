'''文本比较'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import difflib
import tkinter as tk

# import sys
# if sys.version_info > (3, 6):
#     from idlelib.textview import view_text
# else:
#     from idlelib.textView import view_text


# def show_html(title, s1, s2):
#     d = difflib.HtmlDiff()
#     with open(title + '.html', 'w', encoding='u8') as f:
#         f.write(d.make_file(s1.split('\n'), s2.split('\n')))
#     import webbrowser
#     webbrowser.open(title + '.html')


# TODO 优先比对已经打开的文件（列表）


def ReadFile(file):
    with open(file, encoding='u8') as f:
        return f.read()


class CompareFile(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent.menubar, tearoff=0)
        self.text = parent.text
        self.io = parent.io
        self.top = parent.top
        self.flist = parent.flist

        parent.add_adv_menu('Compare to File', self.CompareFile, sp=True)
        parent.add_adv_menu('Compare to Clipboard', self.CompareClipboard)

    def ShowDiff(self, s1, s2):
        diff = difflib.unified_diff(s1.splitlines(True), s2.splitlines(True))
        diff = ''.join(diff) or '@@ same text @@'
        editwin = self.flist.new(None)
        editwin.text.insert('1.0', diff)
        editwin.set_saved(True) # close with no prompt

    def CompareFile(self):
        p2 = self.io.askopenfile()
        if p2:
            s1 = self.text.get('1.0', 'end-1c')
            s2 = ReadFile(p2)
            self.ShowDiff(s1, s2)

    def CompareClipboard(self):
        s1 = self.text.get('sel.first', 'sel.last')
        s2 = self.text.clipboard_get()
        self.ShowDiff(s1, s2)
