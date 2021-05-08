import tkinter as tk


class ReplaceBar(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # TODO 从idle中获取设置
        self.patvar  = tk.StringVar(self, '')     # search pattern
        self.replvar = tk.StringVar(self, '')     # replace string
        self.revar   = tk.BooleanVar(self, False) # regular expression?
        self.casevar = tk.BooleanVar(self, False) # match case?
        self.wordvar = tk.BooleanVar(self, False) # match whole word?
        self.backvar = tk.BooleanVar(self, False) # search backwards?

        self.patvar.trace('w', self.Find)
        self.replvar.trace('w', self.Find)

        tk.Label(self, text='Find:').pack(side='left')
        tk.Entry(self, width=8, textvariable=self.patvar).pack(side='left', fill='x', expand=True)
        tk.Label(self, text='Repl:').pack(side='left')
        tk.Entry(self, width=8, textvariable=self.replvar, validatecommand=self.Find).pack(side='left', fill='x', expand=True)

        tk.Checkbutton(self, text='Re',   variable=self.revar)  .pack(side='left')
        tk.Checkbutton(self, text='Case', variable=self.casevar).pack(side='left')
        tk.Checkbutton(self, text='Word', variable=self.wordvar).pack(side='left')

        tk.Button(self, relief='groove', text='<<', command=self.Prev).pack(side='left')
        tk.Button(self, relief='groove', text='>>', command=self.Next).pack(side='left')
        tk.Button(self, relief='groove', text='Replace', command=self.Replace).pack(side='left')
        tk.Button(self, relief='groove', text='Replace All', command=self.ReplaceAll).pack(side='left')

        tk.Label(self, text='Match: 0/0').pack(side='left')


    def GetSetting(self):
        print('------')
        print(self.patvar.get())
        print(self.replvar.get())
        print(self.revar.get())
        print(self.casevar.get())
        print(self.wordvar.get())
        print(self.backvar.get())


    def Find(self, *_):
        self.GetSetting()


    def Prev(self):
        self.backvar.set(True)
        self.GetSetting()


    def Next(self):
        self.backvar.set(False)
        self.GetSetting()


    def Replace(self):
        self.GetSetting()
        

    def ReplaceAll(self):
        self.GetSetting()
        


top = tk.Tk()
text = ReplaceBar(top)
text.pack(fill='x')
top.mainloop()
