'''横向滚动条'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import sys
PY37 = sys.version_info > (3, 7)

import tkinter as tk


class ScrollHorizontal:
    def __init__(self, parent):
        text = parent.text
        frame = parent.text_frame

        # TODO 会导致拖拽打开文件时闪退
        hbar = tk.Scrollbar(frame, orient='h')
        hbar['command'] = text.xview
        text['xscrollcommand'] = hbar.set
        if PY37:
            hbar.grid(row=2, column=1, sticky='nsew')
        else:
            hbar.pack(fill='x', side='bottom')
        # TODO 参考 idlelib.textview.ViewWindow 的 AutoHiddenScrollbar 方法
