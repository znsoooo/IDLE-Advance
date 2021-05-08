import tkinter as tk


class ScrolledText(tk.Frame): # Good! by lsx
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        vbar = tk.Scrollbar(self)
        vbar.pack(side='right', fill='y')
        text = tk.Text(self, yscrollcommand=vbar.set)
        text.pack(side='left', fill='both', expand=True)
        vbar['command'] = text.yview


top = tk.Tk()
text = ScrolledText(top)
text.pack()
top.mainloop()

