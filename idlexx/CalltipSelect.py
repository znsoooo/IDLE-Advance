'''可选中函数提示'''

# TODO 显示完整的__doc__内容并自动调整文本框大小，需要修改idlelib.calltip.get_argspec函数，可能没有简洁的实现方法。


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import tkinter as tk
# import idlelib.calltip


# _MAX_LINES = idlelib.calltip._MAX_LINES
# _MAX_COLS = idlelib.calltip._MAX_COLS
#
#
# class MyCalltip(idlelib.calltip.Calltip):
#     def fetch_tip(self, expression, max_lines=_MAX_LINES, max_cols=_MAX_COLS):
#         idlelib.calltip._MAX_LINES = max_lines
#         idlelib.calltip._MAX_COLS = max_cols
#         self.expression = expression
#         return super().fetch_tip(expression)
#
#     def open_calltip(self, evalfuncs):
#         super().open_calltip(evalfuncs)
#
#         calltip = self.active_calltip
#         if not calltip: # not callable before "(".
#             return
#
#         self.top = calltip.tipwindow
#         self.text = calltip.anchor_widget
#         self.label = calltip.label
#         self.s = calltip.text
#         self.first = False
#
#         # Example:
#         # s2 = '\n'.join('%d: '%(ln+1) + line*2 for ln, line in enumerate(self.s.split('\n')))
#         # self.label.config(text=s2) # hack in !!!
#
#         self.text.bind('<FocusOut>', print) # unbind auto hide. TODO 运行完移除，注意别的影响
#
#         # self.label.bind('<Button>', self.OnClick)  # Exp 1: click and insert
#         self.label.bind('<Enter>', self.OnEnter) # Exp 2: enter and change widget to tk.Text
#
#         # Exp 3: show first as tk.Text and reshape to same size
#         # self.top.update()
#         # self.Label2Text(self.s)
#
#     def OnClick(self, e):
#         h = self.label.winfo_height()
#         y = e.y
#         lines = self.s.split('\n')
#         ln = y // (h // len(lines))
#         self.text.insert('insert', lines[ln])
#
#     def OnEnter(self, e):
#         s2 = self.fetch_tip(self.expression, 999, 999)
#         self.Label2Text(s2)
#
#     def Label2Text(self, s):
#         if self.first:
#             return
#
#         self.first = True
#         self.label.forget()
#
#         # TODO 没有双击选中了
#         text2 = tk.Text(self.top, background='#ffffe0', relief='solid', borderwidth=1, font=self.text['font'])
#         text2.insert('1.0', s)
#         text2.pack(expand=1, fill='both')
#
#         h = self.top.winfo_height()
#         w = self.top.winfo_width()
#         self.top.geometry('%dx%d'%(w, h))
#
#
# idlelib.calltip.Calltip = MyCalltip


class CalltipSelect:
    def __init__(self, parent):
        self.text = parent.text
        self.ctip = parent.ctip

        self.ctip._open_calltip = self.ctip.open_calltip
        self.ctip.open_calltip = self.open_calltip # Good: add actions after original functions

    def open_calltip(self, e):
        self.ctip._open_calltip(False)
        self.first = False
        self.text.bind('<FocusOut>', print) # unbind auto hide. TODO 运行完移除，注意别的影响

        calltip = self.ctip.active_calltip
        self.top   = calltip.tipwindow
        self.label = calltip.label
        self.s     = calltip.text

        self.top.update()
        self.Label2Text(self.s)

    def Label2Text(self, s):
        if self.first:
            return
        self.first = True

        self.label.forget()
        text2 = tk.Text(self.top, background='#ffffe0', relief='solid', borderwidth=1, font=self.text['font'])
        text2.insert('1.0', s)
        text2.pack(expand=1, fill='both')
        # TODO 没有双击选中了

        h = self.top.winfo_height()
        w = self.top.winfo_width()
        self.top.geometry('%dx%d' % (w, h))
