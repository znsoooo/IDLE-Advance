"""添加Windows右键菜单打开"""


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


import os
import sys
import tkinter as tk


# Get Python versions
major = sys.version_info[0]
minor = sys.version_info[1]
bits = sys.maxsize.bit_length() + 1
versions = (major, minor, bits)

# Get paths for Python and script
exe = sys.executable
src = os.path.abspath(__file__ + '/../__main__.py')

# Select 2 classes of file's type
classes = ['Python.File', 'Python.NoConFile']


def SetRegValue(key, name='', value=''):
    import winreg
    root, key = key.split('\\', 1)
    key = winreg.CreateKey(getattr(winreg, root), key)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
    winreg.CloseKey(key)


def DeleteReg(key, name=''):
    import winreg
    if isinstance(key, str):
        root, key = key.split('\\', 1)
        key = winreg.OpenKey(getattr(winreg, root), key, 0, winreg.KEY_ALL_ACCESS)
    if name:
        winreg.DeleteValue(key, name)
    else:
        for i in range(winreg.QueryInfoKey(key)[0]):
            name = winreg.EnumKey(key, i)
            DeleteReg(winreg.OpenKey(key, name))
        winreg.DeleteKey(key, '')


def AddWindowsMenu():
    SetRegValue(r'HKEY_CURRENT_USER\Software\Classes\.py\ShellNew', 'FileName')

    for cls in classes:
        root = r'HKEY_CURRENT_USER\Software\Classes\%s\Shell\editwithidleadv' % cls
        SetRegValue(root, 'MUIVerb', '&Edit with IDLE-Adv')
        SetRegValue(root, 'Subcommands')
        SetRegValue(root + r'\shell\edit%d%d-%d' % versions, 'MUIVerb', 'Edit with IDLE-Adv %d.%d (%d-bit)' % versions)
        SetRegValue(root + r'\shell\edit%d%d-%d\command' % versions, '', '"%s" "%s" "%%L" %%*' % (exe, src))


def DeleteWindowsMenu():
    for cls in classes:
        root = r'HKEY_CURRENT_USER\Software\Classes\%s\Shell\editwithidleadv' % cls
        DeleteReg(root + r'\shell\edit%d%d-%d' % versions)


def DeleteWindowsMenuAll():
    for cls in classes:
        DeleteReg(r'HKEY_CURRENT_USER\Software\Classes\%s\Shell\editwithidleadv' % cls)


class ContextManager(tk.Menu):
    def __init__(self, parent):
        if sys.platform == 'win32':
            tk.Menu.__init__(self, parent.menubar, tearoff=0)

            self.add_command(label='Add Context Menu', command=AddWindowsMenu)
            self.add_command(label='Remove Context Menu', command=DeleteWindowsMenu)
            self.add_command(label='Remove All Context Menu', command=DeleteWindowsMenuAll)

            parent.amenu.insert_cascade(0, label='Context Manager', menu=self)
