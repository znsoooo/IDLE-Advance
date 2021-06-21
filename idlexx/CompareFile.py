import os
import difflib
import webbrowser
import tkinter as tk
from idlelib.textview import ViewWindow, Button  # Button is ttk.Button


# TODO 支持选择py或全部格式文件

def CompareFile(parent, file1, file2):  # TODO 移植到不依赖输入，支持任意文件接口
    with open(file1, encoding='u8') as f:
        ss1 = f.read().split('\n')
    with open(file2, encoding='u8') as f:
        ss2 = f.read().split('\n')
    title = 'Different between %s and %s' % (os.path.basename(file1), os.path.basename(file2))  # TODO 我之前时怎么命名的？

    d = difflib.Differ()
    ss3 = d.compare(ss1, ss2)
    text = '\n'.join(ss3)
    dlg = ViewWindow(parent, title, text, wrap='none', _utest=True)
    dlg.viewframe.button_ok.forget()  # ok按钮用的是ViewFrame里的控件!

    def show_html():
        d = difflib.HtmlDiff()
        with open(title + '.html', 'w', encoding='u8') as f:
            f.write(d.make_file(ss1, ss2))
        webbrowser.open(title + '.html')

    toolbar = tk.Frame(dlg)
    Button(toolbar, text='HTML', command=show_html).pack(side='left')
    Button(toolbar, text='Close', command=dlg.viewframe.ok).pack(side='left')
    toolbar.pack()

    dlg.wait_window()
