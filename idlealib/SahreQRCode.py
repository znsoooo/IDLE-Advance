'''将选中代码转化为二维码'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import tkinter as tk
from PIL import ImageTk

import qrcode

# TODO 过长文本保护（Unicode长度）/翻页显示
# TODO 调整弹出位置


def qrmake(qrstr): # max about 2340 chars
    qr = qrcode.QRCode(box_size=2, border=2)
    qr.add_data(qrstr)
    qr.best_fit()
    qr.makeImpl(False, 3) # 3 or 6
    img = qr.make_image()
    return img


class ViewWindow(tk.Toplevel):
    def __init__(self, parent, title, text):
        super().__init__(parent)
        self.transient(parent) # hide minimize/maximize icon
        x = parent.winfo_rootx() + 10
        y = parent.winfo_rooty() + 10
        self.geometry('+%d+%d'%(x, y))
        self.title(title)
        self.img = ImageTk.PhotoImage(image=qrmake(text), master=self)
        qrc = tk.Label(self, image=self.img)
        qrc.pack()

        self.focus()
        self.bind('<Return>', lambda e: self.destroy())
        self.bind('<Escape>', lambda e: self.destroy())


class SahreQRCode:
    def __init__(self, parent):
        self.text = parent.text
        self.top = parent.top

        self.text.bind('<<share-qrcode>>', self.Post)

        parent.rmenu.add_separator()
        parent.rmenu.add_command(label='Share Code', command=self.Post)

        parent.add_adv_menu('Share QRCode', self.Post, sp=True)

    def Post(self):
        s = self.text.get('sel.first', 'sel.last') or self.text.get('1.0', 'end')
        s = s[:2000] # TODO 过长保护提示
        brief = s if len(s) < 21 else s[:10] + ' ... ' + s[-10:]
        ViewWindow(self.top, '%d chars: %s'%(len(s), brief), s)
