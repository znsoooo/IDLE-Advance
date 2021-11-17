'''配置右键菜单、桌面快捷方式、开始菜单、右键新建的界面菜单'''

# TODO 自动匹配pythonw.exe

import os
import sys
import time
import winreg
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

options = ('All Positions Below', 'Lnk: Desktop Shortcut', 'Lnk: Start Up Menu', 'Reg: Right Click Menu', 'Reg: Create New File')


# ---------------------------------------------------------------------------
# make link
# ---------------------------------------------------------------------------


def MakeLink(exe, folder, file, cmd):
    try:
        import winshell
        root = os.path.dirname(exe)
        path = os.path.join(folder, file)
        winshell.CreateShortcut(path, exe, cmd, root, (root + r'\Lib\idlelib\Icons\idle.ico', 0))
    except ImportError:
        os.popen('explorer "%s"' % folder)
        top.clipboard_clear()
        top.clipboard_append('"%s" %s' % (exe, cmd))
        time.sleep(0.5)
        showinfo('Info', 'Copy `cmd` and create shortcut by right click in opened explorer')


# ---------------------------------------------------------------------------
# edit regedit
# ---------------------------------------------------------------------------


def GetDir(name, local=False): # Name: 'Desktop', 'SendTo', 'Programs', 'Startup'
    path = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    if local:
        name = 'Common ' + name
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    else:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
    return winreg.QueryValueEx(key, name)[0]


def DeleteRecu(key):
    for i in range(winreg.QueryInfoKey(key)[0]):
        name = winreg.EnumKey(key, i)
        DeleteRecu(winreg.OpenKey(key, name))
        winreg.DeleteKey(key, name)


def DeleteKey(key, name=''):
    root, p = key.split('\\', 1)
    key2 = winreg.OpenKey(getattr(winreg, root), p)
    if name:
        winreg.DeleteValue(key2, name)
    else:
        DeleteRecu(key2)
        winreg.DeleteKey(getattr(winreg, root), p)


def SetKey(key, name='', val=''):
    root, p = key.split('\\', 1)
    key2 = winreg.CreateKey(getattr(winreg, root), p)
    winreg.SetValueEx(key2, name, 0, winreg.REG_SZ, val)


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------


def Loop(fun):
    for name in options[1:]:
        v0.set(name)
        Switch()
        fun()
    v0.set(options[0])
    Switch()


def Add():
    id = options.index(v0.get())
    s1, s2, s3, s4 = v1.get(), v2.get(), v3.get(), v4.get()
    if id == 0:
        Loop(Add)
        return
    try:
        if id in [1, 2]: # lnk
            MakeLink(s1, s2, s3, s4)
        elif id in [3, 4]: # reg
            SetKey(s2, s3, s4)
    except Exception as e:
        showinfo('Error', str(e))
    # else:
    #     showinfo('Info', 'Success!')


def Remove():
    id = options.index(v0.get())
    s2, s3, s4 = v2.get(), v3.get(), v4.get()
    if id == 0:
        Loop(Remove)
        return
    try:
        if id in [1, 2]: # lnk
            p = os.path.join(s2, s3)
            if os.path.isfile(p):
                os.remove(p)
        elif id in [3, 4]: # reg
            DeleteKey(s2, s3)
    except Exception as e:
        showinfo('Error', str(e))
    # else:
    #     showinfo('Info', 'Success!')


def Switch(*_):
    id = options.index(v0.get())
    exe = v1.get()
    src = os.path.abspath('../__main__.py')
    s2 = s3 = s4 = ''
    if id == 1:
        s2 = GetDir('Desktop')
        s3 = 'IDLE-Advance.lnk'
        s4 = '"%s"' % src
    elif id == 2:
        s2 = GetDir('Programs')
        s3 = 'Python IDLE-Advance.lnk'
        s4 = '"%s"' % src
    elif id == 3:
        s2 = r'HKEY_CURRENT_USER\Software\Classes\Python.File\Shell\Edit with IDLE-Adv\command'
        s4 = '"{}" "{}" "%L" %*'.format(exe, src)
    elif id == 4:
        s2 = r'HKEY_CURRENT_USER\Software\Classes\.py\ShellNew'
        s3 = 'FileName'
    v2.set(s2)
    v3.set(s3)
    v4.set(s4)


def Center(self):
    self.withdraw() # withdraw/deiconify 阻止页面闪烁
    self.update_idletasks()
    x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
    y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
    self.geometry('+%d+%d' % (x, y))
    self.deiconify()


if __name__ == '__main__':
    top = tk.Tk()
    top.title('IDLE-Advance Context Helper')
    top.resizable(1, 0)
    top.columnconfigure(1, weight=1) # for `grid` can expand

    v0 = tk.StringVar(value='All')
    v1 = tk.StringVar(value=sys.executable)
    v2 = tk.StringVar(value='')
    v3 = tk.StringVar(value='')
    v4 = tk.StringVar(value='')

    v1.trace_add('write', Switch)

    text = tk.Label(top, text=' Add to: ')
    menu = ttk.OptionMenu(top, v0, options[0], *options, command=Switch)
    menu.config(width=20)
    btn1 = ttk.Button(top, text='Add',    command=Add)
    btn2 = ttk.Button(top, text='Remove', command=Remove)

    text.grid(row=0, column=0, sticky='e')
    menu.grid(row=0, column=1, sticky='w')
    btn1.grid(row=0, column=2)
    btn2.grid(row=0, column=3)

    for r, (name, var) in enumerate(zip(['exe', 'path', 'name', 'cmd'], [v1, v2, v3, v4])):
        tk.Label(top, text=' %s: ' % name).grid(row=r+1, column=0, sticky='e')
        tk.Entry(top, textvariable=var)   .grid(row=r+1, column=1, sticky='we', columnspan=3)

    Center(top)

    top.mainloop()
