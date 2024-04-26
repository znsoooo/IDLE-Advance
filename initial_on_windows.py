import sys
import winreg


def SetRegValue(key, name='', value=''):
    root, key = key.split('\\', 1)
    key = winreg.CreateKey(getattr(winreg, root), key)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
    winreg.CloseKey(key)


def InitialOnWindows():
    if sys.platform != 'win32':
        return

    # Set for creating new Python file
    SetRegValue(r'HKEY_CURRENT_USER\Software\Classes\.py\ShellNew', 'FileName')

    # Get Python versions
    major = sys.version_info[0]
    minor = sys.version_info[1]
    bits = sys.maxsize.bit_length() + 1
    versions = (major, minor, bits)

    # Get paths for Python and script
    exe = sys.executable
    src = __import__('idlealib').__file__

    # Set context menu for 2 classes of files
    for cls in ['Python.File', 'Python.NoConFile']:
        root = r'HKEY_CURRENT_USER\Software\Classes\%s\Shell\editwithidleadv' % cls
        SetRegValue(root, 'MUIVerb', '&Edit with IDLE-Adv')
        SetRegValue(root, 'Subcommands')
        SetRegValue(root + r'\shell\edit%d%d-%d' % versions, 'MUIVerb', 'Edit with IDLE-Adv %d.%d (%d-bit)' % versions)
        SetRegValue(root + r'\shell\edit%d%d-%d\command' % versions, '', '"%s" "%s" "%%L" %%*' % (exe, src))


if __name__ == '__main__':
    InitialOnWindows()
